import os

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "mongodb://localhost:27017/")
DB_DATABASE = os.environ.get("DB_DATABASE", "test")

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
