import re

def validarPassword(psw):
    if re.findall('[!?-_.]+', psw):
        return True
    else:
        return False