import re

from field import Field


class Birthday(Field):
    def __init__(self, birthday):
        if re.match(r'\d{2}\.\d{2}\.\d{4}', birthday):
            super().__init__(birthday)
        else:
            raise ValueError(
                f"'{birthday}' doesn't match the birthday format DD.MM.YYYY")
