import re
import random
import string
from database import *

class Hash:
    lowercase_letters = {
        'a':'z','b':'y','c':'x','d':'w',
        'e':'v','f':'u','g':'t','h':'s',
        'i':'r','j':'q','k':'p','l':'o',
        'm':'n','n':'m','o':'l','p':'k',
        'q':'j','r':'i','s':'h','t':'g',
        'u':'f','v':'e','w':'d','x':'c',
        'y':'b','z':'a'
    }

    uppercase_letters = {
        'A':'Z','B':'Y','C':'X','D':'W',
        'E':'V','F':'U','G':'T','H':'S',
        'I':'R','J':'Q','K':'P','L':'O',
        'M':'N','N':'M','O':'L','P':'K',
        'Q':'J','R':'I','S':'H','T':'G',
        'U':'F','V':'E','W':'D','X':'C',
        'Y':'B','Z':'A'
    }

    spc_character = {
        '`':'+', '~':'=', '!':'-', '@':'_', '#':')', '$':'(',
        '%':'}', '^':'{', '&':']', '*':'[', ':':"'", ';':'"',
        '<':'.', '>':',', '|':'\\', '?':'/', '/':'?', '\\':'|',
        ',':'>', '.':'<', '"':';', "'":':', '[':'*', ']':'&',
        '{':'^', '}':'%', '(':'$', ')':'#', '_':'@', '-':'!',
        '=':'~', '+':'`', ' ' : 'ʡ', 'ʡ':' '
    }

    @staticmethod
    def generate_random_letters(count):
        letters = string.ascii_letters
        random_letters = [random.choice(letters) for _ in range(count)]
        return str(random.randint(10, 100)).join(random_letters)

    @staticmethod
    def hash_password(password):
        password = Hash.apply_character_transformation(password)
        p = ''

        # Append random numbers after each character
        for char in password:
            p += char + str(random.randint(10, 99))  # Numbers should be two digits

        password = p

        # Add random letters at the beginning and end
        hash_prefix = Hash.generate_random_letters(10)
        code = hash_prefix + password
        hash_suffix = Hash.generate_random_letters(10)
        code = code + hash_suffix

        return code
    
    @staticmethod
    def apply_character_transformation(password: str):
        new_password = []
        for char in password:
            if char in Hash.lowercase_letters:
                new_password.append(Hash.lowercase_letters[char])
            elif char in Hash.uppercase_letters:
                new_password.append(Hash.uppercase_letters[char])
            elif char in Hash.spc_character:
                new_password.append(Hash.spc_character[char])
            else:
                new_password.append(char)
        return "".join(new_password)

    @staticmethod
    def extract_original_password(hashed_password: str) -> str:
        stripped_password = hashed_password[10:-10]

        original_password = ''.join([stripped_password[i] for i in range(0, len(stripped_password), 3)])
        original_password = original_password[6:-6]
        
        return Hash.apply_character_transformation(original_password)
    

    
def email_is_valid(email):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid:
        return True
    else:
        return False
    
def password_is_varified(password:str, email:str):
    found_user = Session.query(User).filter(User.email == email).first()
    if found_user:
        if Hash.extract_original_password(found_user.password) == password:
            return (True, found_user.name)
        else:
            return (False, False)
    return (False, False)
    
