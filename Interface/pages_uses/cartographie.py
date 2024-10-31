import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

def show():
    # Données d'exemple
    data = pd.DataFrame({
        'lat': [45.764043, 45.757813, 45.763423, 45.761143, 45.758943],
        'lon': [4.835659, 4.832443, 4.837456, 4.834123, 4.830643],
        'type': ['Pharmacie', 'Parapharmacie', 'Pharmacie', 'Parapharmacie', 'Pharmacie'],
        'sales': [100, 150, 200, 250, 300]
    })

    # Titre
    st.title("Tableau de bord interactif des lieux de santé")

    # Filtres dans la barre latérale
    st.sidebar.header("Filtres")
    type_filter = st.sidebar.multiselect("Type de lieu", data['type'].unique(), default=data['type'].unique())
    min_sales = st.sidebar.slider("Ventes minimales", min_value=int(data['sales'].min()), max_value=int(data['sales'].max()), value=int(data['sales'].min()))

    # Filtrage des données
    filtered_data = data[(data['type'].isin(type_filter)) & (data['sales'] >= min_sales)]

    # Création de la mise en page à deux colonnes
    col1, col2 = st.columns([2, 1])

    # Colonne 1 : Carte et graphique camembert
    with col1:
        # Carte
        if not filtered_data.empty:
            avg_lat = filtered_data['lat'].mean()
            avg_lon = filtered_data['lon'].mean()
            view_state = pdk.ViewState(latitude=avg_lat, longitude=avg_lon, zoom=12)
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=filtered_data,
                get_position=["lon", "lat"],
                get_radius=200,
                get_fill_color=[255, 0, 0],
                pickable=True
            )
            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
        else:
            st.warning("Aucune donnée à afficher avec les filtres sélectionnés.")

        # Graphique camembert
        st.subheader("Répartition des types de lieux")
        if not filtered_data.empty:
            fig, ax = plt.subplots()
            type_counts = filtered_data['type'].value_counts()
            ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.axis("equal")  # Assure une forme de cercle
            st.pyplot(fig)
        else:
            st.warning("Aucune donnée à afficher pour le graphique camembert.")

    # Colonne 2 : Trois graphiques, chacun prenant 1/3
    with col2:
        st.subheader("Analyse des ventes")
        
        if not filtered_data.empty:
            # Graphique 1 : Histogramme des ventes
            st.write("Histogramme des ventes")
            fig1, ax1 = plt.subplots()
            ax1.hist(filtered_data['sales'], bins=10, color='skyblue', edgecolor='black')
            ax1.set_xlabel("Ventes")
            ax1.set_ylabel("Fréquence")
            st.pyplot(fig1)

            # Graphique 2 : Graphique linéaire
            st.write("Graphique linéaire des ventes")
            fig2, ax2 = plt.subplots()
            ax2.plot(filtered_data['sales'], marker='o', color='green')
            ax2.set_title("Tendance des ventes")
            ax2.set_xlabel("Index")
            ax2.set_ylabel("Ventes")
            st.pyplot(fig2)

            # Graphique 3 : Graphique en barres
            st.write("Graphique en barres des ventes")
            fig3, ax3 = plt.subplots()
            ax3.bar(filtered_data.index, filtered_data['sales'], color='orange', edgecolor='black')
            ax3.set_xlabel("Index")
            ax3.set_ylabel("Ventes")
            st.pyplot(fig3)
        else:
            st.warning("Aucune donnée à afficher pour les graphiques.")

# Appeler la fonction pour afficher le tableau de bord
if __name__ == "__main__":
    show()