from typing import List, Tuple
import unittest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows

class TestFitTransform(unittest.TestCase):
    """
    Класс для тестирования функции fit_transform()
    """

    def test_equal(self):
        """
        Проверка верности работы функции fit_transform() на равенство
        """
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        transformed_cities = fit_transform(cities)
        exp_transformed_cities = [
            ('Moscow', [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow', [0, 0, 1]),
            ('London', [1, 0, 0]),
        ]
        self.assertEqual(transformed_cities, exp_transformed_cities)

    def test_in(self):
        """
        Проверяет, содержит ли в выводе fit_transform() часть верного ответа
        """
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        transformed_cities = fit_transform(cities)
        exp_city_in = ('Moscow', [0, 0, 1])
        self.assertIn(exp_city_in, transformed_cities)

    def test_not_in(self):
        """
        Проверяет, что в выводе не содержится неверное значение
        """
        cities = ['Moscow', 'New York', 'Moscow', 'London']
        transformed_cities = fit_transform(cities)
        exp_city_in = ('Paris', [0, 0, 1])
        self.assertNotIn(exp_city_in, transformed_cities)

    def test_empty(self):
        """
        Проверка на пустой список
        """
        cities = []
        transformed_cities = fit_transform(cities)
        exp_transformed_cities = []
        self.assertEqual(transformed_cities, exp_transformed_cities)

    def test_error_empty(self):
        """
        Проверка исключение на 0 аргументов
        """
        with self.assertRaises(TypeError):
            fit_transform()


if __name__ == '__main__':
    from pprint import pprint

    cities = ['Moscow', 'New York', 'Moscow', 'London']
    exp_transformed_cities = [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]
    transformed_cities = fit_transform(cities)
    pprint(transformed_cities)
    assert transformed_cities == exp_transformed_cities