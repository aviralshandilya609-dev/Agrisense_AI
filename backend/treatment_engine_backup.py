# AgriSense AI - 38 Class Treatment Engine
# ---------------------------------------------------------
# This database covers all 38 PlantVillage classes used
# by the AgriSense AI model.
#
# Chemical recommendations are included only where a
# source-verified recommendation is available.
#
# IMPORTANT:
# Do not extend a chemical recommendation to another
# crop/disease without checking the current registered
# Indian product label and local agricultural/KVK guidance.
# ---------------------------------------------------------


TREATMENT_DATA = {

    # =====================================================
    # APPLE
    # =====================================================

    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple scab",
        "condition_type": "fungal_disease",

        "management": (
            "Remove fallen infected leaves, maintain orchard sanitation, "
            "prune for better airflow, and monitor during wet periods."
        ),

        "chemical_recommendations": [
            {
                "active_ingredient": "Captan 50% WP",
                "product_type": "Fungicide",
                "dose": "2.5 kg/ha",
                "application_method": "Foliar spray",
                "water_volume": "750–1000 L/ha",
                "phi_days": None,
                "frequency": (
                    "Use according to the current registered label "
                    "and local advisory."
                ),
                "source": "PPQS IPM Package of Practices for Apple",
                "source_url": (
                    "https://ppqs.gov.in/sites/default/files/"
                    "pop-apple_final-_08.12.2022.pdf"
                ),
                "verification_status": "source_verified_ipm"
            }
        ],

        "verification_status": "verified_chemical_entries"
    },


    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black rot",
        "condition_type": "fungal_disease",

        "management": (
            "Prune and destroy dead or mummified plant material, "
            "remove infected fruit and cankers, and improve orchard "
            "sanitation and airflow."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_verified_chemical_label_check_required"
    },


    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar apple rust",
        "condition_type": "fungal_disease",

        "management": (
            "Remove or manage nearby alternate hosts where practical, "
            "prune affected material, improve airflow, and monitor "
            "from early leaf development."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Continue orchard sanitation, "
            "balanced nutrition, irrigation management and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # BLUEBERRY
    # =====================================================

    "Blueberry___healthy": {
        "crop": "Blueberry",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain appropriate irrigation, "
            "nutrition, drainage, sanitation and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # CHERRY
    # =====================================================

    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain sanitation, pruning, "
            "balanced nutrition and routine monitoring."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry",
        "condition": "Powdery mildew",
        "condition_type": "fungal_disease",

        "management": (
            "Improve canopy airflow, remove severely affected tissue "
            "where practical, avoid excessive nitrogen, and monitor "
            "new growth."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    # =====================================================
    # CORN / MAIZE
    # =====================================================

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (maize)",
        "condition": "Cercospora leaf spot / gray leaf spot",
        "condition_type": "fungal_disease",

        "management": (
            "Use crop rotation where feasible, manage infected residue, "
            "maintain balanced nutrition and scout lower leaves for "
            "early symptoms."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (maize)",
        "condition": "Common rust",
        "condition_type": "fungal_disease",

        "management": (
            "Use resistant/tolerant varieties where available, "
            "scout regularly, maintain balanced nutrition and avoid "
            "unnecessary prolonged leaf wetness."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Corn_(maize)___healthy": {
        "crop": "Corn (maize)",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Continue balanced "
            "fertilization, irrigation and regular scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (maize)",
        "condition": "Northern leaf blight",
        "condition_type": "fungal_disease",

        "management": (
            "Use resistant varieties, rotate crops, manage infected "
            "residue and scout regularly, especially under humid conditions."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    # =====================================================
    # GRAPE
    # =====================================================

    "Grape___Black_rot": {
        "crop": "Grape",
        "condition": "Black rot",
        "condition_type": "fungal_disease",

        "management": (
            "Remove infected berries and plant debris, improve canopy "
            "ventilation, avoid prolonged leaf wetness and maintain "
            "vineyard sanitation."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "condition": "Esca (black measles)",
        "condition_type": "fungal_disease_complex",

        "management": (
            "Remove and destroy severely affected wood, use clean "
            "planting material, disinfect pruning tools and manage "
            "pruning wounds to reduce infection risk."
        ),

        "chemical_recommendations": [],

        "verification_status": "management_guidance_no_direct_cure"
    },


    "Grape___healthy": {
        "crop": "Grape",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain canopy management, "
            "balanced nutrition, irrigation and vineyard sanitation."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "condition": "Leaf blight (Isariopsis leaf spot)",
        "condition_type": "fungal_disease",

        "management": (
            "Remove infected leaves and debris, improve canopy ventilation "
            "and monitor during humid periods."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    # =====================================================
    # ORANGE
    # =====================================================

    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange",
        "condition": "Huanglongbing (citrus greening)",
        "condition_type": "bacterial_like_systemic_disease",

        "management": (
            "There is no curative pesticide treatment for an infected tree. "
            "Use certified disease-free planting material, remove severely "
            "infected trees where recommended, and manage the psyllid vector "
            "through an authorised citrus IPM programme."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "no_direct_cure_vector_management"
    },


    # =====================================================
    # PEACH
    # =====================================================

    "Peach___Bacterial_spot": {
        "crop": "Peach",
        "condition": "Bacterial spot",
        "condition_type": "bacterial_disease",

        "management": (
            "Use clean planting material, prune for airflow, remove "
            "severely affected material, avoid unnecessary leaf wetness "
            "and follow local bacterial-disease IPM guidance."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Peach___healthy": {
        "crop": "Peach",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain orchard sanitation, "
            "pruning, balanced nutrition and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # BELL PEPPER
    # =====================================================

    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell pepper",
        "condition": "Bacterial spot",
        "condition_type": "bacterial_disease",

        "management": (
            "Use disease-free seed/transplants, avoid overhead irrigation, "
            "remove infected plant material, sanitize tools and improve "
            "field sanitation."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Pepper,_bell___healthy": {
        "crop": "Bell pepper",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain balanced nutrition, "
            "irrigation, drainage and regular scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # POTATO
    # =====================================================

    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early blight",
        "condition_type": "fungal_disease",

        "management": (
            "Use healthy seed, rotate crops, remove infected residue, "
            "maintain plant vigor and avoid prolonged leaf wetness."
        ),

        "chemical_recommendations": [
            {
                "active_ingredient": "Mancozeb 75% WP",
                "product_type": "Protective fungicide",
                "dose": "600–800 g in 300 L water/acre",
                "application_method": "Foliar spray",
                "water_volume": "300 L/acre",
                "phi_days": None,
                "frequency": (
                    "Follow the current registered label and local advisory."
                ),
                "source": "PPQS AESA-based IPM – Potato",
                "source_url": (
                    "https://ppqs.gov.in/sites/default/files/potato.pdf"
                ),
                "verification_status": "source_verified_ipm"
            }
        ],

        "verification_status": "verified_chemical_entries"
    },


    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Use healthy seed tubers, "
            "balanced nutrition, proper irrigation and regular scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late blight",
        "condition_type": "oomycete_disease",

        "management": (
            "Use healthy seed, remove volunteer/infected plants, improve "
            "field ventilation and use disease forecasting where available. "
            "Late blight risk increases under cool, wet conditions."
        ),

        "chemical_recommendations": [
            {
                "active_ingredient": "Registered late-blight fungicide",
                "product_type": "Fungicide",
                "dose": (
                    "Use the current registered product label "
                    "for potato late blight"
                ),
                "application_method": "Foliar spray",
                "water_volume": "As per current label",
                "phi_days": None,
                "frequency": (
                    "Follow the current label and local agriculture/KVK "
                    "advisory; rotate modes of action."
                ),
                "source": "PPQS AESA-based IPM – Potato",
                "source_url": (
                    "https://ppqs.gov.in/sites/default/files/potato.pdf"
                ),
                "verification_status":
                    "source_verified_ipm_label_required"
            }
        ],

        "verification_status":
            "verified_source_label_required"
    },


    # =====================================================
    # RASPBERRY
    # =====================================================

    "Raspberry___healthy": {
        "crop": "Raspberry",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain sanitation, "
            "pruning, irrigation and regular scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # SOYBEAN
    # =====================================================

    "Soybean___healthy": {
        "crop": "Soybean",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain crop sanitation, "
            "balanced nutrition, appropriate irrigation and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    # =====================================================
    # SQUASH
    # =====================================================

    "Squash___Powdery_mildew": {
        "crop": "Squash",
        "condition": "Powdery mildew",
        "condition_type": "fungal_disease",

        "management": (
            "Improve airflow, avoid excessive nitrogen, remove heavily "
            "affected leaves where practical and reduce prolonged "
            "humid canopy conditions."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    # =====================================================
    # STRAWBERRY
    # =====================================================

    "Strawberry___healthy": {
        "crop": "Strawberry",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Maintain clean planting "
            "material, good drainage, irrigation management and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "condition": "Leaf scorch",
        "condition_type": "fungal_disease",

        "management": (
            "Remove heavily infected leaves, improve field sanitation "
            "and airflow, avoid prolonged leaf wetness and use clean "
            "planting material."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    # =====================================================
    # TOMATO
    # =====================================================

    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "condition": "Bacterial spot",
        "condition_type": "bacterial_disease",

        "management": (
            "Use disease-free seed/transplants, avoid overhead irrigation, "
            "remove infected debris, sanitize tools and reduce leaf wetness."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early blight",
        "condition_type": "fungal_disease",

        "management": (
            "Remove infected leaves and debris, use crop rotation, "
            "improve airflow, avoid overhead irrigation and monitor "
            "lower leaves for progression."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy",
        "condition_type": "healthy",

        "management": (
            "No disease treatment indicated. Continue balanced nutrition, "
            "irrigation, sanitation and routine scouting."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_treatment_needed"
    },


    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late blight",
        "condition_type": "oomycete_disease",

        "management": (
            "Scout frequently, reduce leaf wetness, remove severely "
            "affected material and follow local disease-management timing."
        ),

        "chemical_recommendations": [

            {
                "active_ingredient": "Azoxystrobin 23% SC",
                "product_type": "Systemic fungicide",
                "dose": "200 ml in 200 L water/acre",
                "application_method": "Foliar spray",
                "water_volume": "200 L/acre",
                "phi_days": None,
                "frequency": (
                    "PPQS tomato IPM lists this for late blight; "
                    "follow the current label."
                ),
                "source":
                    "PPQS/DPPQ&S AESA-based IPM Package – Tomato",
                "source_url":
                    "https://ppqs.gov.in/sites/default/files/tomato.pdf",
                "verification_status": "source_verified_ipm"
            },

            {
                "active_ingredient": "Mandipropamid 23.4% SC",
                "product_type": "Fungicide",
                "dose": "0.08% formulation",
                "application_method": "Foliar spray",
                "water_volume": "500 L/ha",
                "phi_days": 5,
                "frequency": (
                    "First spray preventively or at disease initiation; "
                    "follow the current registered label for repeat interval "
                    "and maximum applications."
                ),
                "source": "PPQS primary package label",
                "source_url":
                    "https://ppqs.gov.in/sites/default/files/"
                    "mandipropamid_23.4_sc93fsyngenta_india_limited_1.pdf",
                "verification_status": "label_verified"
            }
        ],

        "verification_status": "verified_chemical_entries"
    },


    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "condition": "Leaf mold",
        "condition_type": "fungal_disease",

        "management": (
            "Improve ventilation, reduce humidity and leaf wetness, "
            "remove infected lower leaves and maintain greenhouse/"
            "field sanitation."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "condition": "Septoria leaf spot",
        "condition_type": "fungal_disease",

        "management": (
            "Remove infected leaves and crop debris, rotate crops, "
            "improve airflow, avoid overhead irrigation and sanitize tools."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "condition": "Two-spotted spider mites",
        "condition_type": "mite_pest",

        "management": (
            "Inspect leaf undersides, reduce plant stress, conserve "
            "beneficial predatory mites/insects and use an authorised "
            "miticide only when the pest and crop are confirmed."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "condition": "Target spot",
        "condition_type": "fungal_disease",

        "management": (
            "Remove infected leaves and debris, improve airflow, "
            "reduce leaf wetness and use crop sanitation and rotation."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "management_guidance_chemical_label_check_required"
    },


    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "condition": "Tomato mosaic virus",
        "condition_type": "viral_disease",

        "management": (
            "There is no direct chemical cure for an infected plant. "
            "Remove severely infected plants, use clean seed/transplants, "
            "disinfect tools and hands, and prevent mechanical spread."
        ),

        "chemical_recommendations": [],

        "verification_status": "no_direct_cure_management"
    },


    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Tomato yellow leaf curl virus",
        "condition_type": "viral_disease",

        "management": (
            "There is no direct chemical cure for an infected plant. "
            "Remove severely infected plants where recommended, use "
            "clean planting material and manage the whitefly vector "
            "through an authorised IPM programme."
        ),

        "chemical_recommendations": [],

        "verification_status":
            "no_direct_cure_vector_management"
    }
}


# =========================================================
# MAIN FUNCTION USED BY FASTAPI
# =========================================================

def get_treatment(class_name: str) -> dict:

    item = TREATMENT_DATA.get(class_name)

    # -----------------------------------------------------
    # Unknown class safety fallback
    # -----------------------------------------------------

    if item is None:

        return {
            "available": False,

            "crop": "",

            "condition": class_name,

            "condition_type": "unknown",

            "management": (
                "No treatment record is available for this model class. "
                "Please verify the diagnosis with an agricultural expert."
            ),

            "cultural_management": (
                "No verified management record available."
            ),

            "chemical_recommendations": [],

            "verification_status": "unknown_class"
        }


    # -----------------------------------------------------
    # Return treatment information
    # -----------------------------------------------------

    return {

        "available": True,

        "crop": item["crop"],

        "condition": item["condition"],

        "condition_type": item["condition_type"],

        "cultural_management": item["management"],

        "chemical_recommendations":
            item["chemical_recommendations"],

        "verification_status":
            item["verification_status"],

        "safety_rule": (
            "Chemical recommendations must be used only for the exact "
            "crop and target condition covered by the current registered "
            "product label. Follow the label, PPE, PHI and local "
            "agricultural/KVK guidance. Do not mix products unless the "
            "label or authorised agronomist explicitly permits it."
        )
    }