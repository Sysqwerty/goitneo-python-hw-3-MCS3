from collections import UserDict
from datetime import datetime
from typing import Dict
from collections import defaultdict

from record import Record


WEEK_DAY_DICT = {
    0: "Monday",
    1: "Tusday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        return self.get(name)

    def delete(self, name):
        self.__delitem__(name)

    def get_birthdays_per_week(self) -> dict:
        users_dictionary_per_weekday = defaultdict(list)
        current_date = datetime.today().date()
        celebrate_dict = dict()

        for user, record in self.data.items():
            if record.birthday:
                birthday_string: str = record.birthday.value
                birthday: datetime = datetime.strptime(
                    birthday_string, "%d.%m.%Y").date()
                birthday_this_year: datetime = birthday.replace(
                    year=current_date.year)

                if birthday_this_year < current_date:
                    birthday_this_year: datetime = birthday.replace(
                        year=current_date.year + 1)

                delta_days = (birthday_this_year - current_date).days

                if delta_days < 7:
                    week_day = birthday_this_year.weekday()

                    if week_day in [5, 6]:
                        week_day = 0

                    users_dictionary_per_weekday[WEEK_DAY_DICT[week_day]].append(
                        user)

        # Прінтує людей з Днем Нарождення на наступний тиждень, починаючи з понеділка
        # for day in WEEK_DAY_DICT.values():
        #     celebrate_users = ", ".join(users_dictionary_per_weekday[day])
        #     print(f"{day}: {celebrate_users}")

        for day in WEEK_DAY_DICT.values():
            celebrate_users = ", ".join(users_dictionary_per_weekday[day])
            celebrate_dict[f"{day}"] = celebrate_users

        return celebrate_dict


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")

    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("22.10.1984")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("22.10.1984")
    book.add_record(jane_record)

    # Створення та додавання нового запису для Simon
    simon_record = Record("Simon")
    simon_record.add_phone("9811234567")
    book.add_record(simon_record)

    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    # print(john)  # Виведення: Contact name: John, phones: 1112223333;

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Пошук всіх телефонів у записі John
    found_phones = john.get_phones()
    # print(found_phones)
    # ['1112223333', '5555555555']

    # Видалення запису Jane
    # book.delete("Jane")

    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # Видалення телефону "5555555555" із запису John
    john_record.remove_phone("5555555555")

    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # Виведення днів нарождення на наступний тиждень
    print(book.get_birthdays_per_week())
