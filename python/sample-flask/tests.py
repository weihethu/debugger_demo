import unittest
from unittest.mock import patch
import requests_mock
from web_scraping_server import scrape

class TestScrape(unittest.TestCase):
    def setUp(self):
        self.data = {'url': 'http://www.yahoo.tw/index.html'}

    @requests_mock.Mocker()
    def test_scrape(self, m):
        m.get('http://www.yahoo.tw', text='<html></html>')
        result, ok = scrape(self.data)
        self.assertTrue(ok)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
