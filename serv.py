from flask import Flask, request, jsonify
from datetime import datetime
import json
import logging
import os

app = Flask(__name__)

# --- Налаштування логування ---
# Встановлюємо формат часу для лог-файлу
LOG_FILE = 'system_reports.log'
# Якщо лог-файл не існує, створюємо його, щоб уникнути помилок
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'a').close()

# Налаштовуємо основний логер Python
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
print(f"Сервер налаштовано на логування даних у файл: {LOG_FILE}")
# -----------------------------

@app.route('/system-reports', methods=['POST'])
def receive_data():
    """Обробляє POST-запити, отримує JSON та логує його."""
    
    # 1. Перевірка, чи запит містить дані у форматі JSON
    if not request.is_json:
        # Повертаємо помилку 400 Bad Request, якщо Content-Type неправильний
        return jsonify({"message": "Помилка: очікується Content-Type: application/json"}), 400

    try:
        # 2. Отримуємо JSON-тіло запиту як словник Python
        data = request.get_json()
        
        # 3. Додаємо метадані сервера (час отримання)
        received_timestamp = datetime.now().isoformat()
        data['server_received_at'] = received_timestamp
        
        # 4. Логуємо дані:
        #   a) У консоль
        print("\n--- Отримано новий звіт ---")
        print(f"Час отримання: {received_timestamp}")
        print(f"Хост: {data.get('network', {}).get('hostname', 'N/A')}")
        print(f"Платформа: {data.get('system_os', {}).get('platform', 'N/A')}")
        print("Повні дані:")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        print("----------------------------")
        print(data)
        #   b) У лог-файл (записуємо як один рядок JSON)
        logging.info(json.dumps(data, ensure_ascii=False))

        # 5. Повертаємо успішну відповідь 201 Created
        return jsonify({
            "status": "success",
            "message": "Дані успішно отримані та залоговані",
            "timestamp": received_timestamp
        }), 201

    except Exception as e:
        # Обробка помилок при парсингу JSON або інша помилка
        error_message = f"Помилка обробки даних: {e}"
        logging.error(error_message)
        return jsonify({"status": "error", "message": error_message}), 500


if __name__ == '__main__':
    # Сервер буде доступний за адресою: http://127.0.0.1:5000/system-reports
    # Використовуйте '0.0.0.0' для доступу з інших комп'ютерів у локальній мережі
    print("\n🚀 Запуск Flask-сервера...")
    print("Сервер доступний за адресою: http://127.0.0.1:5000")
    print("Кінцева точка для POST-запитів: /system-reports")

    app.run(debug=False, host='0.0.0.0')

