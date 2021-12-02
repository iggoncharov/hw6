import unittest
from unittest.mock import patch
import json
import urllib.request
import io
import coverage


API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2021-12-03
      * DD.MM.YYYY - 03.12.2021
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)


    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


class TestFunc(unittest.TestCase):
    """
    Класс для тестирования функции 'what_is_year_now'
    """
    def test_dash(self):
        """
        Тестирование записи через тире '-'
        """
        date_mock = '{"currentDateTime": "2021-12-03"}'
        with patch.object(urllib.request, 'urlopen', return_value = io.StringIO(date_mock)):
            actual = what_is_year_now()
        expected = 2021
        self.assertEqual(actual, expected)

    def test_point(self):
        """
        Тестирование записи через точку '.'
        """
        date_mock = '{"currentDateTime": "03.12.2021"}'
        with patch.object(urllib.request, 'urlopen', return_value=io.StringIO(date_mock)):
            actual = what_is_year_now()
        expected = 2021
        self.assertEqual(actual, expected)

    def test_not_delimiter(self):
        """
        Тестирование исключения через разделитель '/'
        """
        date_mock = '{"currentDateTime": "03/12/2021"}'
        with patch.object(urllib.request, 'urlopen', return_value=io.StringIO(date_mock)):
            with self.assertRaises(ValueError):
                what_is_year_now()

    def test_not_date(self):
        """
        Тестрирование исключения на произвольный текст
        """
        date_mock = '{"currentDateTime": "1 2 3 4 5 no type"}'
        with patch.object(urllib.request, 'urlopen', return_value=io.StringIO(date_mock)):
            with self.assertRaises(ValueError):
                what_is_year_now()


if __name__ == '__main__':
    unittest.main()

