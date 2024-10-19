from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to my Flask server!"

@app.route("/api/data", methods=["GET"])
def get_data():
    data = {"message": "Hello, World!", "data": [1, 2, 3, 4, 5]}
    return jsonify(data)

@app.route("/api/submit", methods=["POST"])
def submit_data():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"status": "success", "message": "Data received successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,  debug=True)