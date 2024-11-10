import os
import streamlit as st
import pandas as pd

def show():
    st.header("Contexte  des données  Logements")

    # Charger les données
    try:
        df = pd.read_csv('./Data/data_carto.csv')
    except FileNotFoundError:
        st.error("Le fichier de données est introuvable. Veuillez vérifier le chemin.")
        return
    except Exception as e:
        st.error(f"Une erreur s'est produite lors du chargement des données : {e}")
        return
    
    # Appliquer les filtres
    filtered_df = df

    # Filtres interactifs sur la même ligne
    # st.write("##### Appliquer des filtres")
    col1, col2, col3, col4  = st.columns(4)
    with col1:
        logement_type = st.multiselect("Type de propriété", options=df["Logement"].unique())
    with col2:
        code_postal = st.multiselect("Codes postaux", options=df["Code_postal_(BAN)"].unique())
    with col3:
        dpe_label = st.multiselect("Étiquettes DPE", options=df["Etiquette_DPE"].unique())
    with col4:
        periode_construction = st.multiselect("Période de construction", options=df["Periode_construction"].unique())




    if logement_type:
        filtered_df = filtered_df[filtered_df["Logement"].isin(logement_type)]
    if code_postal:
        filtered_df = filtered_df[filtered_df["Code_postal_(BAN)"].isin(code_postal)]
    if dpe_label:
        filtered_df = filtered_df[filtered_df["Etiquette_DPE"].isin(dpe_label)]
    if periode_construction:
        filtered_df = filtered_df[filtered_df["Periode_construction"].isin(periode_construction)]

    # Afficher les statistiques sous forme de métriques
    st.write("##### Statistiques sur les propriétés filtrées")
    
    total_properties = len(filtered_df)
    average_surface = filtered_df['Surface_habitable_logement'].mean() if total_properties > 0 else 0
    average_heating_cost = filtered_df['Coût_chauffage'].mean() if total_properties > 0 else 0

    col1, col2, col3,  col4 = st.columns(4)
    with col1:
        st.metric("Nombre total de propriétés filtrées", f"{total_properties}")
    with col2:
        st.metric("Surface moyenne des propriétés", f"{average_surface:.2f} m²")
    with col3:
        st.metric("Coût moyen de chauffage", f"{average_heating_cost:.2f} €")
    with col4:
        # Option de téléchargement du tableau filtré
        st.download_button(
            label="Télécharger les données filtrées",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='proprietes_filtrees.csv',
            mime='text/csv'
        )

    # Afficher le DataFrame filtré sous forme de tableau
    st.write("##### Tableau des propriétés filtrées")
    st.dataframe(filtered_df, width=1200, height=500)


 