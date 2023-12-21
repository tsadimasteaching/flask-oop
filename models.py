import datetime


class User:
    def __init__(self, id: int, name: str, surname: str, email: str, birth_year: int):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.birth_year = birth_year

    def __str__(self):
        return str(self.id) + " " + self.name + " " + self.surname + " "  + self.email + " "+ str(self.birth_year)

    def get_age(self):
        return datetime.date.today().year - int(self.birth_year)

    age = property(fget=get_age)
