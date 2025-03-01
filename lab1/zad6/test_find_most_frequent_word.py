import unittest
from collections import Counter

def find_most_frequent_word(word):

    if not word.strip():
        return ""

    word_frequency = Counter(word.split())

    return word_frequency.most_common(1)[0][0]


class TestFindMostFrequentWord(unittest.TestCase):

    def test_find_most_frequent_word(self):
        self.assertEqual(find_most_frequent_word("apple apple bannana"), "apple")

    def test_find_most_frequent_single_word(self):
        self.assertEqual(find_most_frequent_word("apple"),"apple")

    def find_most_frequent_word_in_blank_string(self):
        self.assertEqual(find_most_frequent_word(""),"")

    def test_most_frequent_word_same_frequency(self):
        self.assertEqual(find_most_frequent_word("apple apple banana banana"),"apple")

    def test_most_frequent_word_case_sensitivity(self):
        self.assertEqual(find_most_frequent_word("hello hello hello Hello Banana banana Banana "),"hello")

    if __name__ == '__main__':
        unittest.main()







