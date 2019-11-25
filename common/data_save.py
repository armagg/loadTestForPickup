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


class LoadData:

    def __init__(self):
        config = config_loader()
        self.file_address = config['files']['users']
        if not os.path.exists(self.file_address):
            raise NotFoundFile
        self.users_file = open(self.file_address, 'r')
        try:
            self.users = json.load(self.users_file)
        except json.JSONDecodeError:
            raise FileIsEmpty()

    def get_one_user(self):
        if len(self.users) == 0:
            return NotEnoughUsers
        return self.users.pop()


class CreatUsers:
    def __init__(self):
        self.users = []
        config = config_loader()
        self.file_address = config['files']['users']
        if os.path.exists(self.file_address):
            self.mode = 'r+'
        else:
            self.mode = 'w'
