from base_models import *
from storage import save_data, load_data


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as err:
            print(str(err))

    return inner


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Name and phone are required fields.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    print(message)


@input_error
def change_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        raise ValueError("Contact not found.")
    else:
        record.edit_phone(phone, args[2])
    print(message)


@input_error
def show_phones(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    else:
        phones = (o.value for o in record.phones)
        print(f"{name} phones: {', '.join(phones)}")


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record is None:
        raise ValueError("Contact not found.")
    else:
        record.add_birthday(birthday)
    print(message)


@input_error
def show_birthday_by_name(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    elif record.birthday is None:
        print(f"{name} has no birthday.")
    else:
        print(f"{name} birthday: {record.birthday}")


@input_error
def show_all(book: AddressBook):
    records = book.get_all()
    if not records:
        return "Address book is empty."

    for record in records:
        print(record)
    return


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        #  add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером,
        #  або телефонний номер к контакту який вже існує.
        elif command == "add":
            add_contact(args, book)

        #  change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
        elif command == "change":
            change_contact(args, book)

        #  phone [ім'я]: Показати телефонні номери для вказаного контакту.
        elif command == "phone":
            show_phones(args, book)


        #  all: Показати всі контакти в адресній книзі.
        elif command == "all":
            show_all(book)

        #  add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
        elif command == "add-birthday":
            add_birthday(args, book)

        #  show-birthday [ім'я]: Показати дату народження для вказаного контакту.
        elif command == "show-birthday":
            show_birthday_by_name(args, book)

        #  birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
        elif command == "birthdays":
            book.get_upcoming_birthdays()

        else:
            print("Invalid command.")

        save_data(book)


if __name__ == "__main__":
    main()


