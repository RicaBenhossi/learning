import pytest

from src.module03.phonenumbers import Phonebook


@pytest.fixture
def phonebook(tmpdir):
    '''Provides an empty phonebook.'''
    phonebook = Phonebook(tmpdir)
    yield phonebook
    phonebook.clear_cache()
