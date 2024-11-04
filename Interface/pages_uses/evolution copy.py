import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Créer un DataFrame à partir des données fournies
data = {
    "Logement": ["neuf", "neuf", "neuf", "neuf", "neuf"],
    "Coût_chauffage": [90.2, 77.9, 167.6, 100.8, 189.5],
    "Surface_habitable_logement": [43.9, 43.9, 48.2, 44.0, 42.0],
    "Etiquette_DPE": ["C", "C", "C", "C", "C"],
    "Periode_construction": ["Après 2010", "Après 2010", "Après 2010", "Après 2010", "Après 2010"],
    "Coût_total_5_usages": [623.2, 610.9, 728.8, 634.6, 374.6],
    "Code_postal_(BAN)": [69008.0, 69008.0, 69008.0, 69008.0, 69008.0],
    "Adresse_(BAN)": [
        "19bis Rue Antoine Dumont 69008 Lyon",
        "19bis Rue Antoine Dumont 69008 Lyon",
        "19bis Rue Antoine Dumont 69008 Lyon",
        "19bis Rue Antoine Dumont 69008 Lyon",
        "119 Rue Villon 69008 Lyon"
    ]
}

df = pd.DataFrame(data)
def  show():
    

    # Filtres dans la barre latérale
    st.sidebar.header("Filtres")
    logement_filter = st.sidebar.multiselect("Type de Logement", options=df["Logement"].unique(), default=df["Logement"].unique())
    etiquette_filter = st.sidebar.multiselect("Étiquette DPE", options=df["Etiquette_DPE"].unique(), default=df["Etiquette_DPE"].unique())
    periode_filter = st.sidebar.multiselect("Période de Construction", options=df["Periode_construction"].unique(), default=df["Periode_construction"].unique())

    # Appliquer les filtres
    filtered_df = df[
        (df["Logement"].isin(logement_filter)) &
        (df["Etiquette_DPE"].isin(etiquette_filter)) &
        (df["Periode_construction"].isin(periode_filter))
    ]

    # Calcul des totaux
    total_chauffage = filtered_df["Coût_chauffage"].sum()
    total_surface = filtered_df["Surface_habitable_logement"].sum()
    total_usage = filtered_df["Coût_total_5_usages"].sum()

    # # Afficher la ligne des totaux
    # st.write("### Totaux")
    # st.write(f"**Coût total de chauffage** : {total_chauffage} €")
    # st.write(f"**Surface habitable totale** : {total_surface} m²")
    # st.write(f"**Coût total des 5 usages** : {total_usage} €")

    # Trois colonnes pour l'affichage
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Coût total de chauffage", value=f"{total_chauffage:.2f} €")
        
    with col2:
        st.metric(label="Surface habitable totale", value=f"{total_surface:.2f} m²")
        
    with col3:
        st.metric(label="Coût total des 5 usages", value=f"{total_usage:.2f} €")


    # Colonne 1 : Détails du logement
    with col1:
        st.subheader("Détails du Logement")
        st.write(filtered_df[["Logement", "Coût_chauffage", "Surface_habitable_logement", "Etiquette_DPE", "Periode_construction"]])

    # Colonne 2 : Histogramme et Camembert
    with col2:
        st.subheader("Histogramme et Camembert")

        # Histogramme du coût de chauffage
        plt.figure(figsize=(8, 4))
        sns.histplot(filtered_df['Coût_chauffage'], bins=10, kde=True, color='skyblue')
        plt.title("Répartition du Coût de Chauffage (€)")
        st.pyplot(plt)

        # Camembert des étiquettes DPE
        plt.figure(figsize=(6, 6))
        filtered_df['Etiquette_DPE'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        plt.title("Répartition des Étiquettes DPE")
        plt.ylabel('')  # Cache l'étiquette de l'axe y
        st.pyplot(plt)

    # Colonne 3 : Graphiques en barres et en lignes
    with col3:
        st.subheader("Graphiques Comparatifs")

        # Graphique en barres pour le coût de chauffage par adresse
        plt.figure(figsize=(8, 4))
        sns.barplot(x='Adresse_(BAN)', y='Coût_chauffage', data=filtered_df, palette="viridis")
        plt.title("Coût de Chauffage par Adresse")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)

        # Graphique en ligne pour le coût total par surface habitable
        plt.figure(figsize=(8, 4))
        sns.lineplot(x='Surface_habitable_logement', y='Coût_total_5_usages', data=filtered_df, marker='o', color="purple")
        plt.title("Coût Total par Surface Habitable")
        plt.xlabel("Surface Habitable (m²)")
        plt.ylabel("Coût Total (€)")
        st.pyplot(plt)
