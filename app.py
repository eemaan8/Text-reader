from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OCR_SPACE_API_KEY = os.environ.get('OCR_SPACE_API_KEY')  # Set this in Render Dashboard

def ocr_space_file(image_bytes, api_key):
    payload = {
        'isOverlayRequired': False,
        'apikey': api_key,
        'language': 'eng',
    }
    files = {
        'filename': ('image.jpg', image_bytes),
    }
    response = requests.post('https://api.ocr.space/parse/image', data=payload, files=files)
    return response.json()

@app.route('/')
def home():
    return "ClearSight Text Reader API is running."

@app.route('/live_read', methods=['POST'])
def live_read():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    image_bytes = file.read()
    result = ocr_space_file(image_bytes, OCR_SPACE_API_KEY)

    try:
        text = result['ParsedResults'][0]['ParsedText'].strip()
    except Exception as e:
        return jsonify({'error': 'OCR failed', 'details': str(e)}), 500

    return jsonify({'detected_text': text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
