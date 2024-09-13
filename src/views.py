import json
from utils import get_greeting, get_card_data, get_transactions, get_exchange_rates, get_stock_prices


def get_main_page_data(date_str):
    """Генерирует JSON-ответ с данными для веб-страницы "Главная".

    Args:
    date_str (str): Строка с датой и временем в формате YYYY-MM-DD HH:MM:SS.

    Returns:
    str: JSON-ответ с данными для "Главной".
    """
    try:
        greeting = get_greeting(date_str)
        card_data = get_card_data()
        transactions = get_transactions()
        exchange_rates = get_exchange_rates()
        stock_prices = get_stock_prices(date_str)

        # Предполагается, что функции возвращают строку JSON или уже подготовленные данные
        data = {
            "приветствие": greeting,
            "открытки": json.loads(card_data) if isinstance(card_data, str) else card_data,
            "транзакции": json.loads(transactions) if isinstance(transactions, str) else transactions,
            "exchange_rates": json.loads(exchange_rates) if isinstance(exchange_rates, str) else exchange_rates,
            "stock_prices": json.loads(stock_prices) if isinstance(stock_prices, str) else stock_prices,
        }

        return json.dumps(data, ensure_ascii=False)  # Убедитесь, что кириллица экспортируется корректно
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return json.dumps({"error": "Ошибка при декодировании JSON: " + str(e)}, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка генерации главной страницы: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)  # Вернуть ошибку в формате JSON


# Пример использования
if __name__ == "__main__":
    date_str = "2023-06-01 12:00:00"
    main_page_data = get_main_page_data(date_str)
    print(main_page_data)
