from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY")

@app.route("/")
def home():
    return "Winter assistant is running"

@app.route("/search", methods=["POST"])
def search():

    query = request.json["query"]

    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-medium-online",
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    return jsonify(response.json())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
