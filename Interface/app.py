# app.py
import streamlit as st
from pages_uses import accueil,cartographie, prediction, evolution, navbar, topbar,  classification


# Initialisation de l'état de la page si nécessaire
if 'page' not in st.session_state:
    st.session_state.page = 'Accueil'  # Page par défaut

# Afficher le menu latéral
#topbar.show_topbar
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
