import os

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
DB_DATABASE = os.environ.get("DB_DATABASE", "test")

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

ACCESS_TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINS", "60"))
ACCESS_TOKEN_SECRET_KEY = os.environ["ACCESS_TOKEN_SECRET_KEY"]
