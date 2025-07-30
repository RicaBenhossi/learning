'''
input -> output
1 -> 1
2 -> 2
3 -> Fizz
5 -> Buzz
15 ->-FizzBuzz
'''
import pytest

from module04.fizzbuzz import fizzbuzz, print_fizzbuzz


@pytest.mark.parametrize(
    "input_number, fizzbuzz_number", [
        (1, "1"),
        (2, "2"),
        (4, "4"),
        (98, "98"),
    ]
)
def test_fizzbuzz_normal_number(input_number, fizzbuzz_number):
    assert fizzbuzz(input_number) == fizzbuzz_number


@pytest.mark.parametrize(
    "input_number", [3, 6, 9, 99]
)
def test_fizzbuzz_is_fizz(input_number):
    assert fizzbuzz(input_number) == "Fizz"


@pytest.mark.parametrize(
    "input_number", [5, 10, 20, 95]
)
def test_fizzbuzz_is_buzz(input_number):
    assert fizzbuzz(input_number) == "Buzz"


@pytest.mark.parametrize(
    "input_number", [15, 30, 45, 60, 90]
)
def test_fizzbuzz_is_fizzbuzz(input_number):
    assert fizzbuzz(input_number) == "FizzBuzz"


def test_print_fizzbuzz(capsys):
    print_fizzbuzz(3)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == "1\n2\nFizz\n"
