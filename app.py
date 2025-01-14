from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  
from chat import get_response
import os
app = Flask(__name__)


CORS(app, origins=["http://127.0.0.1:5000", "https://university-bot-8sh1.onrender.com"], supports_credentials=True)


API_KEY = "4c362fc58cb1f7894ea3e0c3356172a9d643cb14e77feb8fe6f70e6857cad0fa"

@app.route("/")
def index_get():
    return render_template('index.html', api_key=API_KEY)

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return "", 200 
    
    try:
        user_api_key = request.headers.get("x-api-key")
        print("Received API Key:", user_api_key) 

        if user_api_key != API_KEY:
            print("Unauthorized access due to incorrect API key.")
            return jsonify({"error": "Unauthorized access"}), 401

        data = request.get_json()
        print("Received data:", data)  

        text = data.get("message")
        if text:
            response = get_response(text)
            print("Generated response:", response)  
            message = {'answer': response}
        else:
            message = {'answer': "Sorry, I didn't understand that."}
    
    except Exception as e:
        print("Error occurred:", str(e)) 
        return jsonify({"error": str(e)}), 500  

    return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
