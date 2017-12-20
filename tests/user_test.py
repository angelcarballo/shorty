import pytest
from .context import User

class TestUser(object):
    def test_new_users_have_a_secure_token(self):
        user = User('test@test.com')
        assert(user.secure_token)

    def test_updating_token(self):
        user = User('test@test.com')
        previous_token = user.secure_token
        user.update_token()
        assert(previous_token != user.secure_token)

