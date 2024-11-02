from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
 




app = Flask(__name__)


 
# Load the pre-trained model
model = joblib.load('./Modèle/random_forest_regressor.pkl')
modelClassification =  joblib.load('./Modèle/pipeline.pkl')




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
def get_data():
    data = {"message": "Hello, World!", "data": [1, 2, 3, 4, 5]}
    return jsonify(data)

@app.route("/api/submit", methods=["POST"])
def submit_data():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"status": "success", "message": "Data received successfully!"})



@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()

    # Convert the data into a pandas DataFrame
    input_data = pd.DataFrame(data, index=[0])
    input_data.to_csv('mydata.csv')
    # Ensure the DataFrame has the correct columns
    if not all(col in input_data.columns for col in ls_variables_explicatives):
        return jsonify({'error': 'Invalid input features'}), 400

    # Make the prediction
    prediction = model.predict(input_data[ls_variables_explicatives])

    # Return the prediction as JSON
    return jsonify({'prediction': prediction[0]})


@app.route('/classification', methods=['POST'])
def classification():
    
    # # Get the JSON data from the request
    data = request.get_json()
    
    # # Convert the data into a pandas DataFrame
    input_data = pd.DataFrame(data, index=[0])
    # input_data.to_csv('mydata.csv')
    # # Ensure the DataFrame has the correct columns
    if not all(col in input_data.columns for col in ls_variables_explicatives_classification):
        return jsonify({'error': 'Invalid input features'}), 400
    


    # # Make the prediction
    prediction = modelClassification.predict(input_data[ls_variables_explicatives_classification])
    # print(input_data)
    # print(prediction)

    # # Return the prediction as JSON
    return jsonify({'classification': prediction[0]})
    # return jsonify({'classification': 'zazeaz'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,  debug=True)
