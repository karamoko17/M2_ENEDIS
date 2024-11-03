import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('../data/data_carto.csv')

def show():
    # Filtres dans la barre latérale
    st.sidebar.header("Filtres")
    logement_filter = st.sidebar.multiselect("Type de Logement", options=df["Logement"].unique())
    etiquette_filter = st.sidebar.multiselect("Étiquette DPE", options=df["Etiquette_DPE"].unique())
    periode_filter = st.sidebar.multiselect("Période de Construction", options=df["Periode_construction"].unique())

    # Appliquer les filtres
    if not any([logement_filter, etiquette_filter, periode_filter]):
        filtered_df = df
    else:
        filtered_df = df[
            (df["Logement"].isin(logement_filter) | len(logement_filter) == 0) &
            (df["Etiquette_DPE"].isin(etiquette_filter) | len(etiquette_filter) == 0) &
            (df["Periode_construction"].isin(periode_filter) | len(periode_filter) == 0)
        ]

    # Convertir le code postal en type de données catégorique
    filtered_df['Code_postal_(BAN)'] = filtered_df['Code_postal_(BAN)'].astype(str)

    # Calculer les totaux
    total_chauffage = filtered_df["Coût_total_5_usages"].mean() if not filtered_df.empty else 0
    total_surface = filtered_df["Etiquette_DPE"].mode()[0] if not filtered_df.empty else "N/A"
    total_usage = filtered_df["Coût_total_5_usages"].sum() if not filtered_df.empty else 0

    # Afficher les métriques
    col1, col2 = st.columns(2)
    col1.metric(label="Coût moyen du chauffage", value=f"{total_chauffage:.2f} €")
    col2.metric(label="Étiquette DPE dominante", value=total_surface)

    # Trier les étiquettes DPE
    sorted_labels = sorted(filtered_df['Etiquette_DPE'].unique())
    sorted_annee = sorted(filtered_df['Année_construction'].unique())

    # Créer les graphiques
    with col1:
        # Histogramme de la moyenne du coût total par Étiquette DPE
        fig_hist1 = px.histogram(
            filtered_df,
            x='Etiquette_DPE',
            y='Coût_total_5_usages',
            histfunc="avg",
            title="Moyenne du Coût Total des 5 Usages par Étiquette DPE",
            color_discrete_sequence=['skyblue'],
            category_orders={'Etiquette_DPE': sorted_labels}
        )
        st.plotly_chart(fig_hist1)

        # Histogramme du coût moyen par période de construction
        fig_line2 = px.histogram(
            filtered_df,
            x='Année_construction',
            y='Coût_total_5_usages',
            histfunc="avg",
            title="Coût moyen par Période de Construction",
            color_discrete_sequence=['#6a51a3']
        )
        st.plotly_chart(fig_line2)

    with col2:
        # Camembert des étiquettes DPE
        fig_pie = px.pie(
            filtered_df, names='Etiquette_DPE',
            title="Répartition des Étiquettes DPE",
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie)

        # Histogramme des Étiquettes DPE par année de construction
        fig_chauffage_surface = px.histogram(
            filtered_df,
            x="Etiquette_DPE",
            animation_frame='Année_construction',
            color="Etiquette_DPE",
            histfunc="count",
            category_orders={'Etiquette_DPE': sorted_labels , 'Année_construction':sorted_annee},
        )
        st.plotly_chart(fig_chauffage_surface)

if __name__ == "__main__":
    show()
