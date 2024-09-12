import json
from datetime import datetime

from utils import get_card_info, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions


def main(date_str):
    # Парсинг даты
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Получение приветствия
    greeting = get_greeting(date.hour)

    # Загрузка транзакций
    transactions = pd.read_csv("transactions.csv")

    # Получение информации о картах
    card_info = [get_card_info(transactions, card_number) for card_number in transactions["card_number"].unique()]

    # Получение топ-транзакций
    top_transactions = get_top_transactions(transactions)

    # Получение курсов валют
    currency_rates = get_currency_rates()

    # Получение цен акций
    stock_prices = get_stock_prices()

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "cards": card_info,
        "top_transactions": top_transactions.to_dict(orient="records"),
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response)


if __name__ == "__main__":
    date_str = "2023-03-15 14:30:00"
    response = main(date_str)
    print(response)
