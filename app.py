import requests
import os
import json
import random  # For generating a fake accuracy score
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

app = Flask(__name__)
CORS(app)

# Function to search Google News
def search_google_news(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
    response = requests.get(url)

    try:
        results = response.json()
        news_links = []
        if "items" in results:
            for item in results["items"]:
                # Extract the domain name (source)
                parsed_url = urlparse(item["link"])
                source = parsed_url.netloc.replace("www.", "")

                # Generate a fake accuracy score for demonstration
                accuracy = round(random.uniform(50, 99), 2)

                news_links.append({
                    "title": item["title"],
                    "link": item["link"],
                    "source": source,
                    "accuracy": f"{accuracy}%"
                })
        return news_links
    except Exception as e:
        return {"error": str(e)}

# Function to verify news using Google Fact Check API
def fact_check_news(query):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={GOOGLE_FACT_CHECK_API_KEY}"
    response = requests.get(url)
    
    try:
        results = response.json()
        fact_checks = []
        if "claims" in results:
            for claim in results["claims"]:
                fact_checks.append({
                    "text": claim["text"],
                    "claimant": claim.get("claimant", "Unknown"),
                    "rating": claim["claimReview"][0]["textualRating"] if "claimReview" in claim else "Unknown",
                    "source": claim["claimReview"][0]["publisher"]["name"] if "claimReview" in claim else "Unknown"
                })
        return fact_checks
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        news_text = data.get("news_text", "")

        print("Input News:", news_text)  # Debug Input

        # AI Model Prediction (Dummy Placeholder - Replace with actual AI model)
        predicted_result = {
            "analysis": "This news appears to be real.",
            "links": search_google_news(news_text)
        }

        # Get fact check results
        fact_check_results = fact_check_news(news_text)

        response_data = {
            "AI_Analysis": predicted_result["analysis"],
            "Trusted_News_Links": predicted_result["links"],
            "Fact_Check_Results": fact_check_results
        }

        print("Response JSON:", json.dumps(response_data, indent=4))  # Debug Response
        return jsonify(response_data)

    except Exception as e:
        print("Server Error:", str(e))  # Print error in logs
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
