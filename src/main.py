import json
from datetime import datetime
import pandas as pd
from src.utils import (
    get_greeting,
    get_transactions_summary,
    get_top_transactions,
    get_exchange_rates,
    get_stock_prices,
)
from src.services import search_personal_transfers
from src.reports import spending_by_category
from src.views import main_page

def generate_report(date_str: str) -> str:
    """Генерирует отчет с различными данными на заданную дату."""

    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_month = date.replace(day=1)

    # Чтение данных из Excel-файла
    df = pd.read_excel("operations.xls")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y")

    # Фильтрация данных
    filtered_df = df[(df["Дата операции"] >= start_month) & (df["Дата операции"] <= date)]

    # Получение всех необходимых данных
    greeting = get_greeting(date)
    transactions_summary = get_transactions_summary(filtered_df)
    top_transactions = get_top_transactions(filtered_df)
    exchange_rates = get_exchange_rates()
    stock_prices = get_stock_prices()

    # Формируем итоговый отчет
    report = {
        "greeting": greeting,
        "transactions_summary": transactions_summary,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(report, ensure_ascii=False, indent=4)

def generate_spending_report(category: str, date: str) -> str:
    """Генерирует отчет о расходах по категории."""
    # Загружаем данные из Excel-файла
    transactions = pd.read_excel("operations.xls")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y")

    # Генерируем отчет по категории
    return spending_by_category(transactions, category, date)

if __name__ == "__main__":
    date_input = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
    report = generate_report(date_input)
    print("Отчет о финансах:")
    print(report)

    category_input = input("Введите категорию для отчета о расходах: ")
    date_category_input = input("Введите дату в формате YYYY-MM-DD для отчета о расходах: ")
    spending_report = generate_spending_report(category_input, date_category_input)
    print("Отчет о расходах по категории:")
    print(spending_report)