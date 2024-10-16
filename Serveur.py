from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a route for the root URL ("/") that returns a simple message
@app.route("/")
def index():
    return "Welcome to my Flask server!"

# Define a route for a GET request to "/api/data" that returns some sample data
@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello, World!", "data": [1, 2, 3, 4, 5]}
    return jsonify(data)

# Define a route for a POST request to "/api/submit" that accepts some data
@app.route("/api/submit", methods=["POST"])
def submit_data():
    data = request.get_json()
    print("Received data:", data)
    return "Data received successfully!"

if __name__ == "__main__":
    app.run(debug=True)