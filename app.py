from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

# Load the pre-trained model
model = joblib.load('./Modèle/random_forest_regressor.pkl')
modelClassification = joblib.load('./Modèle/pipeline.pkl')

# Define the expected input features
ls_variables_explicatives = [
    'Periode_construction',
    'Surface_habitable_logement',
    'Etiquette_DPE',
    'Deperditions_enveloppe',
    'Annee_reception_DPE',
    'Déperditions_renouvellement_air',
    'Type_énergie_n°1',
    'Deperditions_baies_vitrées',
    'Qualité_isolation_murs',
    'Déperditions_ponts_thermiques',
    'Déperditions_murs',
    'Deperditions_planchers_hauts'
]

ls_variables_explicatives_classification = [
    'Conso_5_usages_par_m²_é_primaire',
    'Emission_GES_5_usages_par_m²',
    'Conso_5_usages/m²_é_finale',
    'Conso_chauffage_é_primaire',
    'Emission_GES_chauffage',
    'Coût_chauffage',
    'Besoin_ECS',
    'Surface_habitable_logement',
    'Coût_total_5_usages',
    'Conso_5_usages_é_finale_énergie_n°1',
    'Conso_ECS_é_primaire',
    'Conso_éclairage_é_finale',
    'Type_énergie_principale_chauffage',
    'Conso_chauffage_é_finale',
    'Année_construction'
]

@app.route("/")
def index():
    return "Welcome to my Flask server!"

@app.route("/api/data", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': "Get sample data",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def get_data():
    data = {"message": "Hello, World!", "data": [1, 2, 3, 4, 5]}
    return jsonify(data)

@app.route("/api/submit", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'example': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': "Submit data",
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def submit_data():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"status": "success", "message": "Data received successfully!"})

@app.route('/predict', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {col: {'type': 'number'} for col in ls_variables_explicatives}
            }
        }
    ],
    'responses': {
        200: {
            'description': "Predicted value",
            'schema': {
                'type': 'object',
                'properties': {
                    'prediction': {'type': 'number'}
                }
            }
        }
    }
})
def predict():
    data = request.get_json()
    input_data = pd.DataFrame(data, index=[0])

    if not all(col in input_data.columns for col in ls_variables_explicatives):
        return jsonify({'error': 'Invalid input features'}), 400

    prediction = model.predict(input_data[ls_variables_explicatives])
    return jsonify({'prediction': prediction[0]})

@app.route('/classification', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {col: {'type': 'number'} for col in ls_variables_explicatives_classification}
            }
        }
    ],
    'responses': {
        200: {
            'description': "Classification result",
            'schema': {
                'type': 'object',
                'properties': {
                    'classification': {'type': 'string'}
                }
            }
        }
    }
})
def classification():
    data = request.get_json()
    input_data = pd.DataFrame(data, index=[0])

    if not all(col in input_data.columns for col in ls_variables_explicatives_classification):
        return jsonify({'error': 'Invalid input features'}), 400

    prediction = modelClassification.predict(input_data[ls_variables_explicatives_classification])
    return jsonify({'classification': prediction[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
