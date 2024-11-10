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


@app.route("/", methods=["GET"])
def home():
    return "Bienvenue sur l'API de prévision de consommation énergétique !Vous pouvez utiliser l'API en envoyant un fichier CSV contenant les données de votre logement à l'URL /predict ou /classification pour obtenir une prédiction de consommation énergétique ou une classification de performance énergétique."


@app.route("/data", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': "Numéro de la page à récupérer"
        },
        {
            'name': 'size',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': "Nombre d'éléments par page"
        }
    ],
    'responses': {
        200: {
            'description': "Récupérer les données paginées",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'page': {'type': 'integer'},
                    'size': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'data': {
                        'type': 'object',
                        'additionalProperties': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_data():
    # Lecture des données
    df = pd.read_csv("./Data/data_carto.csv")

    # Récupération des paramètres de pagination
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)

    # Calcul de l'index de début et de fin
    start = (page - 1) * size
    end = start + size

    # Nombre total de pages
    total_pages = (len(df) + size - 1) // size

    # Extraction des données pour la page demandée
    paginated_data = df[start:end].to_dict(orient="list")

    # Retour des données paginées
    return jsonify({
        'message': "Données récupérées avec succès",
        'page': page,
        'size': size,
        'total_pages': total_pages,
        'data': paginated_data
    })

@app.route('/predict', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'Periode_construction': {'type': 'string', 'enum': ['Avant 1960', '1961 - 1970', '1981 - 1990', '1991 - 2000', '2001 - 2010', 'Après 2010'], 'description': 'Période de construction du bâtiment (de l\'année de construction)'},
                    'Surface_habitable_logement': {'type': 'number', 'description': 'Surface habitable du logement en m²'},
                    'Etiquette_DPE': {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'E', 'F', 'G'], 'description': 'Étiquette de performance énergétique du logement (DPE)'},
                    'Deperditions_enveloppe': {'type': 'number', 'description': 'Déperditions énergétiques totales liées à l\'enveloppe du bâtiment (en kWh)'},
                    'Annee_reception_DPE': {'type': 'number', 'description': 'Année de réception du diagnostic de performance énergétique (DPE)'},
                    'Déperditions_renouvellement_air': {'type': 'number', 'description': 'Déperditions énergétiques dues au renouvellement de l\'air (en kWh)'},
                    'Type_énergie_n°1': {'type': 'string', 'enum': ['Électricité', 'Gaz naturel', 'Charbon', 'Bois – Bûches', 'Réseau de Chauffage urbain', 'Bois – Granulés (pellets) ou briquettes', 'Fioul domestique', "Électricité d'origine renouvelable utilisée dans le bâtiment", 'Bois – Plaquettes d’industrie', 'GPL', 'Bois – Plaquettes forestières', 'Propane'], 'description': 'Type d\'énergie utilisé pour le chauffage'},
                    'Deperditions_baies_vitrées': {'type': 'number', 'description': 'Déperditions énergétiques dues aux baies vitrées (en kWh)'},
                    'Qualité_isolation_murs': {'type': 'string', 'enum': ['insuffisante', 'moyenne', 'bonne', 'très bonne'], 'description': 'Qualité de l\'isolation des murs'},
                    'Déperditions_ponts_thermiques': {'type': 'number', 'description': 'Déperditions énergétiques dues aux ponts thermiques (en kWh)'},
                    'Déperditions_murs': {'type': 'number', 'description': 'Déperditions énergétiques dues aux murs (en kWh)'},
                    'Deperditions_planchers_hauts': {'type': 'number', 'description': 'Déperditions énergétiques dues aux planchers hauts (en kWh)'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': "Valeur prédite",
            'schema': {
                'type': 'object',
                'properties': {
                    'prediction': {'type': 'number', 'description': "Valeur prédite basée sur les entrées"}
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
                'properties': {
                    'Conso_5_usages_par_m²_é_primaire': {'type': 'number', 'description': "Consommation énergétique des 5 usages principaux par m² (énergie primaire) en kWh/m²"},
                    'Emission_GES_5_usages_par_m²': {'type': 'number', 'description': "Émissions de gaz à effet de serre des 5 usages principaux par m² en kgCO2/m²"},
                    'Conso_5_usages/m²_é_finale': {'type': 'number', 'description': "Consommation énergétique des 5 usages principaux par m² (énergie finale) en kWh/m²"},
                    'Conso_chauffage_é_primaire': {'type': 'number', 'description': "Consommation du chauffage (énergie primaire) en kWh"},
                    'Emission_GES_chauffage': {'type': 'number', 'description': "Émissions GES pour le chauffage en kgCO2"},
                    'Coût_chauffage': {'type': 'number', 'description': "Coût du chauffage en euros"},
                    'Besoin_ECS': {'type': 'number', 'description': "Besoin en Eau Chaude Sanitaire (ECS) en kWh"},
                    'Coût_total_5_usages': {'type': 'number', 'description': "Coût total pour 5 usages en euros"},
                    'Conso_5_usages_é_finale_énergie_n°1': {'type': 'number', 'description': "Consommation des 5 usages principaux (énergie finale) pour l'énergie n°1 en kWh"},
                    'Conso_ECS_é_primaire': {'type': 'number', 'description': "Consommation ECS (énergie primaire) en kWh"},
                    'Conso_éclairage_é_finale': {'type': 'number', 'description': "Consommation d'éclairage (énergie finale) en kWh"},
                    'Type_énergie_principale_chauffage': {'type': 'string', 'enum': ['Électricité', 'Gaz naturel', 'Charbon', 'Bois – Bûches', 'Fioul domestique', 'Réseau de Chauffage urbain', 'Bois – Granulés (pellets) ou briquettes', 'Bois – Plaquettes d’industrie', 'GPL', 'Bois – Plaquettes forestières', 'Propane', "Électricité d'origine renouvelable utilisée dans le bâtiment"], 'description': "Type d'énergie utilisée pour le chauffage"},
                    'Conso_chauffage_é_finale': {'type': 'number', 'description': "Consommation chauffage (énergie finale) en kWh"},
                    'Année_construction': {'type': 'integer', 'description': "Année de construction du logement", 'minimum': 1460, 'maximum': 2024},
                    'Surface_habitable_logement': {'type': 'number', 'description': "Surface habitable du logement en m²"}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': "Résultat de la classification",
            'schema': {
                'type': 'object',
                'properties': {
                    'classification': {'type': 'string', 'description': "Classe prédite pour le logement"}
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
