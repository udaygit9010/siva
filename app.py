import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import numpy as np

# Load API keys from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

app = Flask(__name__)
CORS(app)

# 🔹 Load or Train SVM Model
MODEL_PATH = "svm_model.pkl"
VECTORIZER_PATH = "tfidf_vectorizer.pkl"

def train_svm_model():
    # Sample dataset (Replace with real dataset)
    texts = ["Breaking news: major event happening now!", "This is fake news, do not believe it!", "Government announces new policies."]
    labels = [1, 0, 1]  # 1 = Real, 0 = Fake
   
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
   
    model = SVC(kernel='linear', probability=True)
    model.fit(X, labels)
   
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
   
    return model, vectorizer

# Load existing model or train a new one
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model, vectorizer = train_svm_model()

# 🔹 Function to search Google News using the provided API key and search engine ID
def search_google_news(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")
@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Transform input text
    X_input = vectorizer.transform([text])
    
    # Make a prediction
    prediction = model.predict(X_input)[0]
    confidence = np.max(model.predict_proba(X_input))
    
    print(f"🔍 Text: {text}")  # Debugging
    print(f"📊 Prediction: {prediction}")  # Debugging
    print(f"🎯 Confidence: {confidence}")  # Debugging

    # Search Google News for comparison
    google_results = search_google_news(text)

    result = {
        "analysis": "This news appears to be real." if prediction == 1 else "This news might be fake.",
        "is_fake": int(prediction == 0),
        "confidence": float(confidence),
        "google_results": google_results
    }

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
