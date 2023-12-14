

class User:
    def __init__(self, name: str, surname: str, birth_year: int):
        self.name = name
        self.surname = surname
        self.birth_year = birth_year

    def __str__(self):
        return self.name + " " + self.surname + " " + str(self.birth_year)


