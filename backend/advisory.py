def get_advisory(prediction):

    prediction_lower = prediction.lower()

    if "healthy" in prediction_lower:
        return {
            "status": "Healthy",
            "description": "No major disease pattern was detected in the uploaded leaf.",
            "advice": [
                "Continue regular crop monitoring.",
                "Maintain proper irrigation and soil moisture.",
                "Maintain good field hygiene.",
                "Monitor the crop regularly for early signs of disease or pests."
            ]
        }

    if "early_blight" in prediction_lower:
        return {
            "status": "Disease Detected",
            "description": "The AI detected a pattern associated with early blight.",
            "advice": [
                "Remove severely affected leaves where practical.",
                "Improve air circulation around plants.",
                "Avoid unnecessary overhead irrigation.",
                "Monitor nearby plants for similar symptoms."
            ]
        }

    if "late_blight" in prediction_lower:
        return {
            "status": "Disease Detected",
            "description": "The AI detected a pattern associated with late blight.",
            "advice": [
                "Remove severely affected plant material where appropriate.",
                "Improve air circulation around plants.",
                "Avoid unnecessary overhead irrigation.",
                "Monitor surrounding plants frequently."
            ]
        }

    if "powdery_mildew" in prediction_lower:
        return {
            "status": "Disease Detected",
            "description": "The AI detected a pattern associated with powdery mildew.",
            "advice": [
                "Improve air circulation around the crop.",
                "Avoid excessive humidity around plant foliage.",
                "Remove severely affected leaves where appropriate.",
                "Monitor nearby plants for spreading symptoms."
            ]
        }

    if "rust" in prediction_lower:
        return {
            "status": "Disease Detected",
            "description": "The AI detected a pattern associated with rust disease.",
            "advice": [
                "Remove severely affected plant material where practical.",
                "Improve crop ventilation.",
                "Avoid unnecessary leaf wetness.",
                "Continue regular disease monitoring."
            ]
        }

    return {
        "status": "Disease Detected",
        "description": "The AI detected a disease pattern in the uploaded leaf.",
        "advice": [
            "Inspect surrounding plants for similar symptoms.",
            "Remove severely affected plant material where appropriate.",
            "Maintain proper irrigation and field hygiene.",
            "Monitor the crop regularly.",
            "Consult a local agricultural expert before applying treatment."
        ]
    }