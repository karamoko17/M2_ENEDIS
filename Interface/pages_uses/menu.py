import streamlit as st

def show_menu():
    st.sidebar.markdown("<h1 style='text-align: center; color: black;'>GreenTech</h1>", unsafe_allow_html=True)
    
    # Boutons de navigation dans le menu latéral
    if st.sidebar.button("🏠 Accueil"):
        st.session_state.page = 'Accueil'
    if st.sidebar.button("🗺️ Cartographie"):
        st.session_state.page = 'Cartographie'
    if st.sidebar.button("📊 Prédiction prix de vente"):
        st.session_state.page = 'Prédiction'
    if st.sidebar.button("📊 Prediction prix"):
        st.session_state.page = 'regression'
    if st.sidebar.button("📈 Évolution"):
        st.session_state.page = 'Évolution'

    # Pied de page
    st.sidebar.markdown("GreenTech Solutions © 2024")
