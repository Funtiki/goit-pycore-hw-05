"""Модуль містить генератор generator_numbers для пошуку дійсних чисел
у тексті та функцію sum_profit для підрахунку загального прибутку.

Для обчислень використовується Decimal замість float, оскільки йдеться
про фінансові розрахунки, де похибки округлення неприпустимі.
"""

import re
from decimal import Decimal
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[Decimal, None, None]:
    """Знаходить у тексті всі дійсні числа й по одному віддає їх як Decimal.

    Числа записані без помилок і відокремлені пробілами з обох боків.
    """
    # (?<!\S) та (?!\S): перед числом і після нього немає непробільного
    # символу. Це працює і на початку чи в кінці рядка
    pattern = r"(?<!\S)\d+\.\d+(?!\S)"

    for match in re.finditer(pattern, text):
        # Decimal створюємо з рядка, а не з float: float уже містить
        # похибку двійкового представлення (наприклад, 0.1 + 0.2)
        yield Decimal(match.group())


def sum_profit(
    text: str,
    func: Callable[[str], Generator[Decimal, None, None]],
) -> Decimal:
    """Підсумовує всі числа, які повертає генератор func для тексту."""
    # Початкове значення Decimal("0") потрібне, щоб результат був Decimal,
    # а не int: sum() за замовчуванням починає з 0
    return sum(func(text), Decimal("0"))


def main() -> None:
    """Демонструє роботу generator_numbers та sum_profit."""
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими "
        "надходженнями 27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # Загальний дохід: 1351.46


if __name__ == "__main__":
    main()
