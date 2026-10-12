from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
import numpy as np
import json
from PIL import Image
import io

from backend.advisory import get_advisory


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="AgriSense AI",
    description="AI-powered crop disease detection and farm advisory system",
    version="1.0"
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

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open(CLASS_PATH, "r") as file:
    class_names = json.load(file)

print(f"Total classes: {len(class_names)}")


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AgriSense AI Backend is running",
        "model": "EfficientNetB0",
        "classes": len(class_names)
    }


# ==========================================
# PREDICTION API
# ==========================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

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
    # Resize image
    # --------------------------------------

    image = image.resize(
        (224, 224)
    )


    # --------------------------------------
    # Convert image to NumPy array
    # --------------------------------------

    image_array = np.array(image)


    # --------------------------------------
    # Add batch dimension
    # --------------------------------------

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    # --------------------------------------
    # AI MODEL PREDICTION
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

            "class": class_names[index],

            "confidence": round(
                float(predictions[index] * 100),
                2
            )

        })


    # --------------------------------------
    # BEST PREDICTION
    # --------------------------------------

    best_index = top_indices[0]

    prediction_name = class_names[best_index]

    confidence = round(
        float(predictions[best_index] * 100),
        2
    )


    # --------------------------------------
    # FARM ADVISORY
    # --------------------------------------

    advisory = get_advisory(
        prediction_name
    )


    # --------------------------------------
    # FINAL RESPONSE
    # --------------------------------------

    return {

        "prediction": prediction_name,

        "confidence": confidence,

        "status": advisory["status"],

        "description": advisory["description"],

        "advice": advisory["advice"],

        "top_predictions": results

    }