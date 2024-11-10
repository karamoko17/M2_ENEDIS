import os
import streamlit as st

def show():
    # Titre principal de la page avec une couleur et un style attrayants
    st.markdown("""
        <h1 style='text-align: center; color: #27ae60; font-size: 36px; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);'>
            À Propos de GreenTech Solutions
        </h1>
    """, unsafe_allow_html=True)

    # Séparateur horizontal stylisé
    st.markdown("<hr style='border: 1px solid #27ae60; border-radius: 10px;'>", unsafe_allow_html=True)

    # Définir le chemin de l'image
    image_path = './Interface/assets/img/dpe.jpg'

    # Vérifier si l'image existe avant de l'afficher
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, width=350, caption="Diagnostic de Performance Énergétique (DPE)")  # Ajustez la taille et ajoutez une légende
    else:
        st.error("Image non trouvée : " + image_path)
    
    # Espacement après l'image
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Diviser le texte en 2 sections pour plus de lisibilité avec un fond et une bordure stylisés
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
            <div style="text-align: justify; font-size: 18px; color: #34495e; line-height: 1.8; font-family: 'Verdana', sans-serif; padding: 20px; background-color: #ecf0f1; border-radius: 10px;">
                Grâce à des algorithmes avancés et à une interface conviviale, <strong style="color: #27ae60;">GreenTech Solutions</strong> permet 
                aux utilisateurs de mieux comprendre l'efficacité énergétique de leur logement. 
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="text-align: justify; font-size: 18px; color: #34495e; line-height: 1.8; font-family: 'Verdana', sans-serif; padding: 20px; background-color: #ecf0f1; border-radius: 10px;">
                Vous pouvez rapidement accéder à des informations cruciales et prendre des décisions éclairées pour améliorer 
                votre consommation énergétique. Rejoignez-nous pour faire un pas vers un avenir plus vert et plus économique !
            </div>
        """, unsafe_allow_html=True)



    # Pied de page avec un fond coloré et un lien stylisé
    st.markdown("""
        <br>
        <div style='text-align: center; font-size: 14px; color: #7f8c8d; font-family: "Arial", sans-serif; background-color: #f4f6f7; padding: 10px 0; border-radius: 5px;'>
            © 2024 GreenTech Solutions.
        </div>
    """, unsafe_allow_html=True)
