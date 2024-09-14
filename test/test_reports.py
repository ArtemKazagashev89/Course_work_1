from datetime import datetime
import pandas as pd
from src.reports import spending_by_category
import pytest
import json

def test_spending_by_category():
    transactions = pd.DataFrame({
        'Дата операции': [datetime(2023, 6, 25), datetime(2023, 7, 10), datetime(2023, 8, 5)],
        'Категория': ['Продукты', 'Транспорт', 'Продукты'],
        'Сумма операции': [100, 150, 200]
    })

    result = json.loads(spending_by_category(transactions, 'Продукты', '2023-08-25'))
    assert result['total_spent'] == 300

def test_spending_by_category_with_date():
    transactions = pd.DataFrame({
        'Дата операции': [datetime(2023, 6, 25), datetime(2023, 7, 10), datetime(2023, 8, 5)],
        'Категория': ['Продукты', 'Транспорт', 'Продукты'],
        'Сумма операции': [100, 150, 200]
    })

    result = json.loads(spending_by_category(transactions, 'Продукты', '2023-09-01'))
    assert result['total_spent'] == 300

if __name__ == "__main__":
    pytest.main()
