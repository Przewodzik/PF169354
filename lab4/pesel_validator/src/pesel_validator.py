"""This module validates Pesel """
import re
import datetime

class PeselValidator:
    """Class representing a Pesel Validator"""

    @staticmethod
    def validate_format(pesel: str) -> bool:
        """
        Validates if the PESEL number format is valid(exactly 11 digits).

        Args:
            pesel (str): PESEL number to validate

        Returns:
            bool: True if the format is valid (exactly 11 digits),
                  False otherwise
        """

        pattern = r'^\d{11}$'

        return bool(re.match(pattern, pesel))

    @staticmethod
    def validate_check_digit(pesel: str) -> bool:
        """
        Validates if the PESEL number has a correct check digit.

        Args:
            pesel (str): PESEL number to validate

        Returns:
            bool: True if the check digit is valid, False otherwise
        """

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        sum_digits = 0

        for i in range(10):
            sum_digits += (int(pesel[i]) * weights[i]) % 10

        return (10 - (sum_digits % 10)) % 10 == int(pesel[-1])

    @staticmethod
    def validate_birth_date(pesel: str) -> bool:
        """
        Validates if the birthdate encoded in the PESEL number is valid.

        Args:
            pesel (str): PESEL number to validate

        Returns:
            bool: True if the birthdate is valid, False otherwise
        """

        year = int(pesel[0:2])
        month = int(pesel[2:4])
        day = int(pesel[4:6])

        if 1 <= month <= 12:
            year += 1900

        elif 21 <= month <= 32:
            year += 2000
            month = month - 20
        elif 41 <= month <= 52:
            year += 2100
            month = month - 40

        elif 61 <= month <= 72:
            year += 2200
            month = month - 60

        elif 81 <= month <= 92:
            year += 1800
            month = month - 80

        try:
            datetime.date(year, month, day)
        except ValueError:
            return False

        return True

    @staticmethod
    def get_gender(pesel: str) -> str:
        """
        Extracts the gender information from a PESEL number.

        Args:
            pesel (str): PESEL number to process

        Returns:
            str: 'K' for female, 'M' for male
        """

        return 'K' if int(pesel[-2]) % 2 == 0 else 'M'



    @staticmethod
    def is_valid(pesel: str) -> bool:
        """
        Performs complete validation of a PESEL number.

        Args:
            pesel (str): PESEL number to validate

        Returns:
            bool: True if the PESEL number is valid in all aspects, False otherwise
        """

        return (
                PeselValidator.validate_format(pesel) and
                PeselValidator.validate_birth_date(pesel) and
                PeselValidator.validate_check_digit(pesel)
        )
