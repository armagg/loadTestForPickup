from dataclasses import dataclass
import json, yaml
import os


@dataclass
class User:
    password: str
    username: str
    token: str
    new_token: str

def config_loader():
    with open('config.yml', 'r') as config:
        config = yaml.safe_load(config)
        return config


class Data:

    def __init__(self):
