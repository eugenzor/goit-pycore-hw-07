from collections import UserDict
from datetime import datetime, date, timedelta
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


class Birthday(Field):
    """Клас для зберігання дати народження у форматі DD.MM.YYYY."""

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value: str) -> None:
        try:
            parsed = datetime.strptime(value, self.DATE_FORMAT).date()
        except (TypeError, ValueError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
        self.date: date = parsed

    def __str__(self) -> str:
        return self.date.strftime(self.DATE_FORMAT)


class Record:
    """Клас для зберігання інформації про контакт (ім'я, телефони, день народження)."""

    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

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

    def add_birthday(self, birthday: str) -> None:
        """Встановлюємо день народження контакту."""
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones = "; ".join(p.value for p in self.phones)
        parts = [f"Contact name: {self.name.value}", f"phones: {phones}"]
        if self.birthday is not None:
            parts.append(f"birthday: {self.birthday}")
        return ", ".join(parts)


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

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        """Список контактів, яких потрібно привітати у найближчі `days` днів.

        Якщо день народження припадає на вихідний, дату привітання
        переносимо на наступний понеділок.
        """
        today = date.today()
        upcoming: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.date
            celebration = bday.replace(year=today.year)
            if celebration < today:
                celebration = celebration.replace(year=today.year + 1)

            if (celebration - today).days >= days:
                continue

            if celebration.weekday() == 5:
                celebration += timedelta(days=2)
            elif celebration.weekday() == 6:
                celebration += timedelta(days=1)

            upcoming.append(
                {
                    "name": record.name.value,
                    "congratulation_date": celebration.strftime("%d.%m.%Y"),
                }
            )

        return upcoming
