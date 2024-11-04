import streamlit as st
import requests
api_url = "https://performance-energetique-server.onrender.com/api"
# Définir une fonction pour faire une requête GET à l'endpoint de l'API Flask
def get_data(api_url):
    api_url = api_url + "/data"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Erreur lors de la récupération des données.")
        return None

# Créer un bouton pour déclencher la requête API
if st.button("Obtenir les données"):
    data = get_data(api_url)
    if data:
        # Afficher les données dans l'application Streamlit
        st.write(data)

# Template "Hello"
st.title("Bienvenue dans l'application Streamlit!")
st.write("Cette application vous permet de récupérer des données depuis une API Flask.")