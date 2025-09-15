from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")