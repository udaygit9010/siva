from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (Replace with actual API key)
openai.api_key = "your_openai_api_key"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    news_text = request.json['news_text']

    # Ask ChatGPT if the news is real or fake
    chatgpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fact-checking AI that determines if news is real or fake."},
            {"role": "user", "content": f"Can you analyze this news and tell me if it's real or fake? News: '{news_text}'"}
        ]
    )

    response_text = chatgpt_response["choices"][0]["message"]["content"]

    return jsonify({"chatgpt_response": response_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
