import json
import logging
import re

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def search_personal_transfers(transactions):
    """Функция для поиска переводов физическим лицам в транзакциях."""

    # Регулярное выражение для поиска имени и первой буквы фамилии
    pattern = re.compile(r"\\b[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\\.\\b")

    # Отфильтровать транзакции категории "Переводы" с описанием соответствующим регулярному выражению
    filtered_transactions = [
        transaction
        for transaction in transactions
        if transaction.get("Категория") == "Переводы" and pattern.search(transaction.get("Описание", ""))
    ]

    # Логирование количества найденных транзакций
    logger.debug(f"Найдено {len(filtered_transactions)} переводов физическим лицам.")

    # Возвращаем результат в формате JSON
    return json.dumps(filtered_transactions, ensure_ascii=False, indent=4)
