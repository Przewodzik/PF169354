import re
import unittest

def validate_email(email):

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

class TestValidateEmail(unittest.TestCase):

    def test_validate_email(self):
        self.assertTrue(validate_email("email@example.com"))

    def test_validate_email_missing_symbol(self):
        self.assertFalse(validate_email("email_example.com"))

    def test_validate_email_missing_email(self):
        self.assertFalse(validate_email(""))

    def test_validate_email_missing_domain(self):
        self.assertFalse(validate_email("email@.com"))

    def test_validate_email_missing_name(self):
        self.assertFalse(validate_email("@example.com"))

    if __name__ == '__main__':
        unittest.main()


