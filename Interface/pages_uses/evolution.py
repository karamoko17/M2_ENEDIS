import streamlit as st
import pandas as pd
import plotly.express as px

# # Créer un DataFrame à partir des données fournies
# data = {
#     "Logement": ["neuf", "neuf", "neuf", "neuf", "neuf"],
#     "Coût_chauffage": [90.2, 77.9, 167.6, 100.8, 189.5],
#     "Surface_habitable_logement": [43.9, 43.9, 48.2, 44.0, 42.0],
#     "Etiquette_DPE": ["C", "C", "C", "C", "C"],
#     "Periode_construction": ["Après 2010", "Après 2010", "Après 2010", "Après 2010", "Après 2010"],
#     "Coût_total_5_usages": [623.2, 610.9, 728.8, 634.6, 374.6],
#     "Code_postal_(BAN)": [69008.0, 69008.0, 69008.0, 69008.0, 69008.0],
#     "Adresse_(BAN)": [
#         "19bis Rue Antoine Dumont 69008 Lyon",
#         "19bis Rue Antoine Dumont 69008 Lyon",
#         "19bis Rue Antoine Dumont 69008 Lyon",
#         "19bis Rue Antoine Dumont 69008 Lyon",
#         "119 Rue Villon 69008 Lyon"
#     ]
# }

# df = pd.DataFrame(data)
df = pd.read_csv('./Data/data_carto.csv')

def show():
    # Filtres dans la barre latérale
    # Filtres dans la barre latérale
    st.sidebar.header("Filtres")
    logement_filter = st.sidebar.multiselect("Type de Logement", options=df["Logement"].unique())
    etiquette_filter = st.sidebar.multiselect("Étiquette DPE", options=df["Etiquette_DPE"].unique())
    periode_filter = st.sidebar.multiselect("Période de Construction", options=df["Periode_construction"].unique())

    # Appliquer les filtres
    if not logement_filter and not etiquette_filter and not periode_filter:
        # Si aucun filtre n'est sélectionné, afficher tout le DataFrame
        filtered_df = df
    else:
        filtered_df = df[
            (df["Logement"].isin(logement_filter) | (len(logement_filter) == 0)) &
            (df["Etiquette_DPE"].isin(etiquette_filter) | (len(etiquette_filter) == 0)) &
            (df["Periode_construction"].isin(periode_filter) | (len(periode_filter) == 0))
        ]

    # Convertir le code postal en type de données catégorique
    filtered_df['Code_postal_(BAN)'] = filtered_df['Code_postal_(BAN)'].astype(str)
    # Calcul des totaux
    total_chauffage = filtered_df["Coût_total_5_usages"].mean()
    total_surface = filtered_df["Etiquette_DPE"].mode()[0]
    total_usage = filtered_df["Coût_total_5_usages"].sum()

    # Afficher les métriques
    col1, col2 = st.columns(2)
    # col1, col2, col3 = st.columns(3)
    col1.metric(label="Coût moyen du chauffage", value=f"{total_chauffage:.2f} €")
    col2.metric(label="Ettiquette median", value=f"{total_surface}")
    # col3.metric(label="Coût total des 5 usages", value=f"{total_usage:.2f} €")

    # Afficher les détails et les graphiques
    col1, col2 = st.columns(2)
    # col1, col2, col3 = st.columns(3)


    # Obtenir les étiquettes DPE triées par ordre alphabétique
    sorted_labels = sorted(filtered_df['Etiquette_DPE'].unique())
    filtered_df['Année_construction'] = pd.Categorical(
    filtered_df['Année_construction'],
    ordered=True,  # Cela permet de garder l'ordre dans les catégories
    categories=sorted(filtered_df['Année_construction'].unique())  # Trie les années
   )
        # Créer une colonne pour l'année de construction
    filtered_df['Année_construction'] = pd.Categorical(
        filtered_df['Année_construction'],
        ordered=True,
        categories=sorted(filtered_df['Année_construction'].unique())
    )
# Créer l'histogramme avec les étiquettes DPE triées

    # Colonne 1 : Détails du logement
    with col1:
        fig_hist1 = px.histogram(
            filtered_df,
            x='Etiquette_DPE',
            y='Coût_total_5_usages',
            histfunc="avg",
            title="Moyenne du Coût Total des 5 Usages par Étiquette DPE",
            color_discrete_sequence=['skyblue'],
            category_orders={'Etiquette_DPE': sorted_labels}  # Spécifier l'ordre des catégories
        )
        st.plotly_chart(fig_hist1)

        # Camembert des étiquettes DPE
        # Graphique en ligne pour le coût total par surface habitable
        fig_line2 = px.bar(
            filtered_df,
            x='Logement',
            
            
            # histfunc="avg",
            title="Coût moyen par Période de Construction",
            color_discrete_sequence=['#6a51a3']
        )
        st.plotly_chart(fig_line2)

    # Colonne 2 : Histogramme et Camembert
    with col2:
        # Camembert des étiquettes DPE
        fig_pie = px.pie(
            filtered_df, names='Etiquette_DPE',
            title="Répartition des Étiquettes DPE",
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie)
        
        # Graphique en ligne pour le coût de chauffage
        # Graphique en ligne pour le coût de chauffage par surface habitable
        # fig_chauffage_surface = px.line(
        #     filtered_df,
        #     x='Surface_habitable_logement',  # Surface habitable en m²
        #     y='Coût_chauffage',
        #     title="Coût de Chauffage par Surface Habitable",
        #     color_discrete_sequence=['#2ca02c'],  # Choisissez une autre couleur
        #     markers=True  # Ajoutez des marqueurs pour chaque point
        # )

        fig_chauffage_surface = px.histogram(
            filtered_df,
            x="Etiquette_DPE",  # Étiquette DPE comme variable catégorique
            y="Etiquette_DPE",  # Étiquette DPE comme variable catégorique
            
            # y='Coût_total_5_usages',  # Coût total des 5 usages sur l'axe y
            animation_frame='Année_construction',  # Animation par année de construction
            color="Etiquette_DPE",  # Couleur en fonction de l'étiquette DPE
            histfunc="count",
            
            category_orders={'Etiquette_DPE': sorted_labels},
            # size='Coût_total_5_usages',  # Taille des points basée sur le coût total
            # size_max=45,  # Taille maximale des points
            # log_x=False,  # Définir à False si les valeurs de x ne sont pas logarithmiques
            # range_y=[0, filtered_df['Coût_total_5_usages'].max() * 1.1],  # Ajuster la plage de y pour être dynamique
        )

        st.plotly_chart(fig_chauffage_surface)



    # # Colonne 3 : Graphiques en barres et en lignes
    # with col3:
    #     # Graphique en barres pour le coût de chauffage par adresse
    #     fig_bar = px.bar(
    #         filtered_df, x='Adresse_(BAN)', y='Coût_chauffage',
    #         title="Coût de Chauffage par Adresse",
    #         color_discrete_sequence=['#2b83ba']
    #     )
    #     st.plotly_chart(fig_bar)

    #     # Graphique en ligne pour le coût total par surface habitable
    #     fig_line = px.line(
    #         filtered_df, x='Surface_habitable_logement', y='Coût_total_5_usages',
    #         title="Coût Total par Surface Habitable", markers=True, color_discrete_sequence=['#6a51a3']
    #     )
    #     st.plotly_chart(fig_line)

 
