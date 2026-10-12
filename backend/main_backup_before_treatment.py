from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
import numpy as np
import json
import io
import base64

from PIL import Image

from backend.advisory import get_advisory


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AgriSense AI",
    description="AI-powered crop disease detection and farm advisory system",
    version="1.3"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# MODEL PATHS
# ==========================================

MODEL_PATH = "ml_model/agrisense_model.keras"
CLASS_PATH = "ml_model/class_names.json"


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading AgriSense AI model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

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

    # --------------------------------------
    # HIGH CONFIDENCE
    # --------------------------------------

    if confidence >= 70:

        return {

            "confidence_level":
                "High",

            "prediction_reliable":
                True,

            "uncertainty_message":
                "The AI has high confidence in this prediction."

        }


    # --------------------------------------
    # MODERATE CONFIDENCE
    # --------------------------------------

    elif confidence >= 50:

        return {

            "confidence_level":
                "Moderate",

            "prediction_reliable":
                True,

            "uncertainty_message":
                "The AI has moderate confidence. "
                "Verify the result with a clear image "
                "and visual inspection."

        }


    # --------------------------------------
    # LOW CONFIDENCE
    # --------------------------------------

    else:

        return {

            "confidence_level":
                "Low",

            "prediction_reliable":
                False,

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
    Provides an AI-estimated crop health indicator.

    IMPORTANT:
    This is an indicative score based on the
    model's predicted disease confidence.

    It is NOT a measurement of actual field
    damage or crop-loss percentage.
    """

    disease_free_terms = [
        "healthy"
    ]


    prediction_lower = (
        prediction_name.lower()
    )


    # --------------------------------------
    # HEALTHY PREDICTION
    # --------------------------------------

    if any(
        term in prediction_lower
        for term in disease_free_terms
    ):

        health_score = 100.0

        severity = "Healthy"

        severity_description = (
            "The model classified the uploaded "
            "leaf as healthy with the given confidence."
        )

        return (
            health_score,
            severity,
            severity_description
        )


    # --------------------------------------
    # DISEASE PREDICTION
    # --------------------------------------

    if confidence >= 90:

        health_score = 30.0

        severity = "Severe"

        severity_description = (
            "The AI model shows high confidence "
            "in the detected disease. Immediate "
            "inspection and appropriate crop "
            "management are recommended."
        )


    elif confidence >= 70:

        health_score = 50.0

        severity = "Moderate"

        severity_description = (
            "The AI model shows moderate-to-high "
            "confidence in the detected disease. "
            "Inspect the affected area and take "
            "appropriate management action."
        )


    elif confidence >= 50:

        health_score = 70.0

        severity = "Mild"

        severity_description = (
            "The AI model detected a possible "
            "disease with moderate confidence. "
            "Further inspection and monitoring "
            "are recommended."
        )


    else:

        health_score = 85.0

        severity = "Uncertain"

        severity_description = (
            "The model confidence is relatively low. "
            "The result should be treated as uncertain "
            "and the crop should be inspected manually."
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
            True
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


    # --------------------------------------
    # AI PREDICTION
    # --------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]


    # --------------------------------------
    # TOP 3 PREDICTIONS
    # --------------------------------------

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


    # --------------------------------------
    # BEST PREDICTION
    # --------------------------------------

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


    # --------------------------------------
    # AI CONFIDENCE GUARD
    # --------------------------------------

    confidence_guard = get_confidence_guard(
        confidence
    )


    # --------------------------------------
    # HEALTH + SEVERITY
    # --------------------------------------

    (
        health_score,
        severity,
        severity_description
    ) = calculate_health_and_severity(
        prediction_name,
        confidence
    )


    # --------------------------------------
    # FARM ADVISORY
    # --------------------------------------

    advisory = get_advisory(
        prediction_name
    )


    # --------------------------------------
    # GENERATE GRAD-CAM
    # --------------------------------------

    print(
        "Generating Grad-CAM..."
    )


    gradcam_image = generate_gradcam(
        image_array
    )


    # --------------------------------------
    # FINAL RESPONSE
    # --------------------------------------

    return {

        "prediction":
            prediction_name,

        "confidence":
            confidence,


        # F4: Confidence information

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


        # Existing advisory

        "status":
            advisory["status"],


        "description":
            advisory["description"],


        "advice":
            advisory["advice"],


        # Existing top predictions

        "top_predictions":
            results,


        # Existing health + severity

        "health_score":
            health_score,


        "severity":
            severity,


        "severity_description":
            severity_description,


        # Existing Grad-CAM

        "gradcam":
            gradcam_image

    }