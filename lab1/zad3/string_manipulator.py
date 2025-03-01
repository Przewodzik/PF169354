import re

class StringManipulator:

    def reverse_string(self, string):
        return string[::-1]

    def count_words(self,string):
        words = re.findall(r'\w+', string)
        return len(words)

    def capitalize_words(self,string):
        return ''.join(word.capitalize() for word in string.split())

