import os
from google.cloud import storage
import joblib  # or you can use import pickle

# Set up authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"  # Replace with your service account key path

def load_model_from_gcs(bucket_name, model_file_name):
    # Initialize the GCS client
    storage_client = storage.Client()
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Get the blob (file) from the bucket
    blob = bucket.blob(model_file_name)
    
    # Download the model file as bytes
    model_data = blob.download_as_bytes()
    
    # Load the model using joblib (or pickle)
    model = joblib.loads(model_data)  # Use pickle.loads(model_data) if using pickle
    
    return model

# Usage
bucket_name = 'performanceenergetique-6f3af.appspot.com'
model_file_name = 'random_forest_regressor.pkl'

model = load_model_from_gcs(bucket_name, model_file_name)
print("Model loaded successfully!")