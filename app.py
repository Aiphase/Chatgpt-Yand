from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Конфигурация API
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"  # Замените на актуальный URL API
API_KEY = "your_api_key_here"  # Ваш API-ключ
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.json
        user_input = data.get("text", "")

        # Формируем запрос для Яндекс GPT-4
        payload = {
            "input": user_input,
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 200
            }
        }

        # Отправляем запрос
        response = requests.post(YANDEX_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
