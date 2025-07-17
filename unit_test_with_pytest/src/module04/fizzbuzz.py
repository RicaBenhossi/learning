def fizzbuzz(input_number):
    result = str()
    if input_number % 3 == 0:
        result += "Fizz"

    if input_number % 5 == 0:
        result += "Buzz"

    if not result:
        result = str(input_number)

    return str(result)


def print_fizzbuzz(highest_number):
    fizzbuzz_numbers = (fizzbuzz(i) for i in range(1, highest_number + 1))
    for fizzbuzz_number in fizzbuzz_numbers:
        print(fizzbuzz_number)

if __name__ == "__main__":
    print_fizzbuzz(100)
