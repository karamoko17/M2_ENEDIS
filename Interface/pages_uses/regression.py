import streamlit as st
import requests

def show():
    st.header("Prédiction du Prix de Vente")
    st.write("Ici, vous pouvez estimer le prix de vente d'un bien immobilier.")

    # Créer deux colonnes
    col1, col2 = st.columns(2)

    # Champs d'entrée pour la première colonne
    with col1:
        periode_construction = st.selectbox("Période de Construction", 
                                             ['Avant 1960', '1961 - 1970', '1981 - 1990', 
                                              '1991 - 2000', '2001 - 2010', 'Après 2010'])
        surface_habitable_logement = st.number_input("Surface Habitable (m²)", min_value=0, value=100)
        etiquette_dpe = st.selectbox("Étiquette DPE", ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        deperditions_enveloppe = st.number_input("Déperditions Enveloppe", min_value=0.0, value=100.0)
        annee_reception_dpe = st.number_input("Année de Réception DPE", min_value=1900, max_value=2024, value=2024)
        deperditions_renouvellement_air = st.number_input("Déperditions Renouvellement Air", min_value=0.0, value=20.0)

    # Champs d'entrée pour la deuxième colonne
    with col2:
        type_energie_n1 = st.selectbox("Type d'Énergie N°1", 
                                         ['Électricité', 'Gaz naturel', 'Charbon', 'Bois – Bûches',
                                          'Réseau de Chauffage urbain', 'Bois – Granulés (pellets) ou briquettes',
                                          'Fioul domestique', "Électricité d'origine renouvelable utilisée dans le bâtiment",
                                          'Bois – Plaquettes d’industrie', 'GPL', 'Bois – Plaquettes forestières', 'Propane'])
        deperditions_baies_vitre = st.number_input("Déperditions Baies Vitrées", min_value=0.0, value=10.0)
        qualite_isolation_murs = st.selectbox("Qualité de l'Isolation des Murs", ['insuffisante', 'moyenne', 'bonne', 'très bonne'])
        deperditions_ponts_thermiques = st.number_input("Déperditions Ponts Thermiques", min_value=0.0, value=5.0)
        deperditions_murs = st.number_input("Déperditions Murs", min_value=0.0, value=20.0)
        deperditions_planchers_hauts = st.number_input("Déperditions Planchers Hauts", min_value=0.0, value=10.0)

    # Create a button to make the prediction
    if st.button("Prédire"):
        # Prepare the data for the API
        input_data = {
            "Periode_construction": periode_construction,
            "Surface_habitable_logement": surface_habitable_logement,
            "Etiquette_DPE": etiquette_dpe,
            "Deperditions_enveloppe": deperditions_enveloppe,
            "Annee_reception_DPE": annee_reception_dpe,
            "Déperditions_renouvellement_air": deperditions_renouvellement_air,
            "Type_énergie_n°1": type_energie_n1,
            "Deperditions_baies_vitrées": deperditions_baies_vitre,
            "Qualité_isolation_murs": qualite_isolation_murs,
            "Déperditions_ponts_thermiques": deperditions_ponts_thermiques,
            "Déperditions_murs": deperditions_murs,
            "Deperditions_planchers_hauts": deperditions_planchers_hauts
        }

        # Send the request to the Flask API
        # response = requests.post("http://127.0.0.1:5000/predict", json=input_data)
        response = requests.post("https://performance-energetique-server.onrender.com/predict", json=input_data)


        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.success(f"La prédiction du prix de vente est : {prediction:.2f}")
        else:
            st.error("Erreur dans la prédiction. Vérifiez vos entrées.")

if __name__ == "__main__":
    show()