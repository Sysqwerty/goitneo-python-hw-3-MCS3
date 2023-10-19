from address_book import AddressBook


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
    "exit": "enter 'close' or 'exit' to close the assistant",
}


def help():
    formatted_commands = ""
    for key, value in commands.items():
        formatted_commands += f"==> {key}: {value}\n"
    return formatted_commands


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: add [name] [phone]"
        except UserAlreadyExistsError:
            return f"Contact is already exist"

    return inner


@add_contact_error
def add_contact(args: list[str, str], contacts: dict):
    name, phone = args
    name = name.capitalize()
    if (contacts.get(name)):
        raise UserAlreadyExistsError
    else:
        contacts[name] = phone
        return f"Contact added: {name} {phone}"


def change_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: change [name] [phone]"
        except UserNotFoundError:
            return f"User wasn't found"

    return inner


@change_contact_error
def change_contact(args: list[str, str], contacts: dict):
    name, phone = args
    name = name.capitalize()
    if contacts.get(name):
        contacts[name] = phone
        return f"Contact updated: '{name} {phone}'."
    else:
        raise UserNotFoundError


def show_phone_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please use format: phone [user]"
        except UserNotFoundError:
            return f"User wasn't found"

    return inner


@show_phone_error
def show_phone(args: list[str, str], contacts: dict):
    name: str = args[0].capitalize()
    phone: str = contacts.get(name)
    if contacts.get(name):
        return phone
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
    while True:
        user_input: str = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "help":
            print(help())
        elif command == "hello":
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
