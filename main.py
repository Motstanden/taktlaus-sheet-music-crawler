import os
from dotenv import load_dotenv
from typing import Tuple

def clear_terminal():
    os.system('clear')

def setup_environment() -> Tuple[str, str]:
    load_dotenv(verbose=True)
    username = os.getenv('TAKTLAUS_USERNAME')
    password = os.getenv('TAKTLAUS_PASSWORD')
    return username, password 

if __name__ == "__main__":
    clear_terminal()
    username, password = setup_environment()
    print(username, password)

    