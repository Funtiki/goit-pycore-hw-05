"""Модуль містить функцію caching_fibonacci, яка за допомогою замикання
кешує вже обчислені числа Фібоначчі."""

from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Створює замикання з кешем і повертає функцію fibonacci(n)."""
    # Створюємо порожній словник для зберігання результатів
    cache = {}

    def fibonacci(n: int) -> int:
        """Рекурсивно обчислює n-е число Фібоначчі з використанням кешу."""
        # Базові випадки рекурсії
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Перевіряємо, чи є результат у кеші
        if n in cache:
            return cache[n]

        # Обчислюємо число Фібоначчі рекурсивно
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        # Повертаємо збережений результат
        return cache[n]

    # Повертаємо внутрішню функцію
    return fibonacci


if __name__ == "__main__":
    # Отримуємо функцію fibonacci
    fib = caching_fibonacci()

    # Перевіряємо роботу функції
    print(fib(10))  # 55
    print(fib(15))  # 610
    print(fib(20))  # 6765


