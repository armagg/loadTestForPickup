from dataclasses import dataclass


@dataclass
class Users:
    password: str
    username: str
    token: str
    new_token: str
