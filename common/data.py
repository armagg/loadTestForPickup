import os
import yaml
from pickle import load, dump


from common.exceptions import DoesNotUserExists, NotEnoughUsers, FileIsEmpty


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


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
        try:
            config = config_loader()
            self.address = config['files']['users']
            self.mode = 'rb' if os.path.exists(self.address) else 'wb'
            self.users_file = open(self.address, self.mode)
            if self.mode == 'wb':
                raise FileIsEmpty
            try:
                self.users = load(self.users_file)
            except (TypeError, EOFError) as ignored:
                raise FileIsEmpty()
        except FileIsEmpty:
            self.users = []

    def get_one_user(self):
        if len(self.users) == 0:
            raise NotEnoughUsers()
        return self.users.pop()

    def add_one_user(self, username, password):
        self.users.append(User(username, password))

    def save_data_added(self):
        if len(self.users) != 0:
            self.mode = 'wb'
            self.users_file = open(self.address, self.mode)
            dump(self.users, self.users_file)
            self.users_file.flush()
        else:
            raise DoesNotUserExists()

    def end(self):
        self.users_file.close()