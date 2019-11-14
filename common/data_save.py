from dataclasses import dataclass
from common.exceptions import *
import json, yaml
import os


@dataclass
class User:
    username: str
    password: str
    token: str = None
    new_token: str = None


def load_yaml(address):
    with open(address, 'r') as yml:
        yml = yaml.safe_load(yml)
        return yml


def config_loader():
    with open('config.yml', 'r') as config:
        config = yaml.safe_load(config)
        return config


class Data:

    def __init__(self):
        config = config_loader()
        address = config['files']['users']
        self.mode = 'r' if os.path.exists(address) else 'w'
        self.users_file = open(address, self.mode)
        if self.mode == 'w':
            raise FileIsEmpty()
        try:
            self.users: dict = json.load(self.users_file)
            users = []
            for user in self.users:
                users.append(User(user['username'], user['password']))
            self.users = users
        except json.JSONDecodeError:
            raise FileIsEmpty()

    def get_one_user(self):
        if len(self.users) == 0:
            raise NotEnoughUsers()
        return self.users.pop()


