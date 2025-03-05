import openai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
CORS(app)

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

# Function to search Google News for verification
def search_google_news(query):
    GOOGLE_API_KEY = "AIzaSyAkKcye33pAhbFoU_aCZ1gRMEF7ul-kTk8"
# Replace with your Google API Key
    SEARCH_ENGINE_ID = "142a8acb8a92a4611"  # Replace with your Custom Search Engine ID

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
        ai_result = ai_response.get("choices", [{}])[0].get("message", {}).get("content", "Error processing AI response")
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
