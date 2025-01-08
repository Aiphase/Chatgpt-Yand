from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Конфигурация API
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"  # Убедитесь, что URL актуален
API_KEY = "your_api_key_here"  # Замените на ваш API-ключ

HEADERS = {
    "Authorization": f"Api-Key {API_KEY}",  # Используем Api-Key вместо Bearer
    "Content-Type": "application/json"
}

@app.route('/process', methods=['POST'])
def process_request():
    try:
        # Получаем данные от клиента
        data = request.json
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"error": "Input text is required"}), 400

        # Формируем запрос для Яндекс GPT
        payload = {
            "prompt": user_input,  # Используем 'prompt', согласно документации
            "temperature": 0.7,  # Контролирует разнообразие ответов
            "maxTokens": 200  # Ограничивает количество генерируемых токенов
        }

        # Отправляем запрос к API
        response = requests.post(YANDEX_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Генерирует исключение при HTTP-ошибке

        # Возвращаем ответ API
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        # Обрабатываем HTTP ошибки
        return jsonify({"error": f"HTTP error occurred: {http_err.response.status_code} {http_err.response.text}"}), 500
    except requests.exceptions.RequestException as req_err:
        # Обрабатываем другие сетевые ошибки
        return jsonify({"error": f"Request error occurred: {str(req_err)}"}), 500
    except Exception as e:
        # Обрабатываем любые другие ошибки
        return jsonify({"error": f"Unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
