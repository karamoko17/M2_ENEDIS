import streamlit as st
import pandas as pd
import pydeck as pdk

def show():
    # Titre de l'interface
    # st.title("Carte des Logements à Lyon avec Couleurs DPE et Filtres")

    # Charger les données
    df = pd.read_csv('./Data/data_carto.csv')

    # Filtrer et nettoyer les données
    df_cleaned = df[['lat', 'lon', 'Logement', 'Adresse_(BAN)', 'Code_postal_(BAN)', 'Coût_total_5_usages', 'Periode_construction', 'Coût_chauffage', 'Surface_habitable_logement', 'Etiquette_DPE']].dropna(subset=['lat', 'lon', 'Etiquette_DPE'])

    # Options de filtres sans sélection par défaut
    code_postal_options = df_cleaned['Code_postal_(BAN)'].unique().tolist()
    periode_construction_options = df_cleaned['Periode_construction'].unique().tolist()
    dpe_options = df_cleaned['Etiquette_DPE'].unique().tolist()

    # Agencement des filtres en ligne
    col1, col2, col3 = st.columns(3)
    with col1:
        code_postal_filter = st.multiselect("Code postal", options=code_postal_options)
    with col2:
        periode_construction_filter = st.multiselect("Période de construction", options=periode_construction_options)
    with col3:
        dpe_filter = st.multiselect("Étiquette DPE", options=dpe_options)

    # Appliquer les filtres si des valeurs sont sélectionnées
    if code_postal_filter:
        df_cleaned = df_cleaned[df_cleaned['Code_postal_(BAN)'].isin(code_postal_filter)]
    if periode_construction_filter:
        df_cleaned = df_cleaned[df_cleaned['Periode_construction'].isin(periode_construction_filter)]
    if dpe_filter:
        df_cleaned = df_cleaned[df_cleaned['Etiquette_DPE'].isin(dpe_filter)]

    # Définir les couleurs pour chaque étiquette DPE
    dpe_colors = {
        "A": [0, 255, 0, 160],   # Vert clair pour DPE A
        "B": [0, 255, 255, 160], # Cyan pour DPE B
        "C": [255, 255, 0, 160], # Jaune pour DPE C
        "D": [255, 165, 0, 160], # Orange pour DPE D
        "E": [255, 69, 0, 160],  # Rouge-orange pour DPE E
        "F": [255, 0, 0, 160],   # Rouge pour DPE F
        "G": [139, 0, 0, 160],   # Rouge foncé pour DPE G
    }

    # Ajouter une colonne 'color' au dataframe en fonction du DPE
    df_cleaned['color'] = df_cleaned['Etiquette_DPE'].map(dpe_colors)

    # Créer une couche de marqueurs avec pydeck, en utilisant la couleur selon DPE
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_cleaned,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=20,
        pickable=True,
        opacity=0.6
    )

    # Créer une vue de la carte centrée autour de Lyon
    view_state = pdk.ViewState(
        latitude=45.75,
        longitude=4.85,
        zoom=12,
        pitch=0
    )

    # Créer la carte avec pydeck (utilisation de Mapbox pour un fond personnalisé)
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/streets-v11',  # Utiliser un style Mapbox pour la carte
        tooltip={
            "html": "<b>Logement:</b> {Logement}<br><b>Adresse:</b> {Adresse_(BAN)}<br><b>Coût chauffage:</b> {Coût_chauffage}€<br><b>Surface:</b> {Surface_habitable_logement} m²<br><b>DPE:</b> {Etiquette_DPE}",
            "style": {"color": "white"}
        }
    )

    # Agencement en colonnes pour la carte et la légende
    col1, col2 = st.columns([5, 1])

    # Afficher la carte dans la première colonne
    with col1:
        st.pydeck_chart(r)

    # Afficher la légende dans la deuxième colonne
    with col2:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: flex-start; padding: 10px; background-color: #f9f9f9; border-radius: 5px;'>
            <b>Légende des Étiquettes DPE</b>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(0, 255, 0); display: inline-block; margin-right: 10px;'></span> A </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(0, 255, 255); display: inline-block; margin-right: 10px;'></span> B </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(255, 255, 0); display: inline-block; margin-right: 10px;'></span> C </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(255, 165, 0); display: inline-block; margin-right: 10px;'></span> D </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(255, 69, 0); display: inline-block; margin-right: 10px;'></span> E </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(255, 0, 0); display: inline-block; margin-right: 10px;'></span> F </div>
            <div style='display: flex; align-items: center;'><span style='width: 15px; height: 15px; background-color: rgb(139, 0, 0); display: inline-block; margin-right: 10px;'></span> G </div>
        </div>
        """, unsafe_allow_html=True)

