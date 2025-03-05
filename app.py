from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (Replace with actual API key)
openai.api_key = "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"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    news_text = request.form['news_text']

    # Call ChatGPT API for analysis
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Analyze this news and tell me if it's fake or real: {news_text}"}]
    )

    result = response["choices"][0]["message"]["content"]
    return jsonify({"prediction": result})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
