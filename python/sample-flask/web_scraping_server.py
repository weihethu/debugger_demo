from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process():
    if not request.json or 'data' not in request.json:
        return jsonify({'error': 'No data provided'}), 400
    
    page_html, ok = scrape(request.json['data'])
    if not ok:
        return jsonify({'error': 'Failed to fetch the URL'}), 400
    return jsonify({'result': str(page_html)}), 200

url_regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

def scrape(data):
    url = data['url']

    # normalize the url to remove the trailing index.html if present
    normalizeUrl = url
    if url.endswith('/index.html'):
        normalizeUrl = url.rstrip('/index.html')
    
    
    if normalizeUrl == "":
        raise ValueError("URL is empty after normalization")

    if not re.match(url_regex, normalizeUrl):
        raise ValueError("URL is not valid")
    
    response = requests.get(normalizeUrl)

    if response.status_code != 200:
        return None, False

    scraped_data = BeautifulSoup(response.text, 'html.parser')
    return scraped_data, True

if __name__ == '__main__':
    app.run(debug=True, port=8080)
