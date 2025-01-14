from flask import Flask, render_template, jsonify, request
from chat import get_response
import os

app = Flask(__name__)

# Load API Key from Environment Variable
API_KEY = os.getenv("API_KEY")

@app.route("/")
def index_get():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # Check for API Key in request headers
    user_api_key = request.headers.get("x-api-key")
    if user_api_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 401

    # Process the chatbot response if API key is valid
    text = request.get_json().get("message")
    response = get_response(text)
    message = {'answer': response}
    return jsonify(message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
