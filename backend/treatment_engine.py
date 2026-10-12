# AgriSense AI - Strict Treatment Engine v3
# One schema only. No hard-coded treatment records.

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "treatment_database.json")

print("Loading AgriSense treatment database...")
try:
    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        TREATMENT_DATA = json.load(file)
    print(f"Treatment database loaded successfully! Disease classes: {len(TREATMENT_DATA)}")
except Exception as error:
    print("ERROR: Could not load treatment database.")
    print(error)
    TREATMENT_DATA = {}


def _list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_treatment(class_name: str) -> dict:
    item = TREATMENT_DATA.get(class_name)

    # Healthy classes are intentionally excluded from the disease database.
    # Handle them explicitly so a healthy prediction still gets a clean response.
    if class_name.lower().endswith("___healthy"):
        return {
            "available": True,
            "crop": class_name.split("___")[0].replace("_", " "),
            "condition": "Healthy",
            "condition_type": "healthy",
            "direct_cure_available": False,
            "treatment_summary": "No disease treatment is indicated for a healthy prediction.",
            "cultural_management": [
                "Continue routine scouting, appropriate irrigation, balanced nutrition and crop sanitation."
            ],
            "chemical_recommendations": [],
            "chemical_treatment": [],
            "biological_treatment": [],
            "fertilizer_nutrition": "Use soil-test-based balanced nutrition; do not apply fertilizer as a disease cure.",
            "application_guidance": [
                "No pesticide application is indicated from a healthy AI classification alone."
            ],
            "safety": ["Follow local crop-management and product-label guidance."],
            "do_not_do": ["Do not apply pesticides unnecessarily to a healthy crop."],
            "verification_status": "healthy_no_treatment",
            "sources": [],
            "source_policy": "Routine crop management should follow local agricultural/KVK guidance."
        }

    if item is None:
        return {
            "available": False,
            "crop": "",
            "condition": class_name,
            "condition_type": "unknown",
            "direct_cure_available": False,
            "treatment_summary": "No verified disease-treatment record is available for this prediction.",
            "cultural_management": [],
            "chemical_recommendations": [],
            "chemical_treatment": [],
            "biological_treatment": [],
            "fertilizer_nutrition": "",
            "application_guidance": ["Do not apply a pesticide based only on an AI prediction."],
            "safety": ["Consult a qualified agricultural expert or local KVK."],
            "do_not_do": ["Do not extrapolate a pesticide dose from another crop or disease."],
            "verification_status": "unknown_class",
            "sources": [],
            "source_policy": "Use current registered product labels and local agricultural guidance."
        }

    chemical = _list(item.get("chemical_recommendations"))

    return {
        "available": True,
        "crop": item.get("crop", ""),
        "condition": item.get("condition", class_name),
        "condition_type": item.get("condition_type", "unknown"),
        "direct_cure_available": bool(item.get("direct_cure_available", False)),
        "treatment_summary": item.get("treatment_summary", ""),
        "cultural_management": _list(item.get("cultural_management")),
        "chemical_recommendations": chemical,
        "chemical_treatment": chemical,
        "biological_treatment": _list(item.get("biological_treatment")),
        "fertilizer_nutrition": item.get("fertilizer_nutrition", ""),
        "application_guidance": _list(item.get("application_guidance")),
        "safety": _list(item.get("safety")),
        "do_not_do": _list(item.get("do_not_do")),
        "verification_status": item.get("verification_status", "not_verified"),
        "sources": _list(item.get("sources")),
        "source_policy": item.get("source_policy", "Use current registered product labels and local agricultural guidance."),
        "safety_rule": (
            "Chemical recommendations are informational and must be used only when the current registered product label covers the exact crop and target condition. Follow the label, PPE, re-entry interval and PHI. Do not mix products unless the label or qualified agricultural adviser permits it."
        )
    }


def get_treatment_dataset_info() -> dict:
    return {
        "dataset_loaded": len(TREATMENT_DATA) == 26,
        "disease_classes": len(TREATMENT_DATA),
        "database_file": os.path.basename(DATABASE_PATH),
        "healthy_classes_in_database": False
    }
