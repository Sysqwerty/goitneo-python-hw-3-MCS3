import re

from birthday import Birthday
from name import Name
from phone import Phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, contact_phone):
        if contact_phone in self.phones:
            raise Exception(f"Contactalready have phone record '{
                            contact_phone}'")
        self.phone = Phone(contact_phone)
        self.phones.append(self.phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise ValueError(f"Phone '{old_phone}' not found in the record")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone
            
    def get_phones(self):
        return [p.value for p in self.phones]

    def add_birthday(self, birthday: str):
        if re.match(r'\d{2}\.\d{2}\.\d{4}', birthday):
            self.birthday = Birthday(birthday)
        else:
            raise ValueError(
                f"'{birthday}' doesn't match the birthday format DD.MM.YYYY")
    
    def show_birthday(self):
        return self.birthday.value

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
