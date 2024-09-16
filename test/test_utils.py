import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (get_exchange_rates, get_greeting, get_stock_prices, get_top_transactions,
                       get_transactions_summary)


def test_get_greeting():
    assert get_greeting(datetime(2023, 10, 1, 6, 0, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 10, 1, 12, 0, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 10, 1, 17, 0, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2023, 10, 1, 23, 0, 0)) == "Доброй ночи"


@pytest.fixture
def sample_df():
    data = {
        "Номер карты": ["1234", "1234", "5678", "5678", "5678"],
        "Сумма операции с округлением": [100.0, 150.0, 200.0, 100.0, 50.0],
        "Сумма платежа": [100.0, 150.0, 200.0, 100.0, 50.0],
    }
    return pd.DataFrame(data)


def test_get_transactions_summary(sample_df):
    summary = get_transactions_summary(sample_df)
    expected = [
        {"card_number": "1234", "total_expense": 250.0, "cashback": 2},
        {"card_number": "5678", "total_expense": 350.0, "cashback": 3},
    ]
    assert summary == expected


def test_get_top_transactions(sample_df):
    top_transactions = get_top_transactions(sample_df)
    expected = [
        {"Номер карты": "5678", "Сумма операции с округлением": 200.0, "Сумма платежа": 200.0},
        {"Номер карты": "1234", "Сумма операции с округлением": 150.0, "Сумма платежа": 150.0},
        {"Номер карты": "5678", "Сумма операции с округлением": 100.0, "Сумма платежа": 100.0},
        {"Номер карты": "1234", "Сумма операции с округлением": 100.0, "Сумма платежа": 100.0},
        {"Номер карты": "5678", "Сумма операции с округлением": 50.0, "Сумма платежа": 50.0},
    ]
    assert top_transactions == expected


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["EUR", "GBP"]}')
@patch("your_module.requests.get")
def test_get_exchange_rates(mock_get, mock_open_file):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}

    expected = {"EUR": {"EUR": 0.85}, "GBP": {"GBP": 0.75}}
    assert get_exchange_rates() == expected


@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "GOOGL"]}')
@patch("your_module.requests.get")
def test_get_stock_prices(mock_get, mock_open_file):
    mock_response = mock_get.return_value
    mock_response.json.side_effect = [[{"symbol": "AAPL", "price": 150.0}], [{"symbol": "GOOGL", "price": 2500.0}]]

    expected = {"AAPL": 150.0, "GOOGL": 2500.0}
    assert get_stock_prices() == expected
