import os
from dotenv import load_dotenv

load_dotenv()

def get_exa_api_key():
    return os.getenv("EXA_API_KEY")
