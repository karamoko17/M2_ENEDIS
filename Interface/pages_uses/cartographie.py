#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# Load data
df_reshaped = pd.read_csv('data/data_carto.csv')

def show():
    st.title("Tableau de bord interactif des lieux de santé")

    # Exemple de données pour df_reshaped, vous remplacerez ceci par le chargement de vos données réelles
    # df_reshaped = pd.read_csv('votre_fichier.csv')
    with st.sidebar:
        # Liste des périodes de construction uniques
        year_list = list(df_reshaped.Periode_construction.unique())[::-1]

        # Utilisation de `multiselect` pour permettre plusieurs sélections
        selected_years = st.multiselect('Sélectionnez une ou plusieurs périodes de construction', year_list)

        # Filtrer les données en fonction des périodes sélectionnées
        df_selected_years = df_reshaped[df_reshaped['Periode_construction'].isin(selected_years)]
        
        # Trier les résultats
        df_selected_year_sorted = df_selected_years.sort_values(by="Periode_construction", ascending=False)

    # Affichage du tableau filtré
    st.write("Données pour les périodes sélectionnées :")
    st.dataframe(df_selected_year_sorted)

# Appel de la fonction pour afficher le tableau de bord
if __name__ == '__main__':
    show()
