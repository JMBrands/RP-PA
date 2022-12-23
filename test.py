import re
from random import randint
string1 = f"{randint(0,100)},{randint(0,100)}"
def check(str_in):
    regex = re.compile("[0-9]+(\.){1}[0-9]+\Z", re.I)
    match = regex.match(str(str_in))
    return bool(match)
print(string1, "\n", check(string1))
