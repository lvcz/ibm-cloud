import unittest
from unittest.mock import MagicMock, Mock
import scrap


class TestScrap(unittest.TestCase):

    def setUp(self):
        self.html = """"
                            <html>
                                <body>

                                <h2>HTML Links</h2>
                                <p>HTML links are defined with the a tag: https://someUrlOutsideHref.com</p>

                                <a href="https://www.w3schools.com">This is a link</a>

                                </body>
                            </html>
                                """
        # # self.webpage = 'http://testpage.com'
        # responses.add(responses.GET, self.webpage,
        #              body=self.html, status=200)

    # def test_step_when_url_already_crawled_returns_early(self):
    #     from database import was_crawled
    #     scrap.extract_urls = Mock()
    #     was_crawled = Mock(return_value=True)
    #
    #     scrap.step('anyUrl')
    #     assert not scrap.extract_urls.called

    def test_extract_urls_finds_hrefs(self):
        expected = ["https://www.w3schools.com"]
        result = scrap.extract_urls(self.html)
        self.assertEqual(result, expected)
