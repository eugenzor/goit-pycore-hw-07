from collections import UserDict
from typing import Optional


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""

    def __init__(self, value: str) -> None:
        """Ім'я не може бути порожнім."""
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією формату."""

    def __init__(self, value: str) -> None:
        """Перевіряємо формат номера перед збереженням."""
        if not Phone.is_valid(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def is_valid(value: str) -> bool:
        """Номер має складатися рівно з 10 цифр."""
        return isinstance(value, str) and len(value) == 10 and value.isdigit()


class Record:
    """Клас для зберігання інформації про контакт (ім'я та список телефонів)."""

    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додаємо новий телефон у список."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляємо телефон зі списку, якщо він існує."""
        existing = self.find_phone(phone)
        if existing is None:
            raise ValueError(f"Phone {phone} not found")
        self.phones.remove(existing)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінюємо значення існуючого телефону на нове."""
        existing = self.find_phone(old_phone)
        if existing is None:
            raise ValueError(f"Phone {old_phone} not found")
        if not Phone.is_valid(new_phone):
            raise ValueError("Phone number must contain exactly 10 digits")
        existing.value = new_phone

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Повертаємо об'єкт Phone за значенням або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання та керування записами адресної книги."""

    data: dict[str, Record]

    def add_record(self, record: Record) -> None:
        """Ключем у словнику виступає ім'я контакту."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Шукаємо запис за ім'ям, повертаємо None якщо не знайдено."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляємо запис за ім'ям, якщо він існує."""
        if name in self.data:
            del self.data[name]
