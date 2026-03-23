import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
import base64
from flask import Blueprint, request, jsonify
from io import BytesIO

bp1 = Blueprint('main', __name__, url_prefix='/main')

# Charger le modèle Random Forest (SMOTE)
with open("models/rf_model_smote.pkl", "rb") as file:
    best_rf_smote = pickle.load(file)

# Charger le scaler SMOTE
with open("models/scaler_smote.pkl", "rb") as file:
    scaler = pickle.load(file)

# Colonnes utilisées par le modèle
FEATURES = [
    "age", "anaemia", "creatinine_phosphokinase", "diabetes", "ejection_fraction",
    "high_blood_pressure", "platelets", "serum_creatinine", "serum_sodium", 
    "sex", "smoking", "time"
]

def preprocess_input(form_data):
    """Prépare les données pour la prédiction"""
    df = pd.DataFrame([form_data], columns=FEATURES)
    df = df.astype(float)  # Convertit toutes les valeurs en numérique
    # Normaliser avec le scaler SMOTE
    df_scaled = scaler.transform(df)
    # Reconvertir en DataFrame pour conserver les noms de colonnes
    df_scaled = pd.DataFrame(df_scaled, columns=FEATURES)
    return df_scaled

@bp1.route('/api/make_prediction', methods=['POST'])
def make_prediction():
    try:
        # Récupération des données JSON envoyées
        form_data = request.get_json()
        print("Données reçues pour prédiction:", form_data)

        # Vérification : toutes les colonnes nécessaires sont-elles présentes ?
        for feature in FEATURES:
            if feature not in form_data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400

        # Prétraitement des données
        input_data = preprocess_input(form_data)

        # Prédiction
        pred = best_rf_smote.predict(input_data)[0]         # 0 = Survie, 1 = Décès
        prob = best_rf_smote.predict_proba(input_data)[0][1]  # Probabilité de risque

        # Génération des graphiques SHAP
        shap_plots = explain_prediction_with_shap(input_data, pred)

        # Retour JSON avec les deux images SHAP (Waterfall et Summary)
        return jsonify({
            'prediction': 'Death' if pred == 1 else 'Survival',
            'probability': round(prob, 2),
            'shap_plots': shap_plots
        })

    except Exception as e:
        print("Erreur lors de la prédiction:", str(e))
        return jsonify({'error': str(e)}), 500

# Désactivation du mode GUI de Matplotlib (évite certains problèmes en mode serveur)
plt.switch_backend('Agg')

def explain_prediction_with_shap(input_data, pred_class):
    """Explique la prédiction via un SHAP Waterfall Plot et un Summary Plot (cas binaire)"""
    try:
        print("🟢 Début de l'explication SHAP")
        # Initialisation de l'explainer SHAP pour un modèle d'arbres
        explainer = shap.TreeExplainer(best_rf_smote)
        shap_values = explainer(input_data)
        print("✅ SHAP values calculés avec succès")
        
        # Pour le waterfall plot, on extrait les SHAP values de la classe prédite
        shap_vals = shap_values.values[0, :, pred_class]
        base_val = shap_values.base_values[0, pred_class]

        # Construction de l'objet Explanation pour le waterfall plot
        shap_exp = shap.Explanation(
            values=shap_vals,
            base_values=base_val,
            feature_names=FEATURES
        )

        # Générer le Waterfall Plot
        plt.figure(figsize=(10, 6))
        shap.waterfall_plot(shap_exp)
        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches='tight', dpi=150)
        buffer.seek(0)
        waterfall_img = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.clf()  # Réinitialise la figure

        # Pour le Summary Plot, SHAP attend un tableau 2D (nb_samples x nb_features)
        # Ici, on extrait les valeurs pour la classe prédite (même pour un seul échantillon)
        shap_vals_summary = shap_values.values[:, :, pred_class]
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_vals_summary, input_data, plot_type="dot", show=False)
        buffer2 = BytesIO()
        plt.savefig(buffer2, format="png", bbox_inches='tight', dpi=150)
        buffer2.seek(0)
        summary_img = base64.b64encode(buffer2.read()).decode("utf-8")
        buffer2.close()
        plt.clf()

        print("✅ Images SHAP générées avec succès")
        return {
            "waterfall_plot": f"data:image/png;base64,{waterfall_img}",
            "summary_plot": f"data:image/png;base64,{summary_img}"
        }

    except Exception as e:
        print(f"❌ Erreur SHAP : {str(e)}")
        return None
