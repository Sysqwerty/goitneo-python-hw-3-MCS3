from address_book import AddressBook
from record import Record


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


commands: dict = {
    "help": "shows available commands",
    "hello": "prints 'How can I help you?'",
    "add [user] [phone]": "adds new contact",
    "change [user] [phone]": "changes exist contact phone number",
    "phone [user]": "prints exist contact phone number",
    "all": "prints all exist contacts",
    "add-birthday": "adds birthday to a contacct",
    "show-birthday"
    "exit": "enter 'close' or 'exit' to close the assistant",
}


def add_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: add [name] [phone]"
        except UserAlreadyExistsError:
            return f"Contact is already exist"

    return inner


def change_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: change [name] [phone]"
        except UserNotFoundError:
            return f"User wasn't found"

    return inner


def show_phone_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: phone [user]"
        except UserNotFoundError:
            return f"User wasn't found"

    return inner


def help():
    formatted_commands = ""
    for key, value in commands.items():
        formatted_commands += f"==> {key}: {value}\n"
    return formatted_commands


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@add_contact_error
def add_contact(args: list[str, str], contacts: dict):
    name, phone = args
    name = name.capitalize()
    if (contacts.get(name)):
        raise UserAlreadyExistsError
    else:
        book.add_record(Record())
        contacts[name] = phone
        return f"Contact added: {name} {phone}"


@change_contact_error
def change_contact(args: list[str, str], contacts: dict):
    name, phone = args
    name = name.capitalize()
    if contacts.get(name):
        contacts[name] = phone
        return f"Contact updated: '{name} {phone}'."
    else:
        raise UserNotFoundError


@show_phone_error
def show_phone(args: list[str, str], contacts: dict):
    try:
        name: str = args[0].capitalize()
    except IndexError:
        return "Please use format: phone [user]"

    if contacts.get(name):
        return contacts.get(name)
    else:
        raise UserNotFoundError


def show_all(contacts: dict):
    return contacts


def main():
    """
    Assistanse bot takes a commmand from user input and executes available commands.

    It can add, change, show desired or all added phone contacts

    To see available commands use 'help' command
    """
    contacts = {}
    print("Welcome to the assistant bot! Enter a command or 'help' to see available commands.")

    book = AddressBook()

    while True:
        user_input: str = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "help":
                print(help())
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "phone":
                print(show_phone(args, contacts))
            case "all":
                print(show_all(contacts))
            case "add-birthday":
                pass
            case "show-birthday":
                pass
            case "birthdays":
                pass
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
