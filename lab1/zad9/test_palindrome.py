import unittest
import re

def is_palindrome(s):

    s = re.sub(r'\W', '', s)

    return s == s[::-1]


class TestPalindrome(unittest.TestCase):

    def test_palindrome(self):
        self.assertTrue(is_palindrome("kajak"))
        self.assertTrue(is_palindrome("radar"))
        self.assertTrue(is_palindrome("zakaz"))
        self.assertFalse(is_palindrome("hello"))

    def test_long_palindrome(self):
        self.assertTrue(is_palindrome("może jutro ta dama sama da tortu jeżom"))

    def test_empty_palindrome(self):
        self.assertTrue(is_palindrome(""))

    def test_single_char_palindrome(self):
        self.assertTrue(is_palindrome("t"))
        self.assertTrue(is_palindrome("z"))

    if __name__ == '__main__':
        unittest.main()
