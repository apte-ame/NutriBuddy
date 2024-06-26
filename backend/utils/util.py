from datetime import datetime
import os
import bcrypt
import time
from jose import jwt
from datetime import datetime, timedelta
import os
import openai
import csv

def generate_file_name():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"file_{timestamp}.pdf"

def is_pdf(filename: str) -> bool:
    """Check if the filename has a PDF extension"""
    _, extension = os.path.splitext(filename)
    return extension.lower() == ".pdf"

openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def parse_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(access_token):
    decoded_token = jwt.decode(
        access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token

def get_data():
    file_path = os.getenv("CSV_FILE_PATH")
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(dict(row))
    return data


def compare_time(token_time: int):
    if int(time.time()) < token_time:
        return True
    else:
        return False

