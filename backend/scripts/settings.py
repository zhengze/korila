import os
from dotenv import load_dotenv, find_dotenv


class UserInfo(object):
    def __init__(self):
        # load_dotenv(find_dotenv())
        load_dotenv(dotenv_path="../.env")
        pass

    @staticmethod
    def get_user():
        return os.getenv("USER")

    @staticmethod
    def get_password():
        return os.getenv("PASSWORD")


if __name__ == "__main__":
    userinfo = UserInfo()
    print userinfo.get_user()
