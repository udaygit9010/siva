import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to search Google News for the news headline
def search_google_news(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx=YOUR_CSE_ID&key=142a8acb8a92a4611"
    response = requests.get(url)
    results = response.json()
    
    news_links = []
    if "items" in results:
        for item in results["items"]:
            news_links.append({"title": item["title"], "link": item["link"]})
    
    return news_links

@app.route('/predict', methods=['POST'])
def predict():
    news_text = request.form['news_text']

    # Step 1: Ask ChatGPT for an analysis
    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Analyze this news and tell me if it's fake or real: {news_text}"}]
    )
    ai_result = ai_response["choices"][0]["message"]["content"]

    # Step 2: Search Google News for verification
    news_results = search_google_news(news_text[:50])  # Search using first 50 characters of news text

    return jsonify({
        "AI_Analysis": ai_result,
        "Trusted_News_Links": news_results if news_results else "No matching news found"
    })

if __name__ == '__main__':
    app.run(debug=True)
