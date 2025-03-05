import openai
import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

if not OPENAI_API_KEY or not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
    raise ValueError("⚠️ Missing API keys! Set them as environment variables.")

openai.api_key = OPENAI_API_KEY

# Function to search Google News for verification
def search_google_news(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    
    try:
        results = response.json()
        news_links = []
        if "items" in results:
            for item in results["items"]:
                news_links.append({"title": item["title"], "link": item["link"]})
        return news_links
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return "Fake News Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    news_text = request.form.get('news_text')

    if not news_text:
        return jsonify({"error": "No news text provided"}), 400

    # Step 1: Ask ChatGPT for an analysis
    try:
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Analyze this news and tell me if it's fake or real: {news_text}"}]
        )
        ai_result = ai_response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500

    # Step 2: Search Google News for verification
    news_results = search_google_news(news_text[:50])

    return jsonify({
        "AI_Analysis": ai_result,
        "Trusted_News_Links": news_results if news_results else "No matching news found"
    })

if __name__ == '__main__':
    app.run(debug=True)
