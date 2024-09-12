from datetime import datetime

import pandas as pd
import requests


def get_greeting(time):
    if time < 12:
        return "Доброе утро"
    elif time < 18:
        return "Добрый день"
    elif time < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_info(transactions, card_number):
    # Фильтрация транзакций по карте
    card_transactions = transactions[transactions["card_number"] == card_number]

    # Расчет общей суммы расходов
    total_spent = card_transactions["amount"].sum()

    # Расчет кешбэка
    cashback = total_spent * 0.01

    return {"last_digits": card_number[-4:], "total_spent": total_spent, "cashback": cashback}


def get_top_transactions(transactions, n=5):
    # Сортировка транзакций по сумме платежа
    transactions = transactions.sort_values(by="amount", ascending=False)

    # Выборка топ-n транзакций
    top_transactions = transactions.head(n)

    return top_transactions


def get_currency_rates():
    # Получение курсов валют от API
    response = requests.get("https://api.exchangerate-api.com/v4/latest/RUB")
    data = response.json()
    rates = data["rates"]

    return rates


def get_stock_prices():
    # Получение цен акций от API
    response = requests.get("https://api.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=demo")
    data = response.json()
    price = data["Global Quote"]["05. price"]

    return price
