# test_migration.py

import unittest
import pytest

# --- Уявний код для тестування (наприклад, функція) ---
def add_one(x):
    """Додає одиницю."""
    return x + 1

# --- 1. ОРИГІНАЛЬНИЙ ТЕСТ НА unittest ---

# Приклад Mixin-класу, який надає спільний функціонал/налаштування
class LoggedMixin(object):
    """Mixin для логування або спільного налаштування/очищення."""
    def log_message(self, msg):
        print(f"[{self.__class__.__name__}] LOG: {msg}")
    
    # У unittest це викликалося б, але вимагало б ручного виклику super().setUp()
    def setUp(self):
        self.log_message("Setting up test...")


class TestUnittestExample(LoggedMixin, unittest.TestCase):
    """
    Клас успадковується від unittest.TestCase та Mixin.
    Методи починаються з test_.
    """

    def test_add_one_simple(self):
        """Перевірка простого додавання."""
        # Використання методів асерту unittest
        self.assertEqual(add_one(1), 2)
        self.assertTrue(add_one(0) == 1)
        self.log_message("Simple check passed")

    def test_add_one_negative(self):
        """Перевірка з від'ємним числом."""
        self.assertEqual(add_one(-5), -4, "Помилка для від'ємного числа")


# --- 2. МІГРОВАНИЙ ТЕСТ НА pytest ---

# Mixin залишається без змін (не успадковується від TestCase)
class LoggedMixinPytest(object):
    """Mixin для логування або спільного функціоналу в Pytest."""
    # У Pytest, налаштування краще робити через фікстури, 
    # але Mixin може надавати звичайні методи.
    def log_message(self, msg):
        print(f"[{self.__class__.__name__}] PYTEST LOG: {msg}")


class TestPytestMigration(LoggedMixinPytest):
    """
    Клас для Pytest:
    1. Починається з префікса 'Test'.
    2. НЕ успадковується від unittest.TestCase.
    3. Коректно обробляє множинне успадкування (від LoggedMixinPytest).
    """

    # Якщо клас не має __init__ і не успадковується від TestCase,
    # Pytest розпізнає його методи з префіксом test_.

    def test_add_one_simple(self):
        """
        Перевірка простого додавання.
        Використовується звичайний 'assert'.
        """
        result = add_one(1)
        # Заміна self.assertEqual(result, 2) на звичайний assert
        assert result == 2

        # Використання методу з Mixin
        self.log_message("Simple check passed in Pytest")

    @pytest.mark.parametrize("input_val, expected", [
        (0, 1),
        (-5, -4),
        (99, 100),
    ])
    def test_add_one_parametrized(self, input_val, expected):
        """
        Перевірка з параметризацією (сучасний підхід у Pytest).
        Замінює кілька окремих тестових методів.
        """
        assert add_one(input_val) == expected

        
# --- Як запустити мігрований тест ---

# Щоб запустити тести pytest, збережіть цей файл як test_migration.py 
# і виконайте в терміналі:
#
# pip install pytest
# pytest test_migration.py