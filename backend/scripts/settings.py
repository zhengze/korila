import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv


class UserInfo(object):
    def __init__(self):
        # load_dotenv(find_dotenv())
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path=dotenv_path)

    def get_user(self):
        return os.getenv("USER")

    def get_password(self):
        return os.getenv("PASSWORD")


