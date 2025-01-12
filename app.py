import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Конфигурация API
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"  # URL API
API_KEY = "your_api_key_here"  # Ваш API-ключ
FOLDER_ID = "your_folder_id_here"  # Идентификатор каталога
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/', methods=['POST'])
def process_request():
    try:
        # Получаем входные данные от клиента
        data = request.json
        user_input = data.get("text", "")  # Убедитесь, что ключ совпадает с фронтендом

        if not user_input:
            return jsonify({"error": "Input text is required"}), 400

        # Формируем тело запроса к API
        payload = {
            "text": "Привет! Как дела?",  # Здесь используется "text", как требуется API
            "temperature": 0.7,
            "max_tokens": 200,
            "top_p": 0.9,
            "stop": ["\n"],
            "folderId": FOLDER_ID  # Добавляем идентификатор каталога
        }

        # Отправляем запрос к API
        response = requests.post(YANDEX_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        # Возвращаем ответ от API
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    # Use PORT environment variable
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
    
