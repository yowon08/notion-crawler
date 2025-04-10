import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Notion 크롤링 API입니다."

@app.route('/notion-crawl')
def crawl_notion():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'url 파라미터가 필요합니다'}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        blocks = soup.select('[class*="notion-"]')

        texts = []
        for block in blocks:
            text = block.get_text(strip=True)
            if text:
                texts.append(text)

        return jsonify({'text_blocks': texts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 🔥 여기 중요: Render가 사용하는 PORT 환경변수로 실행해야 함
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
