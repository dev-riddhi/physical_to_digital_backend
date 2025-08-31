import random
import string

def generate_token(length: int = 16) -> str:
    
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    token = ''.join(random.choice(characters) for _ in range(length))
    return token