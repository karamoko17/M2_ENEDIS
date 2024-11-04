import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import datetime
from streamlit_folium import folium_static
import os

# Configuration de Streamlit
st.set_page_config(page_title="Property Map", layout="wide")

# Mise en cache pour optimiser les performances
#@st.cache_data
def load_data():
    
    # Charger les jeux de données
    logements_existants = pd.read_csv("./Data/dpe-v2-logements-existants.csv")
    logements_neufs = pd.read_csv("./Data/dpe-v2-logements-neufs.csv")
    adresses = pd.read_csv("./Data/adresses-69.csv", sep=";")
    
    # Ajouter des étiquettes pour l'année et le type de logement
    logements_neufs["Logement"] = "neuf"
    logements_existants["Logement"] = "ancien"
    current_year = datetime.datetime.now().year
    logements_neufs["Année_construction"] = current_year
    
    # Fusionner les datasets sur les colonnes communes
    common_cols = logements_neufs.columns.intersection(logements_existants.columns)
    df_neufs = logements_neufs[common_cols]
    df_existants = logements_existants[common_cols]
    df = pd.concat([df_neufs, df_existants], ignore_index=True)
    
    # Fusionner avec les données d'adresse pour les coordonnées
    df = df.merge(adresses[['id', 'lat', 'lon']], left_on="Identifiant__BAN", right_on="id", how="left")
    return df

# Fonction pour afficher la carte
def create_map(data):
    lyon_location = [45.75, 4.85]
    m = folium.Map(location=lyon_location, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
    for idx, row in data.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
            popup_text = f"Logement: {row['Logement']}<br>Coût chauffage: {row.get('Coût_chauffage', 'N/A')}€<br>Surface: {row.get('Surface_habitable_logement', 'N/A')} m²"
            folium.Marker(
                location=[float(row['lat']), float(row['lon'])],
                popup=popup_text
            ).add_to(marker_cluster)
    
    return m

# Fonction principale pour l'affichage de la cartographie
def show():
    st.title("Property Data Visualization")
    df = load_data()

    # Options de filtrage dans Streamlit
    st.sidebar.header("Filter Options")
    logement_type = st.sidebar.multiselect("Select Property Type", options=df["Logement"].unique(), default=df["Logement"].unique())
    filtered_df = df[df["Logement"].isin(logement_type)]

    # Afficher la carte si des données sont disponibles
    if not filtered_df.empty:
        folium_map = create_map(filtered_df)
        st.write("### Property Map")
        folium_static(folium_map)
    else:
        st.write("No data available for selected filters.")
