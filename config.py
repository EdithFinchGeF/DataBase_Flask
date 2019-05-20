import os

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "token"
    DATABASE="Student.db"
    PAGESIZE = 14