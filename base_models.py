from collections import UserDict
import re
import datetime as dt
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        if not name:
            raise ValueError("Name is required field")
        super().__init__(name)


class Phone(Field):
    #  10 digits phone number
    phone_pattern = re.compile(r"^\d{10}$")

    def __init__(self, phone):
        if not phone:
            raise ValueError("Name is required field")
        if not self.phone_pattern.match(phone):
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(phone)

    def __str__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, value):
        pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
        if not pattern.match(value):
            raise ValueError("Invalid date format. Use DD-MM-YYYY")
        try:
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = (Birthday(birthday))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value
        if name in self.data:
            raise ValueError(f"Record name {name} already set")

        self.data[name] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.data = state

    def get_all(self):
        return self.data.values()

    def get_upcoming_birthdays(self):
        celebrators = []
        for user in self.data.values():
            if user.birthday is None:
                continue

            parsed_birthday = dt.datetime.strptime(user.birthday.value, '%d-%m-%Y').date()
            today = dt.date.today()

            # Add a day or two for congratulation date if birthday is on a weekend:
            def calculate_congrats_day(date: datetime.date):
                if date.weekday() == 5:
                    return date + dt.timedelta(days=2)
                elif date.weekday() == 6:
                    return date + dt.timedelta(days=1)
                return date

            # Check b-day this year:
            this_year_birthday = parsed_birthday.replace(year=today.year)
            if this_year_birthday >= today:
                if 0 <= (this_year_birthday - today).days <= 7:
                    this_year_birthday = calculate_congrats_day(this_year_birthday)
                    celebrators.append({'name': user.name.value, 'congratulation_date': this_year_birthday.__str__()})
                continue

            # Check if less than 7 days left to the new year:
            if today.month == 12 and today.day > 25:
                # Check b-day next year:
                next_year_birthday = parsed_birthday.replace(year=today.year + 1)
                if (next_year_birthday - today).days <= 7:
                    next_year_birthday = calculate_congrats_day(next_year_birthday)
                    celebrators.append({'name': user['name'], 'congratulation_date': next_year_birthday})

        print(celebrators)
