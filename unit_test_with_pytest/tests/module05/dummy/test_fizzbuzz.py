import pytest

from src.module05.dummy.fizzbuzz import fizzbuzz


@pytest.mark.parametrize(
    "number, expected", [
        (2, "2"),
        (3, "Fizz"),
        (5, "Buzz"),
        (15, "FizzBuzz"),
    ]
)
def test_fizzbuzz_nomal_number(number, expected):
    assert fizzbuzz(number) == expected


@pytest.mark.parametrize(
    "number, additional_rules, expected", [
        (7, {7: "Whizz"}, "Whizz"),
    ]
)
def test_fizzbuzz_nomal_number(number, additional_rules, expected):
    assert fizzbuzz(number, additional_rules) == expected
