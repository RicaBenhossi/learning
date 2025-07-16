import os
from pathlib import Path


class Phonebook:

    def __init__(self, temp_dir):
        self.numbers = {}
        self.filemane = Path(temp_dir) / "phonebook.txt"
        self.cache = open(self.filemane, "w")

    def add(self, name, number):
        self.numbers[name] = number

    def lookup(self, name):
        return self.numbers[name]

    def all_names(self):
        return set(self.numbers.keys())

    def clear_cache(self):
        self.cache.close()
        os.remove(self.filemane)

    def is_consistent(self):
        for name1, number1 in self.numbers.items():
            for name2, number2 in self.numbers.items():
                if name1 == name2:
                    continue
                if number1.startswith(number2):
                    return False
        return True
