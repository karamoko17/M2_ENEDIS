# app.py
import streamlit as st
from pages_uses import accueil, cartographie, prediction, evolution, navbar, topbar, classification
import requests
import time

# URL du serveur
url = "https://performance-energetique-server.onrender.com/"

def check_server_status(url, retries=100, delay=60):
    """Vérifie si le serveur est prêt (renvoie HTTP 200)."""
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(delay)
    return False

# Vérifiez le serveur avant de lancer l'application Streamlit
if check_server_status(url):
    # Initialisation de l'état de la page si nécessaire
    if 'page' not in st.session_state:
        st.session_state.page = 'Accueil'  # Page par défaut

    # Afficher le menu latéral
    # topbar.show_topbar
    navbar.show_menu()

    # Affichage du contenu en fonction de la page sélectionnée
    if st.session_state.page == 'Accueil':
        accueil.show()
    elif st.session_state.page == 'Cartographie':
        cartographie.show()
    elif st.session_state.page == 'Prédiction':
        prediction.show()
    elif st.session_state.page == 'Classification':
        classification.show()
    elif st.session_state.page == 'Évolution':
        evolution.show()
else:
    st.error("Le serveur n'est pas disponible. Veuillez réessayer plus tard.")
