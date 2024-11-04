import streamlit as st

def show_menu():
    # CSS pour styliser la top bar
    st.markdown("""
        <style>
        .topbar {
            background-color: #134f5c; /* Couleur de fond */
            position: fixed; /* Fixer la top bar en haut */
            top: 0; /* Positionner en haut */
            left: 0; /* Positionner à gauche */
            width: 100%; /* Largeur 100% */
            padding: 10px 0; /* Espacement vertical */
            text-align: center; /* Centre le texte */
            color: white; /* Couleur du texte */
            font-family: 'Arial', sans-serif; /* Police de caractère */
            z-index: 9999; /* Assurer que la top bar soit au-dessus des autres éléments */
        }
        .topbar h1 {
            font-size: 36px; /* Taille du titre */
            margin: 0; /* Supprimer les marges */
        }

        /* Ajouter un espacement pour le contenu sous la top bar fixe */
        body {
            padding-top: 80px; /* Ajuster la hauteur du padding en fonction de la taille de la top bar */
        }
        </style>
    """, unsafe_allow_html=True)

    # Créer la top bar
    st.markdown('<div class="topbar"><h1>GreenTech Solutions</h1></div>', unsafe_allow_html=True)

