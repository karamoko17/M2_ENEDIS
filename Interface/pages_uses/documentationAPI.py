import streamlit as st


def  show():
    
    # URL of the webpage to display
    url = "https://performance-energetique-server.onrender.com/apidocs/"

    # Create an iframe to display the webpage
    iframe_code = f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>'

    # Display the iframe in the Streamlit app
    st.write(iframe_code, unsafe_allow_html=True)