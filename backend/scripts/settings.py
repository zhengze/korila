import os
from dotenv import load_dotenv, find_dotenv


class UserInfo(object):
    def __init__(self):
        load_dotenv(find_dotenv())

    def get_user(self):
        return os.getenv("USER")

    def get_password(self):
        return os.getenv("PASSWORD")
