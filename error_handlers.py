from colorama import Fore


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
            print(Fore.RED + f"Contact '{args[0]}' wasn't found" + Fore.RESET)
    return inner


def add_contact_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            print(
                Fore.RED + "Please use format: add {name} {phone}" + Fore.RESET)
        except ValueError:
            print(
                Fore.RED + "Phone number doesn't match the format XXXXXXXXXX(10 digits)" + Fore.RESET)
        except ContactAlreadyExistsError:
            print(
                Fore.RED + f"Contact with same name and phone number already exists" + Fore.RESET)
    return inner


def delete_contact_error(func):
    def inner(*args):
        try:
            return func(*args)
        except CommandError:
            print(Fore.RED + "Please use format: delete {name}" + Fore.RESET)
    return inner


def change_contact_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            print(
                Fore.RED + "Please use format: change {name} {old_phone} {new_phone}" + Fore.RESET)
        except ValueError:
            print(
                Fore.RED + "Phone number doesn't match the format XXXXXXXXXX(10 digits)" + Fore.RESET)
        except KeyError:
            print(Fore.RED + f"Contact '{args[0].capitalize()
                                         }' has not phone number '{args[1]}'" + Fore.RESET)
    return inner


def show_phones_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            print(Fore.RED + "Please use format: phone {name}" + Fore.RESET)
    return inner


def add_birthday_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            print(
                Fore.RED + "Please use format: add-birthday {user} {DD.MM.YYYY}" + Fore.RESET)
        except ValueError:
            print(
                Fore.RED + f"'{args[1]}' doesn't match the birthday format DD.MM.YYYY" + Fore.RESET)
    return inner


def show_birthday_error(func):
    def inner(args):
        try:
            return func(args)
        except CommandError:
            print(
                Fore.RED + "Please use format: show-birthday {user}" + Fore.RESET)
        except ValueError:
            print(Fore.RED + f"Contact has not set birthday yet" + Fore.RESET)
    return inner
