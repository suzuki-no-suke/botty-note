import unittest
import marko


class TestMarkoUsage(unittest.TestCase):
    def test_usages(self):
        source = """
# title

## テスト

  * NO1
  * NO2
"""
        html = marko.convert(source)
        self.assertIn('<h1>title</h1>', html)
        self.assertIn('<h2>テスト</h2>', html)
        self.assertIn('<li>NO1</li>', html)
        self.assertIn('<li>NO2</li>', html)
