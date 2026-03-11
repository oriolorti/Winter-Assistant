from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY")
print("PERPLEXITY KEY LOADED:", PERPLEXITY_KEY[:8])

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
