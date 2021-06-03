import os

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "mongodb+srv://example:123456abc@cluster0.jqoga.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DB_DATABASE = os.environ.get("DB_DATABASE", "test")

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
