class MissingInput(Exception):
    pass

class InvalidPassword(Exception):
    def __str__(self) -> str:
        return "Invalid password"