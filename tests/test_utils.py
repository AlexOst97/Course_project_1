import pytest
import pandas as pd
from unittest.mock import patch, Mock, mock_open
import os
from dotenv import load_dotenv
from datetime import datetime
from src.utils import greeting_by_time_of_day, filter_by_date, reading_excel_file, card_expenses
from src.utils import transaction_rating_by_amount, exchange_rate, get_price_stock, get_user_settings


load_dotenv()
API_KEY_CUR = os.getenv("API_KEY_CUR")


test_cases = [
    (datetime(2023, 10, 20, 7, 0), "Доброе утро!"),
    (datetime(2023, 10, 20, 13, 0), "Добрый день!"),
    (datetime(2023, 10, 20, 19, 0), "Добрый вечер!"),
    (datetime(2023, 10, 20, 23, 30), "Доброй ночи!"),
    (datetime(2023, 10, 20, 2, 0), "Доброй ночи!")
]


@pytest.mark.parametrize("date_now, expected_greeting", test_cases)
def test_greeting_by_time_of_day(date_now, expected_greeting):
    """Тестирование функции вывода приветствия в зависимости от времени суток"""
    assert greeting_by_time_of_day(date_now) == expected_greeting


@pytest.mark.parametrize("input_date, expected", [
    ("2021-11-03", [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0, 'Валюта платежа': 'RUB',
         'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'MCC': 5411, 'Номер карты': '*4556'},
        {'Дата платежа': '02.11.2021', 'Статус': 'OK', 'Сумма платежа': -110.0, 'Валюта платежа': 'RUB',
         'Категория': 'Фастфуд', 'Описание': 'Mouse Tail', 'MCC': 5411, 'Номер карты': '*4556'},
        {'Дата платежа': '03.11.2021', 'Статус': 'OK', 'Сумма платежа': -525.0, 'Валюта платежа': 'RUB',
         'Категория': 'Одежда и обувь', 'Описание': 'WILDBERRIES', 'MCC': 5399, 'Номер карты': '*7197'}]),
    ("", []),  # тест на пустую строку
    ("2021-12-03", []),  # тест на дату вне диапазона
    ("2021-11-01", [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0, 'Валюта платежа': 'RUB',
         'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'MCC': 5411, 'Номер карты': '*4556'}])
])
def test_filter_by_date(input_date, expected, sample_data):
    """Тестирование функции фильтрации данных по заданной дате"""
    result = filter_by_date(input_date, sample_data)
    assert result == expected


@patch('pandas.read_excel')
def test_reading_excel_file(mock_read_excel, sample_data):
    """Тестирование функции чтения из Excel файла"""
    mock_read_excel.return_value = pd.DataFrame(sample_data)
    result = reading_excel_file("mock_file.xlsx")
    expected = [
        {
            "Дата платежа": "01.11.2021",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма платежа": -228.0,
            "Валюта платежа": "RUB",
            "Категория": "Супермаркеты",
            "MCC": 5411,
            "Описание": "Колхоз"
        },
        {
            'Дата платежа': '02.11.2021',
            'Номер карты': '*4556',
            'Статус': 'OK',
            'Сумма платежа': -110.0,
            'Валюта платежа': 'RUB',
            'Категория': 'Фастфуд',
            'MCC': 5411,
            'Описание': 'Mouse Tail',
         },
        {
            "Дата платежа": "03.11.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма платежа": -525.0,
            "Валюта платежа": "RUB",
            "Категория": "Одежда и обувь",
            "MCC": 5399,
            "Описание": "WILDBERRIES"
        }
    ]
    assert result == expected
    mock_read_excel.assert_called_once_with("mock_file.xlsx")


@patch('pandas.read_excel')
def test_reading_excel_file_file_not_found(mock_read_excel):
    """Тестирование чтения Excel файла, если файл не найден"""
    mock_read_excel.side_effect = FileNotFoundError
    result = reading_excel_file("non_existing_file.xlsx")
    assert result == []


@pytest.mark.parametrize("input_data, expected", [
    (
        [{'Номер карты': '*4556', 'Сумма платежа': -228.0},
         {'Номер карты': '*4556', 'Сумма платежа': -110.0},
         {'Номер карты': '*7197', 'Сумма платежа': -525.0}],

        [{"last_digits": "4556", "total_spent": 338.0, "cashback": 3.38},
         {"last_digits": "7197", "total_spent": 525.0, "cashback": 5.25}]),

    ([], []),  # Проверка на пустой список

    ([
      {"Номер карты": "nan", "Сумма платежа": "nan"},
      {"Номер карты": float("nan"), "Сумма платежа": float("nan")},], [])
])
def test_card_expenses(input_data, expected):
    """Тестирование функции, возвращающей данные по карте"""
    result = card_expenses(input_data)
    assert result == expected


def test_transaction_rating_by_amount(mock_data):
    """Тестирование функции, возвращающей топ-5 транзакций"""
    result = transaction_rating_by_amount(mock_data)

    expected = [
        {'date': '21.03.2019', 'amount': 190044.51, 'category': 'Переводы',
         'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
        {'date': '14.05.2019', 'amount': 42965.94, 'category': 'Другое', 'description': 'ГУП ВЦКП ЖХ'},
        {'date': '28.08.2018', 'amount': 32999.0, 'category': 'Различные товары',
         'description': 'SPb Trk Atmosfera'},
        {'date': '20.05.2021', 'amount': 8626.0, 'category': 'Бонусы',
         'description': 'Компенсация покупки'},
        {'date': '30.04.2019', 'amount': 6100.0, 'category': 'Зарплата',
         'description': 'Пополнение. ООО "ФОРТУНА". Зарплата'}
    ]
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
    ([], []),  # Тест на случай, если передан пустой список транзакций
    ([  # Тестирует случай, когда все транзакции являются пополнениями
        {"Дата платежа": "01.01.2023", "Сумма платежа": 150, "Категория": "Пополнения", "Описание": "Пополнение"},
        {"Дата платежа": "02.01.2023", "Сумма платежа": 200, "Категория": "Пополнения", "Описание": "Пополнение"},
    ], [])
])
def test_transaction_rating_by_amount(input_data, expected):
    """Тестирование функции, возвращающей рейтинг транзакций по сумме"""
    result = transaction_rating_by_amount(input_data)
    assert result == expected


@pytest.fixture
def trans_1():
    return ["USD", "EUR"]


@patch('requests.get')
def test_currency_conversion(mock_get, trans_1):
    """Тестирование функции вывода курса валют"""
    mock_get.return_value.json.return_value = [
            {"currency": "USD", "rate": 99.82},
            {"currency": "EUR", "rate": 103.83}
        ]
    assert exchange_rate(trans_1) == [
            {"currency": "USD", "rate": 99.82},
            {"currency": "EUR", "rate": 103.83}
        ]


def test_exchange_rate_no_currencies():
    """Тестирование, если передан пустой список"""
    result = exchange_rate([])
    assert result == []


@patch('requests.get')
def test_get_price_stock(mock_get):
    """Тестирование функции получения данных об акциях"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "Global Quote": {"05. price": "150.25"}
    }
    mock_get.return_value = mock_response
    stocks = {"AAPL", "MSFT"}
    expected_result = [{'price': 150.25, 'stock': 'AAPL'}, {'price': 150.25, 'stock': 'MSFT'}]

    result = get_price_stock(stocks)
    assert result == expected_result


def test_get_price_stock_empty_list():
    """Тестирование, если передан пустой словарь"""
    result = get_price_stock({})
    expected = []
    assert result == expected


@patch('requests.get')
def test_get_price_stock_invalid_response(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Global Quote": {"05. price": "invalid_price"}
    }
    mock_get.return_value = mock_response
    stocks = {"GOOGL"}
    with pytest.raises(ValueError):
        get_price_stock(stocks)


@pytest.mark.parametrize("mock_data, expected", [
    ('[{"currency": "USD"}, {"stock": "AAPL"}]', [{"currency": "USD"}, {"stock": "AAPL"}]),  # Успешное чтение
    (None, []),  # Ошибка файла
    ('{"currency": "USD", "stock": AAPL}', [])  # Некорректный JSON
])
def test_get_user_settings(mock_data, expected):
    if mock_data is None:  # Обработка случая FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = get_user_settings("dummy_path.json")
            assert result == expected
    else:
        with patch("builtins.open", new_callable=mock_open, read_data=mock_data):
            result = get_user_settings("dummy_path.json")
            assert result == expected