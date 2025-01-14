from flask import Flask, render_template, jsonify, request
from chat import get_response  
import os

app = Flask(__name__)


API_KEY = os.getenv("API_KEY")

@app.route("/")
def index_get():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
 
    user_api_key = request.headers.get("x-api-key")
    if user_api_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 401

    
    text = request.get_json().get("message")
    
    if text:  
        response = get_response(text)  
        message = {'answer': response}
    else:
        message = {'answer': "Sorry, I didn't understand that."}
    
    return jsonify(message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
