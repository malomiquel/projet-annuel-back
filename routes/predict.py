from flask import request, jsonify
from flasgger import swag_from
import pandas as pd
import joblib

# Chargez le modèle
model = joblib.load('./ML/sepsis_model.pkl')

def predict_routes(app):
    @app.route('/health_check')
    @swag_from({
        'responses': {
            200: {
                'description': 'Health check',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'health_check': {'type': 'boolean'}
                    }
                }
            }
        }
    })
    def health_check():
        return {'health_check': True}

    @app.route('/predict/patient', methods=['POST'])
    @swag_from({
        'parameters': [
            {
                'name': field,
                'in': 'formData',
                'type': 'integer',
                'required': 'true',
            } for field in ['PRG', 'PL', 'PR', 'SK', 'TS', 'M11', 'BD2', 'Age', 'Insurance']
        ],
        'responses': {
            200: {
                'description': 'Prediction',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'prediction': {'type': 'string'},
                        'form_data': {'type': 'object'},
                    }
                }
            },
            400: {
                'description': 'Bad Request',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                    }
                }
            }
        }
    })
    def predict():
        fields = ['PRG', 'PL', 'PR', 'SK', 'TS',
                  'M11', 'BD2', 'Age', 'Insurance']
        data_list = []
        form_data = {}

        for field in fields:
            value = request.get_json()[field]
            form_data[field] = value if value else ""
            if not value:
                # Si le champ est manquant, retourner une erreur
                return jsonify({'error': f"Le champ {field} est obligatoire."}), 400
            try:
                int_value = int(value)
            except ValueError:
                # Si la valeur du champ n'est pas un entier, retourner une erreur
                return jsonify({'error': f"La valeur du champ {field} doit être un entier."}), 400
            data_list.append(int_value)

        # Créer un DataFrame à partir des données
        data = pd.DataFrame([data_list])

        # Effectuer des prédictions avec le modèle
        predictions = model.predict(data)

        # Retourner la réponse au format JSON
        return jsonify({"prediction": predictions[0], "form_data": form_data})