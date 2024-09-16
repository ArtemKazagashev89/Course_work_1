import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Вычисляет общую сумму расходов по указанной категории за последние три месяца."""

    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    start_date = date - timedelta(days=90)

    # Фильтруем данные за последние три месяца и по указанной категории
    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    # Получаем итоговую сумму
    total_spent = filtered["Сумма операции"].sum()

    result = {
        "category": category,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": date.strftime("%Y-%m-%d"),
        "total_spent": total_spent,
    }

    logging.info(f"Report generated for category: {category}")

    return json.dumps(result, ensure_ascii=False)


def report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор, который сохраняет результат работы функции в файл JSON."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> str:
            result = func(*args, **kwargs)
            if filename:
                file_name = filename
            else:
                file_name = f"report_{func.__name__}.json"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(result)
            return result

        return wrapper

    return decorator


# Пример использования декоратора
@report_to_file(filename="category_report.json")
def spending_by_category_report(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Вычисляет общую сумму расходов по указанной категории за последние три месяца и сохраняет отчет в файл. """

    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    start_date = date - timedelta(days=90)

    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    total_spent = filtered["Сумма операции"].sum()

    result = {
        "category": category,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": date.strftime("%Y-%m-%d"),
        "total_spent": total_spent,
    }

    logging.info(f"Report generated for category: {category}")

    return json.dumps(result, ensure_ascii=False)


# Загрузка данных из файла Excel
transactions = pd.read_excel("../data/operations.xlsx")

# Преобразуем даты из строк в объект datetime, чтобы с ними было удобно работать
transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
