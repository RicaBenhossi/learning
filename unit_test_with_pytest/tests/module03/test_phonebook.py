import pytest


def test_lookup_by_name(phonebook):
    phonebook.add("Bob", "12345")
    number = phonebook.lookup("Bob")
    assert number == "12345"


def test_all_names(phonebook):
    phonebook.add("Bob", "12345")
    assert "Bob" in phonebook.all_names()


def test_missing_name(phonebook):
    phonebook.add("Bob", "12345")
    with pytest.raises(KeyError):
        phonebook.lookup("Mary")


@pytest.mark.parametrize(
    "entry1, entry2, is_consistent", [
        (("Bob", "12345"), ("Anna", "012345"), True),
        (("Bob", "12345"), ("Sue", "12345"), False),
        (("Bob", "12345"), ("Sue", "123"), False),
    ]
)
def test_is_consistent(phonebook, entry1, entry2, is_consistent):
    phonebook.add(*entry1)
    phonebook.add(*entry2)
    assert phonebook.is_consistent() == is_consistent
