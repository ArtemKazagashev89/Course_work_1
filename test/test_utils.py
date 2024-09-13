import pytest
import json
from unittest.mock import patch, Mock
from src.utils import get_card_data, get_transactions, get_exchange_rates, get_stock_prices


# Тесты для get_card_data
def test_get_card_data():
    expected_data = [
        {"last_digits": "1234", "total_expenses": 1000, "cashback": 50},
        {"last_digits": "5678", "total_expenses": 2000, "cashback": 100},
    ]
    actual_data = json.loads(get_card_data("2023-06-01"))
    assert actual_data == expected_data


# Тесты для get_transactions
def test_get_transactions():
    expected_data = [
        {"amount": 500, "date": "2023-06-01"},
        {"amount": 400, "date": "2023-06-02"},
        {"amount": 300, "date": "2023-06-03"},
        {"amount": 200, "date": "2023-06-04"},
        {"amount": 100, "date": "2023-06-05"},
    ]
    actual_data = json.loads(get_transactions("2023-06-01"))
    assert actual_data == expected_data


# Тесты для get_exchange_rates
@patch("requests.get")
def test_get_exchange_rates(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    expected_data = {"EUR": 0.85, "GBP": 0.75}
    actual_data = json.loads(get_exchange_rates("2023-06-01"))
    assert actual_data == expected_data


@patch("requests.get", side_effect=requests.exceptions.RequestException("Mocked error"))
def test_get_exchange_rates_error(mock_get):
    expected_error = {"error": "Ошибка получения данных о курсах валют"}
    actual_data = json.loads(get_exchange_rates("2023-06-01"))
    assert actual_data == expected_error


# Тесты для get_stock_prices
@patch("requests.get")
@patch("pandas.DataFrame")
def test_get_stock_prices(mock_dataframe, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"historical": [{"date": "2023-06-01", "close": 100.0}]}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    mock_dataframe.return_value = pd.DataFrame({"date": ["2023-06-01"], "close": [100.0]})
    mock_dataframe.return_value["date"] = pd.to_datetime(mock_dataframe.return_value["date"])
    mock_dataframe.return_value = mock_dataframe.return_value.set_index("date")

    expected_data = {"2023-06-01": {"close": 100.0}}
    actual_data = json.loads(get_stock_prices("2023-06-01 12:00:00"))
    assert actual_data == expected_data


@patch("requests.get", side_effect=requests.exceptions.RequestException("Mocked error"))
def test_get_stock_prices_error(mock_get):
    expected_error = {"error": "Ошибка получения данных о ценах на акции"}
    actual_data = json.loads(get_stock_prices("2023-06-01 12:00:00"))
    assert actual_data == expected_error
