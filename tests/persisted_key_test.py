import pytest
from .context import PersistedKey
from .context import Memory

class DummyDb(Memory):
    def __init__(self, num_fails=5):
        self.num_fails = num_fails
        self.forced_errors = 0

    def store_url(self, key, url):
        # import pdb; pdb.set_trace() 
        if self.forced_errors == self.num_fails:
            return True
        else:
            self.forced_errors += 1
            raise KeyError("Forced error")

class TestPersistedKey(object):
    url = "https://www.monkeyisland.com/you/fight/like/a/cow"

    def test_minify_and_restore(self):
        strategy = PersistedKey()
        key = strategy.minify(self.url)
        assert(strategy.restore(key) == self.url)

    def test_minify_and_restore_custom_key(self):
        strategy = PersistedKey()
        strategy.minify(self.url, "foobar")
        assert(strategy.restore("foobar") == self.url)

    def test_max_key_length(self):
        strategy = PersistedKey(max_len=10)
        assert(len(strategy.minify(self.url)) <= 10)
        strategy = PersistedKey(max_len=3)
        assert(len(strategy.minify(self.url)) <= 3)

    def test_retry_on_existing_key(self):
        strategy = PersistedKey(retries=3, db=DummyDb(num_fails=3))
        with pytest.raises(KeyError):
            strategy.minify(self.url)

        strategy = PersistedKey(retries=4, db=DummyDb(num_fails=3))
        #TODO assert no exception is raised
        assert(strategy.minify(self.url) != False)

    def test_valid_key(self):
        strategy = PersistedKey(max_len=10)
        assert(strategy.valid_key("abcABC123"))
        assert(not strategy.valid_key("no spaces"))
        assert(not strategy.valid_key("abc-%-abc"))
        assert(strategy.valid_key("1234567890"))
        assert(not strategy.valid_key("1234567890X"))

