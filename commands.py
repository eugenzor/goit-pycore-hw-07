from functools import wraps

from models import AddressBook, Record


class CommandError(Exception):
    """Помилка виконання команди, яку потрібно показати користувачу."""


def input_error(func):
    """Перехоплюємо типові помилки введення та піднімаємо CommandError."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise CommandError("Contact not found.")
        except ValueError as exc:
            message = str(exc)
            raise CommandError(message if message else "Give me name and phone please.")
        except IndexError:
            raise CommandError("Enter the argument for the command.")

    return wrapper


def parse_input(user_input: str) -> tuple[str, ...]:
    """Розділяємо введений рядок на команду та аргументи."""
    if not user_input.strip():
        return ("",)
    command, *args = user_input.split()
    return (command.strip().lower(), *args)


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    (name,) = args[:1] or [""]
    if not name:
        raise IndexError
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    if not record.phones:
        return f"{name} has no phone numbers."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(_: list[str], book: AddressBook) -> str:
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and birthday (DD.MM.YYYY) please.")
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    (name,) = args[:1] or [""]
    if not name:
        raise IndexError
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    if record.birthday is None:
        return f"{name} has no birthday set."
    return str(record.birthday)


@input_error
def birthdays(_: list[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )
