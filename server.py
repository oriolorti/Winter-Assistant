from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY")

if PERPLEXITY_KEY:
    print("PERPLEXITY KEY LOADED:", PERPLEXITY_KEY[:8])
else:
    print("PERPLEXITY KEY NOT FOUND")

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
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    try:
        answer = result["choices"][0]["message"]["content"]
    except Exception:
        return jsonify({
            "error": "Unexpected response from Perplexity",
            "raw": result
        }), 500

    return jsonify({
        "result": answer
    })
