import pytest
from .context import Memory, User

class TestMemory(object):
    url = "http://www.awesomestuff.com/this/is/a/long/url"

    def test_store_and_get_url(self):
        db = Memory()
        db.store_url("somekey", self.url)
        assert(db.get_url("somekey") == self.url)

    def test_store_raises_if_key_already_present(self):
        db = Memory()
        db.store_url("somekey", self.url)
        with pytest.raises(KeyError):
            db.store_url("somekey", "http://www.otherurl.com/foo/bar")

    def test_get_url_raises_if_key_not_present(self):
        db = Memory()
        with pytest.raises(KeyError):
            db.get_url("somekey")

    def test_has_key(self):
        db = Memory()
        db.store_url("somekey", self.url)
        assert(db.has_key("somekey") == True)
        assert(db.has_key("otherkey") == False)

    def test_store_and_get_user(self):
        db = Memory()
        user = User("test@test.com")
        db.store_user(user)
        assert(db.get_user("test@test.com") == user)
