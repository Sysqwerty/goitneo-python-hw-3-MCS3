class ContactNotFoundError(Exception):
    pass


class ContactAlreadyExistsError(Exception):
    pass


class CommandError(Exception):
    pass


def contact_not_found_error(func):
    def inner(args):
        try:
            return func(args)
        except ContactNotFoundError:
            return f"Contact '{args[0]}' wasn't found"
    return inner


def add_contact_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            return "Please use format: add [name] [phone]"
        except ValueError:
            return "Phone number doesn't match the format XXXXXXXXXX(10 digits)"
        except ContactAlreadyExistsError:
            return "Contact with same phone number is already exists"
    return inner


def delete_contact_error(func):
    def inner(*args):
        try:
            return func(*args)
        except CommandError:
            return "Please use format: delete [name]"
    return inner


def change_contact_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            return "Please use format: change [name] [old_phone] [new_phone]"
        except ValueError:
            return "Phone number doesn't match the format XXXXXXXXXX(10 digits)"
    return inner


def show_phones_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            return "Please use format: phone [name]"
    return inner


def add_birthday_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            return "Please use format: add-birthday [user] [DD.MM.YYYY]"
        except ValueError:
            return f"'{args[1]}' doesn't match the birthday format DD.MM.YYYY"
    return inner


def show_birthday_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            return "Please use format: show-birthday [user]"
        except ValueError:
            return f"Contact have no set birthday yet"
    return inner
