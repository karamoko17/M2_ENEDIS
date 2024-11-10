import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

def show():
    # Spécifiez le chemin du fichier PDF à afficher
    file_path = "./Documentation/Doc_fonctionnelle.pdf"  # Remplacez par le chemin de votre fichier

    try:
        # Ouvrir et lire le fichier PDF en mode binaire
        with open(file_path, "rb") as pdf_file:
            binary_data = pdf_file.read()
            
            # Affichez le PDF en utilisant une largeur maximale et une hauteur personnalisée
            pdf_viewer(input=binary_data, width=1000, height=900)
    
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")