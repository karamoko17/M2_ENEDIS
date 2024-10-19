import streamlit as st
import requests

# Define a function to make a GET request to the Flask API endpoint
def get_data():
    response = requests.get("http://localhost:5000/api/data")
    data = response.json()
    return data

# Create a button to trigger the API request
st.button("Get Data", on_click=get_data)

# Display the data in the Streamlit app
st.write(get_data())