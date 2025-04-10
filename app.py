from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/notion-crawl", methods=["GET"])
def crawl_notion():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        blocks = soup.select('div[data-block-id]')
        texts = [block.get_text(strip=True) for block in blocks if block.get_text(strip=True)]
        return jsonify({"blocks": texts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)