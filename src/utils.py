import requests
import json
import logging
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загрузка переменных окружения
load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")


def get_greeting(date_str):
    """Возвращает приветствие в зависимости от времени."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
        if 5 <= hour < 12:
            return "Доброе утро!"
        elif 12 <= hour < 18:
            return "Добрый день!"
        else:
            return "Добрый вечер!"
    except ValueError as e:
        logging.error(f"Ошибка при парсинге даты: {e}")
        return "Некорректная дата"


def get_card_data():
    """Возвращает информацию о картах в формате JSON."""
    card_data = [
        {"last_digits": "1234", "total_expenses": 1000, "cashback": 50},
        {"last_digits": "5678", "total_expenses": 2000, "cashback": 100},
    ]
    return json.dumps(card_data)


def get_transactions():
    """Возвращает топ-5 транзакций по сумме платежа."""
    transactions = [
        {"amount": 500, "date": "2023-06-01"},
        {"amount": 400, "date": "2023-06-02"},
        {"amount": 300, "date": "2023-06-03"},
        {"amount": 200, "date": "2023-06-04"},
        {"amount": 100, "date": "2023-06-05"},
    ]
    return json.dumps(transactions)


def get_exchange_rates():
    """Возвращает данные о курсах валют из внешнего сервиса."""
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/USD?key={API_KEY}")
        response.raise_for_status()
        data = response.json()
        return json.dumps(data["rates"])
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении данных о курсах валют: {e}")
        return json.dumps({"error": "Ошибка получения данных о курсах валют"})


def get_stock_prices(date_str):
    """Возвращает данные о ценах на акции из внешнего сервиса."""
    try:
        date_only_str = date_str.split()[0]  # Извлекаем только дату из строки даты и времени
        response = requests.get(
             f"https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EIXIC?serietype=line&from=2023-01-01&to={date_only_str}&apikey={STOCK_API_KEY}"
        )
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["historical"])
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
            return json.dumps(df.to_dict(orient="index"))
        else:
            return json.dumps({"error": "Нет данных о ценах акций"})
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении данных о ценах на акции: {e}")
        return json.dumps({"error": "Ошибка получения данных о ценах на акции"})


# Пример использования функций
if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(get_greeting(current_date))
    print(get_card_data())
    print(get_transactions())
    print(get_exchange_rates())
    print(get_stock_prices(current_date))
