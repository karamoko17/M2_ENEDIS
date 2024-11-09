import os
import streamlit as st
import pandas as pd
import datetime


def load_all_data():
    # Charger les jeux de données
    logements_existants = pd.read_csv("./Data/dpe-v2-logements-existants.csv")
    logements_neufs = pd.read_csv("./Data/dpe-v2-logements-neufs.csv")

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
  
    return df

def show():
    st.header("Cartographie")
    df = load_all_data()

    # Options de filtrage dans Streamlit
    st.write("##### Filtres")
    logement_type = st.multiselect("Sélectionnez le type de la propriété", options=df["Logement"].unique(), default=df["Logement"].unique())
    filtered_df = df[df["Logement"].isin(logement_type)]

    # Afficher le DataFrame filtré sous forme de tableau avec taille personnalisée
    st.write("##### Tableau des propriétés filtrées")
    st.dataframe(filtered_df, width=1200, height=600)  # Spécifie la largeur et la hauteur du tableau


