from address_book import AddressBook
from record import Record


class ContactNotFoundError(Exception):
    pass


class ContactAlreadyExistsError(Exception):
    pass


book: AddressBook

commands: dict = {
    "help": "shows available commands",
    "hello": "prints 'How can I help you?'",
    "add [user] [phone]": "adds new contact (phone is 10-digits)",
    "delete [user]": "deletes contact from the Address Book",
    "change [user] [old_phone] [new_phone]": "changes exist contact phone number",
    "phone [user]": "shows exist contact's phone numbers",
    "all": "shows all exist contacts from Address Book",
    "add-birthday [user] [birthday]": "adds birthday to a contact in format [DD.MM.YYYY]",
    "show-birthday [user]": "shows user's birthday",
    "birthdays": "shows birthdays on next week",
    "exit": "enter 'close' or 'exit' to close the assistant",
}


def add_contact_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return "Please use format: add [name] [phone]"

    return inner


def delete_contact_error(func):
    def inner(contact_name):
        try:
            return func(contact_name)
        except ValueError:
            return "Please use format: delete [name]"

    return inner


def change_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args)
        except ValueError:
            return "Please use format: change [name] [phone]"
        except ContactNotFoundError:
            return f"Contact wasn't found"

    return inner


def show_phones_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ContactNotFoundError:
            return f"User wasn't found"

    return inner


def help():
    sorted_commands = dict(sorted(commands.items(), key=lambda item: item[0]))
    formatted_commands = ""
    for key, value in sorted_commands.items():
        formatted_commands += f">>> {key: <40}: {value: <}\n"
    return formatted_commands


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@add_contact_error
def add_contact(args: list[str, str]):
    contact_name, contact_phone = args
    contact_name = contact_name.capitalize()
    if (book.find(contact_name)):
        record = book.find(contact_name)
    else:
        record: Record = Record(contact_name)

    record.add_phone(contact_phone)
    book.add_record(record)

    return f"Contact added: {contact_name} {contact_phone}"


@delete_contact_error
def delete_contact(contact_name):
    try:
        contact_name = contact_name[0].capitalize()
    except:
        return "Please use format: delete [name]"
    if (book.find(contact_name)):
        book.delete(contact_name)
    else:
        return (f"Contact '{contact_name}' wasn't found")
    return f"Contact deleted: {contact_name}"


@change_contact_error
def change_contact(args: list[str, str, str]):
    contact_name, old_phone, new_phone = args
    contact_name = contact_name.capitalize()
    if book.find(contact_name):
        record: Record = book.find(contact_name)
        record.edit_phone(old_phone, new_phone)

        return f"Contact updated: '{contact_name} {new_phone}'."
    else:
        raise ContactNotFoundError


@show_phones_error
def show_phones(args):
    try:
        contact_name = args[0].capitalize()
    except:
        return "Please use format: phone [name]"

    if book.find(contact_name):
        return book.find(contact_name).get_phones
    else:
        raise ContactNotFoundError


def show_all():
    for name, record in book.data.items():
        return record


def add_birthday(args):
    try:
        contact_name, birthday = args
        contact_name = contact_name.capitalize()
    except:
        return "Please use format: add-birthday [user] [DD.MM.YYYY]"
    if book.find(contact_name):
        record: Record | None = book.find(contact_name)
    else:
        return f"Contact wasn't found"
    record.add_birthday(birthday)
    return "Birthday added"


def show_birthday(args):
    try:
        contact_name = args[0]
        contact_name = contact_name.capitalize()
    except:
        return "Please use format: show-birthday [user]"
    if book.find(contact_name):
        record: Record | None = book.find(contact_name)
    else:
        return f"Contact wasn't found"
    if record.show_birthday():
        birthday = record.show_birthday()
    else:
        return f"Contact {contact_name} have no set birthday yet"
    return f"Contact {contact_name} birthday: {birthday}"


def birthdays():
    get_birthdays_per_week = book.get_birthdays_per_week()
    if get_birthdays_per_week:
        print("\n".join([f"{day}: {', '.join(celebrate_users)}" for day,
                         celebrate_users in get_birthdays_per_week.items() if celebrate_users]))
    else:
        return "There is noone to celebrate birthday next week"


def main():
    """
    Assistanse bot helps to collect and manage user contacts.

    To see available commands use 'help' command
    """
    print("Welcome to the assistant bot!\nEnter a command or 'help' to see available commands.")

    global book
    # стровення нової адресної книги (TODO: додати read fromm file)
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
                print(add_contact(args))
            case "delete":
                print(delete_contact(args))
            case "change":
                print(change_contact(args))
            case "phone":
                print(show_phones(args))
            case "all":
                print(show_all())
            case "add-birthday":
                print(add_birthday(args))
            case "show-birthday":
                print(show_birthday(args))
            case "birthdays":
                birthdays()
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
