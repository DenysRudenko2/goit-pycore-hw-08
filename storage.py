import pickle

from base_models import AddressBook

ADDRESS_BOOK_FILE_NAME = "addressbook.pkl"


def save_data(book, filename=ADDRESS_BOOK_FILE_NAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=ADDRESS_BOOK_FILE_NAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
