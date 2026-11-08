"""
Консольний бот-помічник для управління книгою контактів.
Дозволяє додавати, змінювати, шукати номери телефонів та переглядати
всі збережені контакти. Помилки введення обробляє декоратор input_error.
Пошук контактів не залежить від регістру імені.
"""

from functools import wraps


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.

    Перехоплює KeyError, ValueError та IndexError у функціях-обробниках
    і замість аварійного завершення повертає зрозуміле повідомлення.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Невірна кількість аргументів при розпакуванні name, phone
            return "Give me name and phone please."
        except KeyError:
            # Контакту з таким іменем немає в словнику
            return "Contact not found."
        except IndexError:
            # Команду введено без імені контакту
            return "Enter user name please."

    return inner


def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та її аргументи.

    Аргументи:
        user_input (str): Рядок вводу користувача.

    Повертає:
        tuple: Кортеж, де перший елемент — команда (str),
        а решта — аргументи.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def find_contact_name(name, contacts):
    """
    Шукає ім'я контакту в словнику без урахування регістру.

    Аргументи:
        name (str): Ім'я, яке ввів користувач.
        contacts (dict): Словник для зберігання контактів.

    Повертає:
        str | None: Ім'я у тому вигляді, в якому воно збережене,
        або None, якщо такого контакту немає.
    """
    for saved_name in contacts:
        # casefold() коректніше за lower() для порівняння рядків
        if saved_name.casefold() == name.casefold():
            return saved_name
    return None


@input_error
def add_contact(args, contacts):
    """
    Додає новий контакт до словника контактів.

    Якщо контакт із таким іменем (у будь-якому регістрі) вже існує,
    оновлює його номер замість створення дубліката.

    Аргументи:
        args (list): Список аргументів: ім'я та номер телефону.
        contacts (dict): Словник для зберігання контактів.

    Повертає:
        str: Повідомлення про успішне додавання контакту.
    """
    # Якщо аргументів не 2, виникне ValueError, який обробить декоратор
    name, phone = args
    saved_name = find_contact_name(name, contacts)
    contacts[saved_name or name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Змінює номер телефону для існуючого контакту.

    Аргументи:
        args (list): Список аргументів: ім'я та новий номер телефону.
        contacts (dict): Словник для зберігання контактів.

    Повертає:
        str: Повідомлення про оновлення контакту.
    """
    name, phone = args
    saved_name = find_contact_name(name, contacts)
    # Якщо контакт не знайдено, піднімаємо KeyError для декоратора
    if saved_name is None:
        raise KeyError(name)
    contacts[saved_name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """
    Повертає номер телефону за вказаним ім'ям контакту.

    Аргументи:
        args (list): Список аргументів, що містить ім'я контакту.
        contacts (dict): Словник для зберігання контактів.

    Повертає:
        str: Номер телефону контакту.
    """
    # Без аргументу виникне IndexError, а для невідомого імені — KeyError
    name = args[0]
    saved_name = find_contact_name(name, contacts)
    if saved_name is None:
        raise KeyError(name)
    return contacts[saved_name]


@input_error
def show_all(contacts):
    """
    Повертає всі збережені контакти з їхніми номерами телефонів.

    Аргументи:
        contacts (dict): Словник для зберігання контактів.

    Повертає:
        str: Відформатований рядок з усіма записами
        або повідомлення про їх відсутність.
    """
    if not contacts:
        return "No contacts saved."

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    """
    Головна функція програми, яка керує основним циклом обробки команд.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")

        # Захист від порожнього вводу, щоб програма не падала на split()
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

