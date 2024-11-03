import streamlit as st
import requests

def show():
    st.header("Prédiction du Prix de Vente")
    st.write("Ici, vous pouvez estimer le prix de vente d'un bien immobilier.")

    # Créer deux colonnes
    col1, col2 = st.columns(2)

    # Champs d'entrée pour la première colonne
    with col1:

        conso_5_usages_par_m2_e_primaire = st.number_input("Conso_5_usages_par_m²_é_primaire (kWh/m²)", min_value=0.0, value=200000.0)
        emission_GES_5_usages_par_m2 = st.number_input("Emission_GES_5_usages_par_m² (kgCO2/m²)", min_value=0.0, value=20.0)
        conso_5_usages_par_m2_e_finale = st.number_input("Conso_5_usages/m²_é_finale (kWh/m²)", min_value=0.0, value=80.0)
        conso_chauffage_e_primaire = st.number_input("Conso_chauffage_é_primaire (kWh)", min_value=0.0, value=120.0)
        emission_GES_chauffage = st.number_input("Emission_GES_chauffage (kgCO2)", min_value=0.0, value=15.0)
        cout_chauffage = st.number_input("Coût_chauffage (€)", min_value=0.0, value=300.0)
        besoin_ECS = st.number_input("Besoin_ECS (kWh)", min_value=0.0, value=50.0)

    # Champs d'entrée pour la deuxième colonne
    with col2:
        cout_total_5_usages = st.number_input("Coût_total_5_usages (€)", min_value=0.0, value=500.0)
        conso_5_usages_e_finale_energie_n1 = st.number_input("Conso_5_usages_é_finale_énergie_n°1 (kWh)", min_value=0.0, value=200.0)
        conso_ECS_e_primaire = st.number_input("Conso_ECS_é_primaire (kWh)", min_value=0.0, value=100.0)
        conso_eclairage_e_finale = st.number_input("Conso_éclairage_é_finale (kWh)", min_value=0.0, value=10.0)
        
        type_energie_principale_chauffage = st.selectbox(
            "Type_énergie_principale_chauffage", 
            ['Électricité', 'Gaz naturel', 'Charbon', 'Bois – Bûches', 'Fioul domestique', 
            'Réseau de Chauffage urbain', 'Bois – Granulés (pellets) ou briquettes', 
            'Bois – Plaquettes d’industrie', 'GPL', 'Bois – Plaquettes forestières', 
            'Propane', "Électricité d'origine renouvelable utilisée dans le bâtiment"]
        )
        
        conso_chauffage_e_finale = st.number_input("Conso_chauffage_é_finale (kWh)", min_value=0.0, value=150.0)
        annee_construction = st.number_input("Année_construction", min_value=1460, max_value=2024, value=2024)
        surface_habitable_logement = st.number_input("Surface_habitable_logement (m²)", min_value=0.0, value=100.0)



    # Create a button to make the prediction
    if st.button("Soumettre"):

        input_data = {
            "Conso_5_usages_par_m²_é_primaire": conso_5_usages_par_m2_e_primaire,
            "Emission_GES_5_usages_par_m²": emission_GES_5_usages_par_m2,
            "Conso_5_usages/m²_é_finale": conso_5_usages_par_m2_e_finale,
            "Conso_chauffage_é_primaire": conso_chauffage_e_primaire,
            "Emission_GES_chauffage": emission_GES_chauffage,
            "Coût_chauffage": cout_chauffage,
            "Besoin_ECS": besoin_ECS,
            "Surface_habitable_logement": surface_habitable_logement,
            "Coût_total_5_usages": cout_total_5_usages,
            "Conso_5_usages_é_finale_énergie_n°1": conso_5_usages_e_finale_energie_n1,
            "Conso_ECS_é_primaire": conso_ECS_e_primaire,
            "Conso_éclairage_é_finale": conso_eclairage_e_finale,
            "Type_énergie_principale_chauffage": type_energie_principale_chauffage,
            "Conso_chauffage_é_finale": conso_chauffage_e_finale,
            "Année_construction": annee_construction
        }

        # Send the request to the Flask API
        response = requests.post("https://performance-energetique-server.onrender.com/classification", json=input_data)
        # response = requests.post("http://127.0.0.1:5000/classification", json=input_data)
        # https://performance-energetique-server.onrender.com/

        # st.write(input_data)
        # st.write(response)
        # st.write(response.json())
        if response.status_code == 200:

            prediction = response.json()['classification']
            st.success(f"classification  : {prediction}")
        else:
            st.error("Erreur dans la prédiction. Vérifiez vos entrées.")

if __name__ == "__main__":
    show()
