import streamlit as st

def show():
    # Spécifiez le chemin du fichier Markdown
    file_path = "https://github.com/Adjaro/Performance_Energetique/blob/513c6c352aa6ea15a43e25d5595235ed2671ea01/Documentation/Rapport_analyse.md"  # Remplacez ce chemin par le chemin réel de votre fichier

    try:
        # Ouvrir et lire le contenu du fichier Markdown avec l'encodage UTF-8
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()

        # Afficher le contenu du fichier Markdown
        st.markdown(markdown_content)
    
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} n'a pas été trouvé.")
    except UnicodeDecodeError:
        st.error("Le fichier contient des caractères invalides ou l'encodage n'est pas correct.")
