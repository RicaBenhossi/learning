from phonebook import Phonebook

# Unit Tests With PYTEST

Course: Testing in Python 3 by Emily Bache on Pluralsight

## Installation
- pip
  - Run in terminal: `python -m pip install pytest`
- uv
  - Run in terminal : `uv add pytest --dev`
    - it will add `pytest` as a developmente dependency to your `pyproject.toml`.

## Test Vocabulary

- Test Suite
  - It's all the tests you have implemented and could run to assure everything is ok.
- Test case
  - It's a single teste you write to validade a cenário.
- Fixture
  - Code to manage resourses that you'll need during your tests
- Runner
  - The result report of your tests.
- Units Under Test
  - the class/method/ function that you
- Assertions
  - Assertions are the validations that are executed in the middle or end of the test cases to evaluate that the actual result is as expected.
  - There are 3 types of assert:
      - ![types_of_assert.png](resources/types_of_assert.png)

## Pytest Structure

Create a python package named `tests` on your project and mark it as `Test Source Root` on Pycharm.

Inside it, create a file starting with `test_` or finishing with `_test.py`, and add your tests inside it.
E.G:

```python
import pytest

from module03 import Phonebook


def test_lookup_by_name(phonebook):
  phonebook = Phonebook()
  phonebook.add("Bob", "12345")
  number = phonebook.lookup("Bob")
  assert number == "12345"
```

### Testing Exceptions

In order to test a method that throws an exception, you should create a context manager to capture the exception. 
It is done with the `pytest.riases(Exception)`.

```python
import pytest

from module03 import Phonebook


def test_missing_name(phonebook):
  phonebook.add("Bob", "12345")
  with pytest.raises(KeyError):
    phonebook.lookup("Mary")


```

### Pytest Fixture

Pytest use the decorator `@pytest.fixture` to create its fixtures (setup and teardowm). By convention, the def name of the fixture is the resource you're returning/instantiate. 
and you should pass it as a parameter on your teste cases.

#### Setup Fixture

The decorator `@pytest.fixture` is runned first, creating the object that will be used for the test case `test_find_character`.

```python
import pytest

from src.module03.phonenumbers import Phonebook


@pytest.fixture
def phonebook():
  '''Provides an empty phonebook.'''
  phonebook = Phonebook()
  return phonebook


def test_lookup_by_name(phonebook):
  phonebook.add("Bob", "12345")
  number = phonebook.lookup("Bob")
  assert number == "12345"

```

#### Setup and Teardown Fixture

It uses the same structure, but instead of returning the object with a `return`, use `yield` to wait until the resource is released.
In the exemple bellow, the class Phonebook receive a file as an argument on `__init__` that should be destroyed after the test case finishes.

```python
import pytest

from src.module03.phonenumbers import Phonebook


@pytest.fixture
def phonebook(tmpdir):
  '''Provides an empty phonebook.'''
  phonebook = Phonebook(tmpdir)
  yield phonebook
  phonebook.clear_cache()


def test_missing_name(phonebook):
  phonebook.add("Bob", "12345")
  with pytest.raises(KeyError):
    phonebook.lookup("Mary")
```

**OBS**: the `tmpdir` passed as a parameter to Phonebook, is a builtin fixture of pytest that provides a temporary and unique directory to each test case.

To see all the fixture of a test suite, run one of the commands bellow on the terminal. If your test fixture has a docstring. it will be shown here.
```pytest --fixtures```
```python -m pytest --fixtures```

![show_fixtures.png](resources/show_fixtures.png)

**OBS**: to show all the fixtures you have in your test cases, you should th PYTHONPATH on your terminal
```shell
PYTHONPATH='<your_source_code_dir>'
```
```shell
$env:PYTHONPATH='supermarket_receipt'
```

### Parametrized Test

We can use parametrized tests when we need to test method with diferents inputs. So, intead of write different tests or 
make a lot of asserts inside a single test case, we can just make a lot of diferent entries to a single test case.

```python
import pytest

from src.module03.phonenumbers import Phonebook


@pytest.fixture
def phonebook(tmpdir):
  '''Provides an empty phonebook.'''
  phonebook = Phonebook(tmpdir)
  yield phonebook
  phonebook.clear_cache()


@pytest.mark.parametrize(
  "entry1, entry2, is_consistent", [
    (("Bob", "12345"), ("Anna", "012345"), True),
    (("Bob", "12345"), ("Anna", "12345"), False),
    (("Bob", "12345"), ("Anna", "123"), False),
  ]
)
def test_is_consistent(phonebook, entry1, entry2, is_consistent):
  phonebook.add(*entry1)
  phonebook.add(*entry2)
  assert phonebook.is_consistent() == is_consistent
```

Paramitrized testing helps to reduce duplication in the code and it's recommended when the test case (the 'act' step) 
is the same in the others test cases and we just need to vary the data we use to test.

### Organizing Your Test Code

When we deal with large projects, is common to use some special features:

#### conftest.py

It is a special modile/file that pytest recognizes, and it's the recommended module to store all your fixtrues.
All test cases inside the test module will look for fixtures inside the `confitest.py`.

#### Pytest Marks

Pytest Marks allows you to add metadata or labels to your test cases, making it easier to organize and customise your test cases.

To see all pytest markers, hjust type `python -m pytest --markers` in the terminal.

##### The `pytest.ini`

A file to store all the personal configuration to your pytest

```text
[pytest]
addopts = --strict-markers
markers = slow: Run tests that use sample data from file (deslect with '-m "not slow"')
```

The `addopts = --strict-markers` avoid users to use markers that is not listed on the markers parameter in the ini file.

##### @pytest.mark.slow

It's a pytest decorator to sinalize that the test case may be slow and can be skipped if you want.
We can use a `pytest.ini` file to configure how to run it or not.

E.G: 
This test loads a csv file that can have tons of data, and take too much time to run.

```python
import csv
import pytest
from src.module03.phonenumbers import Phonebook


@pytest.fixture
def phonebook(tmpdir):
  '''Provides an empty phonebook.'''
  phonebook = Phonebook(tmpdir)
  yield phonebook
  phonebook.clear_cache()


@pytest.mark.slow
def test_large_file(phonebook):
  with open("sample_data/sample1.csv") as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
      name = row["Name"]
      number = row["Number"]
      phonebook.add(name, number)
  assert phonebook.is_consistent()

```

Now, this test can be "skipped" when you run all the test suite, just typying `python -m pytest -m "not slow"` in the terminal.
That will deselect the test cases marked with `@pytest.mark.slow` decorator, and it will not run.

This is very helpful in test cases that tak too long to run in development environment. Just run the fast ones or run all just when you need.

##### @pytest.mark.skip

It is usefull when your test case is not ready yet, or the feature it tests is not already finished, and you don't want 
run it.

```python
import pytest

@pytest.mark.skip("Not already implemented.")
def test_new_feature():
  assert True
```

Unlike the `@pytest.mark.slow`, the `@pytest.mark.skip` can not be run. Once it's marked as a skipp test case, it will 
only run when you remove the decorator.

##### @pytest.mark.skipif

Similar to the `@pytest.mark.skip` but with a conditional.

```python
import pytest
import sys
from src.module03.phonenumbers import Phonebook


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python 3.6 or higher to run")
def test_phonebook_contain_names():
  phonebook = Phonebook()
  assert 'Bob' in phonebook.names()
```

If you're running python 3.6, this test will be skipped.

## Test Doubles

A Test Double is recommended when you want to test a code unit that has a dependency, like an object or an external tool.

So you can replace that code for a Test Doble that does and return what you need without more complexity.

It may look not productive to "re-write" a code, but, sometimes, the class/object you need is too complex to instantiate
or your code use an external API that may be caught off-line during your test. You can't take this risk, so you should 
use a Test Double to ensure that your test case has all data and tools it need inside it. In the most cases you just 
need what the API or an object returns. That's why Test Doubles are made for.


![kinds_of_test_doubles.png](resources/kinds_of_test_doubles.png)

### Stubs

Stubs allows you to set a hard coded response (or return) for a method of an object.

For exemple:
```python
from src.module05.stub.alarm import Alarm


class StubSensor:
    def sample_pressure(self):
        return 17.0


def test_alarm_is_on_at_lower_threshold():
    alarm = Alarm(StubSensor())
    alarm.check()
    assert alarm.is_alarm_on
```

In the exemple above, we created a stub of the calss Sensor (StubSensor) that Alarm needs to be constructed. For our test, doesn't 
matter what the `sample_pressure` method does, as we get a value 17.0 from it. So we hard coded te value we need as the 
return of the method `sample_pressure`.

Another exemple using Mock:
```python
from unittest.mock import Mock

from src.module05.stub.alarm import Alarm
from src.module05.stub.sensor import Sensor


def test_alarm_is_on_at_lower_threshold():
    stub = Mock(Sensor)
    stub.sample_pressure.return_value = 17.0
    alarm = Alarm(stub)
    alarm.check()
    assert alarm.is_alarm_on

```
Now we're using the python built-in `Mock` to build the stub. It does the same as the previous exemple, but more 
concisely. When you use Mock a pass the real class you want stub, Mock has access to all methods of the real class and 
can replace what is returned as we see in the code `stub.sample_pressure.return_value = 17.0`.

### Fakes

Fake is like a stub but has an implementation with logic, behavior, but is not good for production.
They're a good option when you're dealing with a files. That can be slow, so you can fake the file in memory to run 
your tests.

![replace_with_fakes.png](resources/replace_with_fakes.png)

E.g.:
```python
import io

from src.module05.fake.html_pages import HtmlPagesConverter


def test_convert_second_page():
    fake_file = io.StringIO("""\
page one
PAGE_BREAK
page two
PAGE_BREAK
page three
PAGE_BREAK
    """)
    converter = HtmlPagesConverter(fake_file)
    converted_text = converter.get_html_page(1)
    assert converted_text == "page two<br />"
```
In the exemple above, the library `io.StringIO` is replacing the real file. It has the same methods a file has but it
runs entirely on memory, which eliminates the external dependencies.

### Dummy Objects
Provides an alternative actor in place of a real object (sometimes None) in order to test our cenario.

E.g.:

````python
import pytest


def fizzbuzz(n, additional_rules):
    answer = str()
    rules = {3: "Fizz", 5:"Buzz"}
    additional_rule = {7: "Whizz"}
    if additional_rules:
        rules.update(additional_rule)

    for divisor in sorted(rules.keys()):
        if n % divisor == 0:
            answer += rules[divisor]

    if not answer:
        answer = str(n)

    return answer


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

````
In this teste case, the `test_fizzbuzz_nomal_number` will pass, but the `test_fizzbuzz_nomal_number` will break because 
it doesn't passes the new argument `additional_rules` to the function `fizzbuzz`. 

So, as this test case doesn't test the additional rules at all, we can just pass `None` as an argument.

```python
@pytest.mark.parametrize(
    "number, expected", [
        (2, "2"),
        (3, "Fizz"),
        (5, "Buzz"),
        (15, "FizzBuzz"),
    ]
)
def test_fizzbuzz_nomal_number(number, expected):
    assert fizzbuzz(number, None) == expected
```

Using a dummy on your tests usually can be a design smell on your code. In this case, the argument `additional_rules` 
should be an optional paameter in the function.

E.g.:
```python
import pytest


def fizzbuzz(n, additional_rules=None):
    answer = str()
    rules = {3: "Fizz", 5:"Buzz"}
    additional_rule = {7: "Whizz"}
    if additional_rules:
        rules.update(additional_rule)

    for divisor in sorted(rules.keys()):
        if n % divisor == 0:
            answer += rules[divisor]

    if not answer:
        answer = str(n)

    return answer


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
```
In the exemple above, we no longer need the dummy because we fiz our design smell just defining a default value to the 
`additional_rules`.

You can use a dummy when you're forced to pass a collaborator to a class or method that is not used in the scenario 
you're testing.

### Spy

A Spy records the method calls it receives, so we can assert they are correct.

E.g.:
```python
from unittest.mock import Mock, call

from src.module05.spy.discounts import DiscountManager
from src.module05.spy.model_objects import Product, User, DiscountData

def test_for_for_users_with_mock_framework():
    notifier = Mock()
    discount_manager = DiscountManager(notifier)
    product = Product("headphones")
    product.discounts = list()
    discount_details = DiscountData("10% off")
    users = [User("user1", [product]), User("user2", [product])]

    discount_manager.create_discount(product, discount_details, users)

    assert product.discounts == [discount_details]
    expected_calls = [
        call(users[0], f"You may be interested in a discount on this product! {product.name}"),
        call(users[1], f"You may be interested in a discount on this product! {product.name}"),
    ]
    notifier.notify.assert_has_calls(expected_calls)
```

The exemple above uses the Mock framework from python Unittest to build a spy. This object has a method named 
`assert_has_calls` that receive a call object in rder to check if they are called.

In this case, the Notifier object has a `notify` method that receives the user and the message, so we create a list of 
those call (in the `expected_calls` list) to use it in the `assert_has_calls`.

### Mock

A Mock knows what method calls to expect, and fails the test if they ar not correct.
It works like a spy but Mocks is told in advance about what method will be called.

E.g.:
```python
from src.module05.spy.discounts import DiscountManager
from src.module05.spy.model_objects import Product, DiscountData, User


class MockNotifier:
    def __init__(self):
        self.expected_user_notification = list()

    def notify(self, user, message):
        # Don't send any messages from the unit test, check all notifications are expected
        expected_user = self.expected_user_notification.pop(0)
        if user != expected_user:
            raise RuntimeError(f"Got notification message for unexpected user {user.name}. Was expecting notification "
                               f"for user {expected_user.name}")

    def expect_notification_to(self, user):
        self.expected_user_notification.append(user)


def test_discount_for_users():
    notifier = MockNotifier()
    discount_manager = DiscountManager(notifier)
    product = Product("headphones")
    product.discounts = list()
    discount_details = DiscountData("10% off")
    users = [User("user1", [product]), User("user2", [product])]
    notifier.expect_notification_to(users[0])
    notifier.expect_notification_to(users[1])

    discount_manager.create_discount(product, discount_details, users)

    assert product.discounts == [discount_details]
```

In the exemple above, the `notifier` has the method `expect_notification_to` that receives the users will be notified.

When the `create_discount` is called, it will call the `notifier.notify` that validates if the user is the correct one.

Using Mock, you told it in advancce what method will be called with what arguments. If these expectatiosn aren't met, 
it throws away an exception in the act part of the test, not in the assertion.

Using a Spy, raises an error afterm in the assertion part of the test.

### How to use Test Doubles

![how_to_use_test_doubles.png](resources/how_to_use_test_doubles.png)

Sumarizing, test doubles are:

- Dummy
  - Usually `None`
- Stub
  - Responds with fixed, pre-prepared data
- Fake
  - Has an implementation, but unsuitable for production
- Spy
  - Similar to Stub, bit can asssert if the test fails. 
- Mock
  - Similar to Spy but throws away an exception in the act part of the test, not in the assertion.

## Approvals

Is an alternative to `assert`. It allows us to compare 2 strings (but not only strings) through a diff.

When you run it for the first time, it will create 2 files with your data to be compared with: 
- **`your_test_file.your_test_case.received.txt`** is what the output that approval generated from your test case.
- **`your_test_file.your_test_case.approved.txt`** is the already approved output you're waiting to receive from the test case

The approval will compare this two files. If the content are the same, the test will pass.

E.g. changing from assert to approval:

Test case with assert:
```python
import pytest

from src.module06.supermarket_receipt.model_objects import SpecialOfferType


def test_no_discount(teller, cart, toothbrush, apples):
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert list() == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity
```

Test case with approval:
```python
import approvaltests

from module06.supermarket_receipt.receipt_printer import ReceiptPrinter
from src.module06.supermarket_receipt.model_objects import SpecialOfferType
 
def test_no_discount(teller, cart, toothbrush, apples):
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    receipts_as_string = ReceiptPrinter().print_receipt(receipt)
    approvaltests.verify(receipts_as_string)

```
In the exemple above, we get rid of sveral assetions for just one approval. When we pass the `receipt_as_string` to 
`approvaltests.verify`, it will create the `your_test_file.your_test_case.received.txt` to be compared with the 
`your_test_file.your_test_case.approved.txt`.

**OBS**: the `ReceiptPrinter().print_receipt(receipt)` is a class we created just to represent a receipt object as 
string.

In resume, a test case have three parts:
![three_parts_of_a_test.png](resources/three_parts_of_a_test.png)

When using approvals, we stil have these three parts, but intead of an assert, we have a diff conpasion:
![three_parts_of_an_approval_test.png](resources/three_parts_of_an_approval_test.png)

### Setup

#### Reporter

To use the approval properly, we need to pass the additiona argument `--approvaltests-use-reporter='PythonNative'` on 
the command line. Otherwise, it will raise a `RuntimeError: This machine has no reporter configuration`.
We can configure it on pycharm as well:
![approvaltests_pycharm_setup.png](resources/approvaltests_pycharm_setup.png)

#### Printer Design

It's the most important to a successfull approval testing because is the class responsable to print all data we need to 
compare.

Advices to write a good printer
- Lay out text on multiple lines;
- Exclude irrelevant details, so your test will only fail with a good reason.
- 
If the test fails and you don't understand what's going on, it's a sign that you need to improve your printer 

#### Approvaltests Config

It's a good practice to have your approved_files in a different directory under your test directory (approved_files for 
exemple). So the approvaltests needs to know where these files are, otherwise, it will create/look then in the same 
directory the test case are.

To do this, just create a `approvaltests_config.json` file in the directory and set on it a `subdirectory` option:
```json
{
  "subdirectory": "approved_files"
}
```

### Comparing Received and Approved files

When running the approval for the first time, the test will fail. That's normal because there is no approved file yet. 
So we must open both, `your_test_file.your_test_case.received.txt` and `your_test_file.your_test_case.approved.txt` 
(preferencial in a diff tool), check if the received file contains all the infos you want to validate. If it's ok, just 
apply the changes to the approved file. 

Now, the `your_test_file.your_test_case.approved.txt` will contains the correct strings to be compared with 
`your_test_file.your_test_case.received.txt`. If there is some difference between than, the test will fail.****

### Advantages of using Approvals

- Easier to understand failures, using a diff
- Easier to update approved files with a tool
- Cheaper test maintenance
- Can simplify a test case, changing several assertions in only one approval

### Verify All Aprovals

We can use approvals to check a bunch of different combinations using `approvaltests.very_all_combinations`.

```python
import approvaltests

from module06.gilded_rose.gilded_rose import Item, GildedRose


def print_item(item):
    return f"Item({item.name}, sell_in={item.sell_in}, quality={item.quality})"


def test_update_quality():
    item = Item("foo", 0, 0)
    items = [item]

    giled_rose = GildedRose(items)
    giled_rose .update_quality()

    approvaltests.verify(print_item(item))
```

The test case above tests only one combination for an item. If we have 5 itens, with 3 possibility of quality and sell 
ins, the tests could turn into a mess.

So, we can make s simple test case that can test all this variations.

```python
import approvaltests

from module06.gilded_rose.gilded_rose import Item, GildedRose


def print_item(item):
    return f"Item({item.name}, sell_in={item.sell_in}, quality={item.quality})"


def update_quality_printer(args, result):
    return f"{args} => {print_item(result)}\n"


def test_update_quality():
    names = ["foo", "Aged Brie", "Backstage passes to a TAFKAL80ETC concert", "Sulfuras, Hand of Ragnaros"]
    sell_ins = [0]
    qualities = [0, 1, 2]

    approvaltests.verify_all_combinations(
        update_quality_for_item,
        [names, sell_ins, qualities],
        formatter=update_quality_printer
    )


def update_quality_for_item(foo, sell_in, quality):
    item = Item(foo, sell_in, quality)
    items = [item]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    return item
```

The test case above will run the method `update_quality_for_item` for eache item of the lists names, sell_ins and 
qualities, combining their values. The approval file it wull generate is like this:
```
('foo', 0, 0) => Item(foo, sell_in=-1, quality=0)
('foo', 0, 1) => Item(foo, sell_in=-1, quality=0)
('foo', 0, 2) => Item(foo, sell_in=-1, quality=0)
('Aged Brie', 0, 0) => Item(Aged Brie, sell_in=-1, quality=2)
('Aged Brie', 0, 1) => Item(Aged Brie, sell_in=-1, quality=3)
('Aged Brie', 0, 2) => Item(Aged Brie, sell_in=-1, quality=4)
('Backstage passes to a TAFKAL80ETC concert', 0, 0) => Item(Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=0)
('Backstage passes to a TAFKAL80ETC concert', 0, 1) => Item(Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=0)
('Backstage passes to a TAFKAL80ETC concert', 0, 2) => Item(Backstage passes to a TAFKAL80ETC concert, sell_in=-1, quality=0)
('Sulfuras, Hand of Ragnaros', 0, 0) => Item(Sulfuras, Hand of Ragnaros, sell_in=0, quality=0)
('Sulfuras, Hand of Ragnaros', 0, 1) => Item(Sulfuras, Hand of Ragnaros, sell_in=0, quality=1)
('Sulfuras, Hand of Ragnaros', 0, 2) => Item(Sulfuras, Hand of Ragnaros, sell_in=0, quality=2)
```

See that for every name, it runs 1 quality. If we insert a new sell_in value, it will generate us 12 more scenarios.

The `approvaltests.verify_all_combinations` can help us improve our test coverage with very little addition of code. 
However, it can improve the number of test cases and the time to run it. 


## Code Coverage

The Coverage Report shows us which lines of our code are executed by out tests. If a line is not being executed, it 
could have bug in that your test is not able to catch.

### Setup

- Install `coverage` using uv or pip.

### Running Coverage

#### Terminal

To run Coverage, just type `PYTHONPATH=../src coverage run -m pytest --approvaltests-use-reporter=PythonNative` in your 
terminal. It will execute the tests, but generates a report to help us find lines of our code that's not being tested 
yet.

To see the report, just type `coverage report -m`:
![coverage_report_terminal.png](resources/coverage_report_terminal.png)

Or you can see a HTML version usig the command `coverage html`:
![coverage_report_html.png](resources/coverage_report_html.png)

In the HTML report, we can have more detailed information about the code coverage just clicking on the file. The red 
lines shows us pieces of code that are not being tested.
![coverage_report_html_detailed.png](resources/coverage_report_html_detailed.png)
![coverage_report_html_detailed02.png](resources/coverage_report_html_detailed02.png)


#### Pycharm

Pycharm can also show us the coverge os our tests. We just have to RUN WITH COVERAGE:
![pycharm_run_with_coverage.png](resources/pycharm_run_with_coverage.png)

The results will be dispalyed in the Coverage session:
![pycharm_coverage_session.png](resources/pycharm_coverage_session.png)

As in the HTML file, clicking on the file will open it. Now we can check, directly in the file, which line is covered 
and which is not, just looking to the gutter:
![pycharm_coverage_in_file.png](resources/pycharm_coverage_in_file.png)


### Branch Coverage

Altough we get 100% coverage of our code, there might be some part of then that are note properly or fully tested in 
all combinations. To ensure that we're not missing a spot, we can use branch coverage.

Branch coverage marks the conditionals of your code that is covered but only in one way.

![branch_coverage.png](resources/branch_coverage.png)
