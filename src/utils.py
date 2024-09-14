import json
from datetime import datetime
from typing import List, Dict, Any, Union
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")


def get_greeting(date: datetime) -> str:
    """Возвращает приветствие на основе времени суток."""

    hour = date.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_transactions_summary(df: pd.DataFrame) -> List[Dict[str, Union[str, float, int]]]:

    """Возвращает сводку транзакций для каждой карты, включая общие расходы и кэшбэк."""

    summary = []
    for card_number, group in df.groupby("Номер карты"):
        total_expense = group["Сумма операции с округлением"].sum()
        cashback = int(total_expense / 100)
        summary.append({"card_number": card_number, "total_expense": total_expense, "cashback": cashback})
    return summary


def get_top_transactions(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает топ 5 транзакций по сумме платежа."""

    top_transactions = df.nlargest(5, "Сумма платежа")
    return top_transactions.to_dict(orient="records")


def get_exchange_rates() -> Dict[str, Dict[str, float]]:
    """Возвращает текущие курсы обмена для валют, указанных в файле настроек пользователя."""

    with open("user_settings.json") as f:
        settings = json.load(f)

    user_currencies = settings["user_currencies"]
    exchange_rates = {}
    for currency in user_currencies:
        response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency}&base=USD&apikey={API_KEY}"
        )
        data = response.json()
        exchange_rates[currency] = data["rates"]
    return exchange_rates


def get_stock_prices() -> Dict[str, float]:
    """Возвращает текущие цены на акции, указанные в файле настроек пользователя."""

    with open("user_settings.json") as f:
        settings = json.load(f)

    user_stocks = settings["user_stocks"]
    stock_prices = {}
    for stock in user_stocks:
        response = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={STOCK_API_KEY}")
        data = response.json()
        if data:
            stock_prices[stock] = data[0]["price"]

    return stock_prices
