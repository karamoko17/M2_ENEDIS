from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# URL Dropbox en mode téléchargement direct
DROPBOX_URL = 'https://www.dropbox.com/scl/fi/ek391mb0isa6oz9bg2vd5/data69rhone.csv?rlkey=zlle9fo6ia4h42inpj3de945c&st=vhc7fmev&dl=1'

def load_data_from_dropbox(url):
    # Charge les données du fichier CSV depuis Dropbox
    df = pd.read_csv(url)
    return df

# Charger les données une seule fois
df = load_data_from_dropbox(DROPBOX_URL)

@app.route('/data', methods=['GET'])
def get_data():
    # Convertit les données en dictionnaire pour un retour JSON
    data = df.to_dict(orient='records')
    return jsonify(data
                   )

if __name__ == '__main__':
    app.run(debug=True)