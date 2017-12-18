import pytest
from .context import UrlMinifier

class TestUrlMinifier(object):
    domain = "http://shor.ty"
    minifier = UrlMinifier(domain)

    def test_minify_and_restore(self):
        url = "http://www.awesomestuff.com/this/is/a/long/url"
        minified_url = self.minifier.minify(url)
        restored_url = self.minifier.restore(minified_url)
        assert(restored_url == url)

    def test_minify_and_restore_with_custom_url(self):
        url = "http://www.awesomestuff.com/this/is/a/long/url"
        requested_key = "custom-url"
        minified_url = self.minifier.minify(url, requested_key)
        assert(minified_url == "http://shor.ty/custom-url")
        restored_url = self.minifier.restore(minified_url)
        assert(restored_url == url)

    def test_minify_with_invalid_custom_url(self):
        url = "http://www.awesomestuff.com/this/is/a/long/url"
        requested_url = "invalid url"
        with pytest.raises(KeyError):
            self.minifier.minify(url, requested_url)

    def test_minify_with_existing_custom_url(self):
        url = "http://www.awesomestuff.com/this/is/a/long/url"
        minified_url = self.minifier.minify(url)

        url2 = "http://www.funkyvibes.com/this/is/another/long/url"
        with pytest.raises(KeyError):
            self.minifier.minify(url2, minified_url)
