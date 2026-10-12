from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
import numpy as np
import json
import io
import base64
import requests
from pydantic import BaseModel
from backend.chatbot import ask_agrisense

from PIL import Image

from backend.advisory import get_advisory
from backend.treatment_engine import get_treatment


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AgriSense AI",
    description="AI-powered crop disease detection and farm advisory system",
    version="1.4"
)


# ==========================================
# CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# MODEL PATHS
# ==========================================

MODEL_PATH = "ml_model/agrisense_model.keras"
CLASS_PATH = "ml_model/class_names.json"


# ==========================================
# LOAD MODEL (Keras config compatibility)
# ==========================================
import keras
import inspect
from keras.src.initializers import random_initializers
from keras.src.layers.normalization import batch_normalization
from keras.src.layers.core import dense

print("Loading AgriSense AI model...")

# Remove fields saved by a different Keras version but unsupported here.
def _patch_init(cls, ignored_keys):
    original = cls.__init__
    def compatible(self, *args, **kwargs):
        for key in ignored_keys:
            kwargs.pop(key, None)
        return original(self, *args, **kwargs)
    cls.__init__ = compatible

# Initializers can contain extra axes fields in the saved model.
for _name in ("VarianceScaling", "GlorotUniform", "HeNormal", "HeUniform",
              "RandomNormal", "RandomUniform", "Zeros", "Ones"):
    _cls = getattr(random_initializers, _name, None)
    if _cls is not None:
        _patch_init(_cls, {"input_axes", "output_axes"})

# BatchNormalization and Dense have additional legacy config fields.
_patch_init(batch_normalization.BatchNormalization,
            {"renorm", "renorm_clipping", "renorm_momentum"})
_patch_init(dense.Dense, {"quantization_config"})

# Also patch public aliases used by Keras deserialization.
keras.layers.BatchNormalization = batch_normalization.BatchNormalization
keras.layers.Dense = dense.Dense

model = keras.models.load_model(MODEL_PATH, compile=False)
print("Model loaded successfully!")

# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open(CLASS_PATH, "r") as file:

    class_names = json.load(file)


print(
    f"Total classes: {len(class_names)}"
)


# ==========================================
# EFFICIENTNETB0 + GRAD-CAM SETUP
# ==========================================

backbone = model.get_layer(
    "efficientnetb0"
)

target_layer = backbone.get_layer(
    "top_activation"
)

gap_layer = model.get_layer(
    "global_average_pooling2d"
)

dropout_layer = model.get_layer(
    "dropout"
)

dense_layer = model.get_layer(
    "dense"
)

print(
    "Grad-CAM target layer:",
    target_layer.name
)


# ==========================================
# AI CONFIDENCE / UNCERTAINTY GUARD
# ==========================================

def get_confidence_guard(confidence):

    # HIGH CONFIDENCE
    if confidence >= 70:

        return {
            "confidence_level": "High",

            "prediction_reliable": True,

            "uncertainty_message":
                "The AI has high confidence in this prediction."
        }


    # MODERATE CONFIDENCE
    elif confidence >= 50:

        return {
            "confidence_level": "Moderate",

            "prediction_reliable": True,

            "uncertainty_message":
                "The AI has moderate confidence. "
                "Verify the result with a clear image "
                "and visual inspection."
        }


    # LOW CONFIDENCE
    else:

        return {
            "confidence_level": "Low",

            "prediction_reliable": False,

            "uncertainty_message":
                "The AI could not reliably identify "
                "the crop condition. Please upload a "
                "clearer leaf image or consult an "
                "agricultural expert."
        }


# ==========================================
# HEALTH + SEVERITY ESTIMATION
# ==========================================

def calculate_health_and_severity(
    prediction_name,
    confidence
):
    """
    Provides a preliminary health indicator
    based on the model's predicted class.

    This is NOT a validated measurement of
    actual plant health or crop damage.
    """

    prediction_lower = (
        prediction_name.lower()
        .replace(" ", "_")
    )

    # --------------------------------------
    # HEALTHY CLASS
    # --------------------------------------

    if "healthy" in prediction_lower:

        health_score = 100.0

        severity = "Predicted Healthy"

        severity_description = (
            "The model classified this leaf as "
            "healthy. This result is an AI prediction "
            "and does not guarantee that the plant "
            "is free from disease."
        )

        return (
            health_score,
            severity,
            severity_description
        )

    # --------------------------------------
    # UNKNOWN / UNCERTAIN CLASS
    # --------------------------------------

    if (
        prediction_name == "Leaf Not in Database"
        or confidence < 60
    ):

        health_score = None

        severity = "Unable to Assess"

        severity_description = (
            "The disease prediction is uncertain. "
            "The actual health condition of this leaf "
            "cannot be reliably determined. Upload a "
            "clear image or consult an agricultural expert."
        )

        return (
            health_score,
            severity,
            severity_description
        )

    # --------------------------------------
    # POSSIBLE DISEASE
    # --------------------------------------

    if confidence >= 85:

        health_score = None

        severity = "Disease Prediction — High Confidence"

        severity_description = (
            "The model predicts a possible disease "
            "with high confidence. Confidence does "
            "not measure disease severity. Inspect "
            "the plant before taking action."
        )

    else:

        health_score = None

        severity = "Disease Prediction — Needs Verification"

        severity_description = (
            "The model predicts a possible disease, "
            "but the result needs verification. "
            "Inspect the leaf and confirm the diagnosis "
            "before applying any treatment."
        )

    return (
        health_score,
        severity,
        severity_description
    )



# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    return {

        "message":
            "AgriSense AI Backend is running",

        "model":
            "EfficientNetB0",

        "classes":
            len(class_names),

        "gradcam":
            True,

        "health_severity":
            True,

        "uncertainty_guard":
            True,

        "treatment_engine":
            True
    }
class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.post("/chat")
async def chat(request: ChatRequest):

    answer = ask_agrisense(
        question=request.message,
        history=request.history
    )

    return {
        "response": answer
    }

# ==========================================
# GRAD-CAM FUNCTION
# ==========================================

def generate_gradcam(image_array):

    # --------------------------------------
    # Convert image to TensorFlow tensor
    # --------------------------------------

    input_tensor = tf.convert_to_tensor(
        image_array,
        dtype=tf.float32
    )


    # --------------------------------------
    # Gradient calculation
    # --------------------------------------

    with tf.GradientTape() as tape:

        # Run EfficientNet

        x = backbone(
            input_tensor,
            training=False
        )


        # Get target activation

        target_activation = target_layer(
            x,
            training=False
        )


        # Classification head

        x = gap_layer(
            target_activation
        )

        x = dropout_layer(
            x,
            training=False
        )

        predictions = dense_layer(
            x
        )


        # Predicted class

        predicted_index = tf.argmax(
            predictions[0]
        )

        predicted_score = predictions[
            0,
            predicted_index
        ]


    # --------------------------------------
    # Calculate gradients
    # --------------------------------------

    grads = tape.gradient(
        predicted_score,
        target_activation
    )


    if grads is None:

        return None


    # --------------------------------------
    # Global average pooling
    # --------------------------------------

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(1, 2)
    )

    feature_maps = target_activation[0]

    pooled_grads = pooled_grads[0]


    # --------------------------------------
    # Generate heatmap
    # --------------------------------------

    heatmap = tf.reduce_sum(
        feature_maps * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    heatmap = heatmap / (
        tf.reduce_max(heatmap) + 1e-8
    )


    # --------------------------------------
    # Convert heatmap to image
    # --------------------------------------

    heatmap = heatmap.numpy()

    heatmap = np.uint8(
        heatmap * 255
    )

    heatmap_image = Image.fromarray(
        heatmap
    )

    heatmap_image = heatmap_image.resize(
        (224, 224)
    )


    # --------------------------------------
    # Create overlay
    # --------------------------------------

    original = Image.fromarray(
        np.uint8(image_array[0])
    ).convert("RGB")


    # --------------------------------------
    # Create colored heatmap
    # --------------------------------------

    import matplotlib.cm as cm

    colored_heatmap = cm.jet(
        np.array(heatmap_image) / 255.0
    )

    colored_heatmap = np.uint8(
        colored_heatmap[:, :, :3] * 255
    )

    colored_heatmap = Image.fromarray(
        colored_heatmap
    )


    # --------------------------------------
    # Blend original + heatmap
    # --------------------------------------

    overlay = Image.blend(
        original,
        colored_heatmap,
        alpha=0.45
    )


    # --------------------------------------
    # Convert to JPEG Base64
    # --------------------------------------

    buffer = io.BytesIO()

    overlay.save(
        buffer,
        format="JPEG",
        quality=90
    )

    encoded_image = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


    return (
        "data:image/jpeg;base64,"
        + encoded_image
    )


# ==========================================
# PREDICTION API
# ==========================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # --------------------------------------
    # Read uploaded image
    # --------------------------------------

    image_data = await file.read()


    # --------------------------------------
    # Open image
    # --------------------------------------

    image = Image.open(
        io.BytesIO(image_data)
    ).convert("RGB")


    # --------------------------------------
    # Resize
    # --------------------------------------

    image = image.resize(
        (224, 224)
    )


    # --------------------------------------
    # NumPy array
    # --------------------------------------

    image_array = np.array(
        image,
        dtype=np.float32
    )


    # --------------------------------------
    # Add batch dimension
    # --------------------------------------

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    # ======================================
    # AI PREDICTION
    # ======================================

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]


    # ======================================
    # TOP 3 PREDICTIONS
    # ======================================

    top_indices = np.argsort(
        predictions
    )[-3:][::-1]


    results = []


    for index in top_indices:

        results.append({

            "class":
                class_names[index],

            "confidence":
                round(
                    float(
                        predictions[index] * 100
                    ),
                    2
                )
        })


    # ======================================
    # BEST PREDICTION
    # ======================================

    best_index = top_indices[0]

    prediction_name = class_names[
        best_index
    ]

    confidence = round(
        float(
            predictions[best_index] * 100
        ),
        2
    )
    # ======================================
    # UNKNOWN / UNCERTAIN PREDICTION GUARD
    # ======================================

    UNKNOWN_THRESHOLD = 50.0

    is_unknown = confidence < UNKNOWN_THRESHOLD

    if is_unknown:
        prediction_name = "Leaf Not in Database"
        results = []


    # ======================================
    # AI CONFIDENCE GUARD
    # ======================================
    if is_unknown:

        confidence_guard = {
        "confidence_level": "Low",
        "prediction_reliable": False,
        "uncertainty_message":
            "Leaf Not in Database. "
            "The AI could not confidently identify "
            "this leaf. Please upload a clearer image "
            "or consult an agricultural expert."
    }

    else:


        confidence_guard = get_confidence_guard(
        confidence
    )


    # ======================================
    # HEALTH + SEVERITY
    # ======================================

    
    if is_unknown:

        health_score = None

        severity = "Unable to Assess"

        severity_description = (
            "Leaf Not in Database. "
            "The AI could not confidently identify "
            "this leaf. Its health condition cannot "
            "be reliably determined by this model."
        )

        # UNKNOWN LEAF ADVISORY

        advisory = {
            "status": "Unknown Leaf",
            "description": (
                "This leaf could not be reliably "
                "identified by the current AI model."
            ),
            "advice": [
                "Upload a clear image of the leaf.",
                "Capture the leaf in natural lighting.",
                "Consult an agricultural expert "
                "if visible damage is present."
            ]
        }

        # NO DISEASE-SPECIFIC TREATMENT

        treatment = None

    else:

        (
            health_score,
            severity,
            severity_description
        ) = calculate_health_and_severity(
            prediction_name,
            confidence
        )

        # FARM ADVISORY

        advisory = get_advisory(
            prediction_name
        )

        # TREATMENT RECOMMENDATION

        treatment = get_treatment(
            prediction_name
        )


    # ======================================
    # GENERATE GRAD-CAM
    # ======================================

    print(
        "Generating Grad-CAM..."
    )

    gradcam_image = generate_gradcam(
        image_array
    )


    # ======================================
    # FARM ADVISORY
    # ======================================

    advisory = get_advisory(
        prediction_name
    )


    # ======================================
    # TREATMENT RECOMMENDATION
    # ======================================

    treatment = get_treatment(
        prediction_name
    )


    # ======================================
    # GENERATE GRAD-CAM
    # ======================================

    print(
        "Generating Grad-CAM..."
    )

    gradcam_image = generate_gradcam(
        image_array
    )


    # ======================================
    # FINAL RESPONSE
    # ======================================

    return {

        # -------------------------------
        # Prediction
        # -------------------------------

        "prediction":
            prediction_name,

        "confidence":
            confidence,


        # -------------------------------
        # Confidence Guard
        # -------------------------------

        "confidence_level":
            confidence_guard[
                "confidence_level"
            ],

        "prediction_reliable":
            confidence_guard[
                "prediction_reliable"
            ],

        "uncertainty_message":
            confidence_guard[
                "uncertainty_message"
            ],


        # -------------------------------
        # Existing Advisory
        # -------------------------------

        "status":
            advisory["status"],

        "description":
            advisory["description"],

        "advice":
            advisory["advice"],


        # -------------------------------
        # Treatment
        # -------------------------------

        "treatment":
            treatment,


        # -------------------------------
        # Top Predictions
        # -------------------------------

        "top_predictions":
            results,


        # -------------------------------
        # Health + Severity
        # -------------------------------

        "health_score":
            health_score,

        "severity":
            severity,

        "severity_description":
            severity_description,


        # -------------------------------
        # Grad-CAM
        # -------------------------------

        "gradcam":
            gradcam_image
    }