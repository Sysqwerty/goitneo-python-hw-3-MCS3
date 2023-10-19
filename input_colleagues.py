from datetime import datetime
from typing import Dict
from collections import defaultdict

week_day_dict = {
    0: "Monday",
    1: "Tusday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

weekand = [5, 6]

users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 10)},
    {"name": "Jillian Bunch", "birthday": datetime(1984, 10, 11)},
    {"name": "Morgan Freeman", "birthday": datetime(2000, 11, 8)},
    {"name": "John Doe", "birthday": datetime(1955, 10, 28)},
    {"name": "Ales Parvales", "birthday": datetime(1955, 10, 13)},
    {"name": "Billie Eilish", "birthday": datetime(1955, 10, 7)},
    {"name": "Captain Morgan", "birthday": datetime(1955, 10, 9)},
    {"name": "John Keepbey", "birthday": datetime(1955, 10, 8)},
]
output_example = {'Monday': ['Bill Gates'], 'Thursday': ['Jan Koum']}


def get_birthdays_per_week(users: list(Dict[str, datetime])):
    users_dictionary_per_weekday = defaultdict(list)
    current_date = datetime.today().date()

    for user in users:
        user_name = user["name"]
        birthday: datetime = user["birthday"].date()
        birthday_this_year: datetime = birthday.replace(year=current_date.year)

        if birthday_this_year < current_date:
            birthday_this_year: datetime = birthday.replace(
                year=current_date.year + 1)

        delta_days = (birthday_this_year - current_date).days

        if delta_days < 7:
            week_day = birthday_this_year.weekday()

            if week_day in weekand:
                week_day = 0

            users_dictionary_per_weekday[week_day_dict[week_day]].append(
                user_name)

    for day in week_day_dict.values():
        celebrate_users = ", ".join(users_dictionary_per_weekday[day])
        print(f"{day}: {celebrate_users}")


if __name__ == '__main__':
    get_birthdays_per_week(users)
