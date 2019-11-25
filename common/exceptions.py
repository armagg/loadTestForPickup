class FileIsEmpty(Exception):
    pass


class TokenExpires(Exception):
    pass

class NotFoundFile(FileNotFoundError):
    pass

class NotEnoughUsers(Exception):
    pass
