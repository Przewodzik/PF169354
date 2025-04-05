import unittest

from lab6.src.utils import StringUtils, ListUtils


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.string_utils = StringUtils()

    def test_reverse_string(self):
        self.assertEqual(self.string_utils.reverse_string("hello"), "olleh")
        self.assertEqual(self.string_utils.reverse_string(""), "")
        self.assertEqual(self.string_utils.reverse_string("a"), "a")

    def test_count_vowels(self):
        self.assertEqual(self.string_utils.count_vowels("hello"), 2)
        self.assertEqual(self.string_utils.count_vowels("AEIOU"), 5)
        self.assertEqual(self.string_utils.count_vowels("xyz"), 0)

    def test_is_palindrome(self):
        self.assertFalse(self.string_utils.is_palindrome("hello"))
        self.assertTrue(self.string_utils.is_palindrome("madam"))
        self.assertTrue(self.string_utils.is_palindrome("racecar"))
        self.assertTrue(self.string_utils.is_palindrome("Kobyła ma mały bok"))
        self.assertFalse(self.string_utils.is_palindrome("To nie jest palindrom"))

    def test_to_uppercase(self):
        self.assertEqual(self.string_utils.to_uppercase("hello"), "HELLO")
        self.assertEqual(self.string_utils.to_uppercase("HELLO"), "HELLO")
        self.assertEqual(self.string_utils.to_uppercase(""), "")

    def test_to_lowercase(self):
        self.assertEqual(self.string_utils.to_lowercase("HELLO"), "hello")
        self.assertEqual(self.string_utils.to_lowercase("hello"), "hello")
        self.assertEqual(self.string_utils.to_lowercase(""), "")

class TestListUtils(unittest.TestCase):
    def setUp(self):
        self.list_utils = ListUtils()

    def test_find_max(self):
        self.assertEqual(self.list_utils.find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(self.list_utils.find_max([-5, -2, -10]), -2)
        self.assertIsNone(self.list_utils.find_max([]))

    def test_find_min(self):
        self.assertEqual(self.list_utils.find_min([1, 2, 3, 4, 5]), 1)
        self.assertEqual(self.list_utils.find_min([-5, -2, -10]), -10)
        self.assertIsNone(self.list_utils.find_min([]))

    def test_calculate_average(self):
        self.assertEqual(self.list_utils.calculate_average([1, 2, 3, 4, 5]), 3)
        self.assertEqual(self.list_utils.calculate_average([-5, -3, -10]), -6)
        self.assertEqual(self.list_utils.calculate_average([]), None)
        self.assertEqual(self.list_utils.calculate_average([1]), 1)

    def test_remove_duplicates(self):
        self.assertEqual(self.list_utils.remove_duplicates([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(self.list_utils.remove_duplicates([]), [])
        self.assertEqual(self.list_utils.remove_duplicates([1,1,1,1,1]), [1])
        self.assertEqual(self.list_utils.remove_duplicates([1,1,1,2,2,3,3]), [1,2,3])

    def test_sort_ascending(self):
        self.assertEqual(self.list_utils.sort_ascending([1,2,3,4]), [1,2,3,4])
        self.assertEqual(self.list_utils.sort_ascending([4,3,2,1]), [1,2,3,4])
        self.assertEqual(self.list_utils.sort_ascending([]), [])
        self.assertEqual(self.list_utils.sort_ascending([1,1,1,1,1]), [1,1,1,1,1])
        self.assertEqual(self.list_utils.sort_ascending([-5,2,3,6,-10,12]), [-10,-5,2,3,6,12])

    def test_sort_descending(self):
        self.assertEqual(self.list_utils.sort_descending([1, 2, 3, 4]), [4,3,2,1])
        self.assertEqual(self.list_utils.sort_descending([4, 3, 2, 1]), [4,3,2,1])
        self.assertEqual(self.list_utils.sort_descending([]), [])
        self.assertEqual(self.list_utils.sort_descending([1, 1, 1, 1, 1]), [1, 1, 1, 1, 1])
        self.assertEqual(self.list_utils.sort_descending([-5, 2, 3, 6, -10, 12]), [12,6,3,2,-5,-10])
