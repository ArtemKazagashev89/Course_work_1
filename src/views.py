import json
from datetime import datetime
from typing import Dict
import pandas as pd
from src.utils import (
    get_greeting,
    get_transactions_summary,
    get_top_transactions,
    get_exchange_rates,
    get_stock_prices,
)

def main_page(date_str: str) -> str:
    """Формирует главную страницу с различными данными на заданную дату."""

    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_month = date.replace(day=1)

    # Чтение данных из Excel-файла
    df = pd.read_excel("operations.xls")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y")

    # Фильтрация данных
    filtered_df = df[(df["Дата операции"] >= start_month) & (df["Дата операции"] <= date)]

    # Приветствие пользователя в зависимости от времени суток
    greeting = get_greeting(date)

    # Сбор данных по транзакциям и кешбэку
    transactions_summary = get_transactions_summary(filtered_df)

    # Получение топ-5 транзакций
    top_transactions = get_top_transactions(filtered_df)

    # Получение курсов валют и стоимости акций
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    # Формируем ответ JSON
    response = {
        "greeting": greeting,
        "transactions_summary": transactions_summary,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response)