from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  
from chat import get_response

app = Flask(__name__)

# Enable CORS for local and deployed URLs
CORS(app, origins=["http://127.0.0.1:5000", "https://university-bot-8sh1.onrender.com"], supports_credentials=True)

@app.route("/")
def index_get():
    return render_template('index.html')

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return "", 200  # Handle preflight requests for CORS

    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging

        text = data.get("message")
        if text:
            response = get_response(text)
            print("Generated response:", response)  # Debugging
            message = {'answer': response}
        else:
            message = {'answer': "Sorry, I didn't understand that."}

    except Exception as e:
        print("Error occurred:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500  # Internal Server Error

    return jsonify(message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
