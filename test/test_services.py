import pytest
import json
from src.services import search_personal_transfers

def test_no_transactions():
    transactions = []
    result = search_personal_transfers(transactions)
    assert result == json.dumps([], ensure_ascii=False, indent=4)

def test_no_transfers():
    transactions = [
        {"Категория": "Покупки", "Описание": "Оплата в магазине"},
        {"Категория": "Зарплата", "Описание": "Начисление зарплаты"}
    ]
    result = search_personal_transfers(transactions)
    assert result == json.dumps([], ensure_ascii=False, indent=4)

def test_no_matching_description():
    transactions = [
        {"Категория": "Переводы", "Описание": "Перевод на карту"},
        {"Категория": "Переводы", "Описание": "Оплата услуг"},
    ]
    result = search_personal_transfers(transactions)
    assert result == json.dumps([], ensure_ascii=False, indent=4)

def test_single_match():
    transactions = [
        {"Категория": "Переводы", "Описание": "Перевод Иванов И."},
        {"Категория": "Покупки", "Описание": "Оплата в магазине"},
    ]
    expected_result = json.dumps([{"Категория": "Переводы", "Описание": "Перевод Иванов И."}], ensure_ascii=False, indent=4)
    result = search_personal_transfers(transactions)
    assert result == expected_result

def test_multiple_matches():
    transactions = [
        {"Категория": "Переводы", "Описание": "Перевод Иванов И."},
        {"Категория": "Переводы", "Описание": "Перевод Смирнов С."},
        {"Категория": "Покупки", "Описание": "Оплата в магазине"},
        {"Категория": "Переводы", "Описание": "Оплата услуг"}
    ]
    expected_result = json.dumps(
        [
            {"Категория": "Переводы", "Описание": "Перевод Иванов И."},
            {"Категория": "Переводы", "Описание": "Перевод Смирнов С."}
        ],
        ensure_ascii=False,
        indent=4
    )
    result = search_personal_transfers(transactions)
    assert result == expected_result