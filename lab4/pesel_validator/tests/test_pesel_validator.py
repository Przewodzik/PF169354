import unittest
from lab4.pesel_validator.src.pesel_validator import PeselValidator

class TestPeselValidator(unittest.TestCase):

    def setUp(self):
        self.validator = PeselValidator()

    def test_pesel_format(self):

        self.assertTrue(PeselValidator.validate_format("44051401458"))

        self.assertFalse(PeselValidator.validate_format("123"))

        self.assertFalse(PeselValidator.validate_format("123456789012"))

        self.assertFalse(PeselValidator.validate_format("1234567890a"))

        self.assertFalse(PeselValidator.validate_format("12345-67890"))

    def test_check_digit(self):

        self.assertTrue(PeselValidator.validate_check_digit("02070803628"))

        self.assertFalse(PeselValidator.validate_check_digit("44051401358"))

    def test_birth_date(self):

        self.assertTrue(PeselValidator.validate_birth_date("02070803628"))

        self.assertFalse(PeselValidator.validate_birth_date("99023211999"))

    def test_gender(self):

        self.assertEqual(PeselValidator.get_gender("44051401359"), "M")
        self.assertEqual(PeselValidator.get_gender("02070803628"), "K")

    def test_is_valid(self):

        self.assertTrue(PeselValidator.is_valid("44051401359"))

        self.assertFalse(PeselValidator.is_valid("1234567890"))

        self.assertFalse(PeselValidator.is_valid("99023112345"))

        self.assertFalse(PeselValidator.is_valid("44051401358"))

        self.assertTrue(PeselValidator.is_valid("85851512340"))

        self.assertTrue(PeselValidator.is_valid("04610112344"))

        self.assertFalse(PeselValidator.is_valid("01222912346"))

if __name__ == '__main__':
    unittest.main()
