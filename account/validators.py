import re

from django.core.exceptions import ValidationError


username_regex = re.compile(
    r"""
    ^                       # beginning of string
    (?!_$)                  # no only _
    (?![-.])                # no - or . at the beginning
    (?!.*[_.-]{2})          # no __ or _. or ._ or .. or -- inside
    [a-zA-Z0-9_.-]+         # allowed characters, atleast one must be present
    (?<![.-])               # no - or . at the end
    $                       # end of string
    """,
    re.X,
)


def is_safe_username(username, regex=username_regex, min_length=3):
    if len(username) < min_length:
        return False
    if not re.match(regex, username):
        return False
    
    return True
    



def validate_username(value):
    if not is_safe_username(value):
        raise ValidationError(
            f'{value} is NOT valid'
        )