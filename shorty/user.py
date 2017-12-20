import secrets

class User(object):
    def __init__(self, email):
        self.email = email
        self.update_token()

    def update_token(self):
        self.secure_token = self.__generate_token()

    def __generate_token(self):
        return secrets.token_urlsafe()

