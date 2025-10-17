import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASS = os.getenv("NEO4J_PASS")

settings = Settings()
