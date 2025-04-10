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

        # Notion의 주요 텍스트 블록 찾기
        blocks = soup.select('[class*="notion-"]')

        texts = []
        for block in blocks:
            text = block.get_text(strip=True)
            if text:
                texts.append(text)

        return jsonify({'text_blocks': texts})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
