import re

def is_alphanumeric(s:str):
    try:
        return bool(re.match("^[a-zA-Z0-9]", s))
    except ValueError:
        raise "Cant enter symbols into the name field."