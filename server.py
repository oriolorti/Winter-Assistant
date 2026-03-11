from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load Perplexity API key
PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY")

if PERPLEXITY_KEY:
    print("PERPLEXITY KEY LOADED:", PERPLEXITY_KEY[:8])
else:
    print("PERPLEXITY KEY NOT FOUND")


@app.route("/")
def home():
    return "Winter assistant is running", 200


# Simple test endpoint to verify GPT Action connectivity
@app.route("/test", methods=["POST"])
def test():
    return jsonify({
        "result": "Winter test action works correctly."
    }), 200


# Main search endpoint using Perplexity
@app.route("/search", methods=["POST"])
def search():
    try:
        body = request.get_json(force=True)
        query = body.get("query", "").strip()

        if not query:
            return jsonify({
                "result": "No query provided."
            }), 400

        if not PERPLEXITY_KEY:
            return jsonify({
                "result": "Perplexity API key is missing on the server."
            }), 500

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

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        print("PERPLEXITY STATUS:", response.status_code)
        print("PERPLEXITY RAW:", response.text[:1000])

        if response.status_code != 200:
            return jsonify({
                "result": f"Perplexity error {response.status_code}: {response.text[:500]}"
            }), 200

        result = response.json()

        answer = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not answer:
            return jsonify({
                "result": "Perplexity returned no answer."
            }), 200

        return jsonify({
            "result": answer
        }), 200

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({
            "result": f"Server error: {str(e)}"
        }), 200
