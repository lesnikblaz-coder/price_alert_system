import os

from pathlib import Path
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# FHUB
FHUB_API_KEY = os.getenv("FHUB_API_KEY")

if not FHUB_API_KEY:
    raise RuntimeError("FHUB_API_KEY not found")


# AUTH
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not found")