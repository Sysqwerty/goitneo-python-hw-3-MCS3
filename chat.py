from classes import Name, Phone, Birthday, Record, AddressBook
from error_handlers import add_contact_error, delete_contact_error, change_contact_error, show_phones_error, contact_not_found_error, add_birthday_error, show_birthday_error, CommandError, ContactAlreadyExistsError, ContactNotFoundError


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
    "show-birthday [user]": "shows user's birthday date",
    "birthdays": "shows birthdays on next week",
    "exit": "enter 'close' or 'exit' to close the assistant",
}


def help():
    sorted_commands = dict(sorted(commands.items(), key=lambda item: item[0]))
    formatted_commands = ""

    for key, value in sorted_commands.items():
        formatted_commands += f">>> {key: <40}: {value: <}\n"

    return formatted_commands


def parse_input(user_input: str):
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
    except:
        return "help", ""

    return cmd, *args


@add_contact_error
def add_contact(args: list[str, str]):
    try:
        name, phone = args
        name = Name(name.capitalize())
    except:
        raise CommandError

    try:
        phone = Phone(phone)
    except:
        raise ValueError

    if book.find(name):
        contact = book.find(name)

        if not phone.value in contact.get_phones():
            record: Record = contact.add_phone(phone)
        else:
            raise ContactAlreadyExistsError
    else:
        record: Record = Record(name, phone)
        book.add_record(record)

    return f"Contact added successfully: {name} {phone}"


@contact_not_found_error
@delete_contact_error
def delete_contact(args):
    try:
        name = Name(args[0].capitalize())
    except:
        raise CommandError

    if (book.find(name)):
        book.delete(name)
    else:
        raise ContactNotFoundError

    return f"Contact '{name}' deleted successfully"


@contact_not_found_error
@change_contact_error
def change_contact(args: list[str, str, str]):
    try:
        name, old_phone, new_phone = args
        name = Name(name.capitalize())
    except:
        raise CommandError
    try:
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
    except:
        raise ValueError

    if book.find(name):
        record: Record = book.find(name)
        record.edit_phone(old_phone, new_phone)
        return f"Contact '{name}' updated successfully"
    else:
        raise ContactNotFoundError


@contact_not_found_error
@show_phones_error
def show_phones(args):
    try:
        name = Name(args[0].capitalize())
    except:
        raise CommandError

    if book.find(name):
        return f"{name.value}: {', '.join(book.find(name).get_phones())}"
    else:
        raise ContactNotFoundError


@contact_not_found_error
@add_birthday_error
def add_birthday(args):
    try:
        name, birthday = args
        name = Name(name.capitalize())
    except:
        raise CommandError

    try:
        birthday = Birthday(birthday)
    except:
        raise ValueError

    if book.find(name):
        record: Record = book.find(name)
        record.add_birthday(birthday)
    else:
        raise ContactNotFoundError

    return "Birthday added successfully"


@contact_not_found_error
@show_birthday_error
def show_birthday(args):
    try:
        name = args[0]
        name = Name(name.capitalize())
    except:
        raise CommandError

    if book.find(name):
        record: Record = book.find(name)
    else:
        raise ContactNotFoundError

    if record.birthday:
        birthday = record.show_birthday()
    else:
        raise ValueError

    return f"{name} birthday: {birthday}"


def show_all():
    if book.data:
        result = list()
        for record in book.data.values():
            result.append(str(record))
        return "\n".join(result)
    else:
        return "No contacts have been added yet"


def birthdays():
    get_birthdays_per_week = book.get_birthdays_per_week()

    if get_birthdays_per_week:
        # celebrates = {k:v for }

        result = "Next week birthdays:\n" + "-" * 10 + "\n"
        result += "\n".join([f"{day}: {celebrate_users}" for day,
                             celebrate_users in get_birthdays_per_week.items()])
        result += "\n" + "-" * 10
        return result
    else:
        return "There is no one to celebrate birthday next week"


def main():
    """
    Assistanse bot helps to collect and manage user contacts.

    To see available commands enter 'help' command
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
                print(birthdays())
            case "close" | "exit":
                print("Good bye!")
                break
            case _:
                print("Invalid command. Please try again")


if __name__ == "__main__":
    main()
