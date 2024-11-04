import os
import streamlit as st

def show():
    st.header("À Propos")

    # Construire le chemin de l'image de manière dynamique
    image_path = './Interface/assets/img/dpe.jpg'

    # Vérifier si l'image existe avant de l'afficher
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, width=300)  # Affiche l'image au centre
    else:
        st.error("Image non trouvée : " + image_path)

    # Afficher le texte
    st.write(
        """
        Bienvenue sur l'application GreenTech Solutions, un allié pour optimiser la performance énergétique des logements. 
        L'application analyse les données des habitations pour prédire leur consommation électrique. 
        
        Elle évalue et classe chaque logement selon la classe de Diagnostic de Performance Énergétique (DPE), 
        facilitant ainsi des choix éclairés. Avec une interface intuitive, l'accès à des informations cruciales sur l'efficacité 
        énergétique est rapide et facile.
        """
    )
