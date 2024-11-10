import streamlit as st

def show_menu():
    # CSS pour uniformiser la largeur des boutons et aligner le texte à gauche
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;        /* Largeur de 100% pour uniformiser */
            text-align: left;   /* Alignement du texte à gauche */
            display: flex;      /* Utiliser Flexbox */
            align-items: center; /* Centrer le contenu verticalement */
            justify-content: flex-start; /* Aligner le texte à gauche */
            padding-left: 10px; /* Décalage du texte à gauche */
        }
        /* Agrandir le titre */
        .sidebar-title {
            font-size: 24px !important; /* Ajuster la taille selon les besoins */
            text-align: center; 
            color: green; 
            margin: 20px 0; /* Espacement autour du titre */
        }
        /* Style pour le pied de page */
        .footer {
            position: relative; /* Change en relative pour éviter de coller en bas */
            margin-top: auto; /* Pousser vers le bas si nécessaire */
            padding: 20px 0; /* Ajuster l'espacement autour du texte */
            text-align: center; /* Centrer le texte */
            color: black; /* Couleur du texte */
            font-size: 14px; /* Taille du texte */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Charger la bibliothèque FontAwesome
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)

    # Titre avec une icône dans la barre latérale
    st.sidebar.markdown("""
        <h1 class='sidebar-title'>
            <i class="fa fa-leaf"></i> GreenTech Solutions
        </h1>
    """, unsafe_allow_html=True)

    # Options de documentation dans le menu latéral
    page_options = [
        "Choisissez une page",
        "📚 Rapport",
        "📡 API",
        "📑 Fonctionnelle",
        "📘 Technique"
    ]
    
    # Boutons de navigation dans le menu latéral
    if st.sidebar.button("🏠 Accueil"):
        st.session_state.page = 'Accueil'
    if st.sidebar.button("💡 Contexte"):
        st.session_state.page = 'Contexte'
    if st.sidebar.button("🗺️ Cartographie"):
        st.session_state.page = 'Cartographie'
    if st.sidebar.button("🗺️ Cartographie Proposition"):
        st.session_state.page = 'Cartographie Proposition'
    if st.sidebar.button("📊 Prédiction de la consommation"):
        st.session_state.page = 'Prédiction'
    if st.sidebar.button("🏷️ Prédiction de l'étiquette DPE"):
        st.session_state.page = 'Classification'
    if st.sidebar.button("📈 Analyses"):
        st.session_state.page = 'Analyses'
    st.sidebar.markdown("<div class='footer'>Documentation</div>", unsafe_allow_html=True)

    if st.sidebar.button("📡 API"):
        st.session_state.page = '📡 API'
    if st.sidebar.button("📑 Fonctionnelle"):
        st.session_state.page = '📑 Fonctionnelle'
    if st.sidebar.button("📘 Technique"):
        st.session_state.page = '📘 Technique'
    if st.sidebar.button("📚 Rapport"):
        st.session_state.page = '📚 Rapport'
    
    # :
    #     # Sélecteur de documentation sans affecter l'état de la page
    # selected_page = st.sidebar.selectbox("Documentation", page_options, index=0)
    # if selected_page != "Choisissez une page":
    #     # pass
    #     st.session_state.page = selected_page
    #     selected_page = "Choisissez une page"

    # Pied de page avec le CSS
    st.sidebar.markdown("<div class='footer'>Awa Edina Nancy © 2024</div>", unsafe_allow_html=True)

