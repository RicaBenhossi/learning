import pytest

from fake_catalog import FakeCatalog
from module06.supermarket_receipt.model_objects import Product, ProductUnit
from module06.supermarket_receipt.shopping_cart import ShoppingCart
from module06.supermarket_receipt.teller import Teller


@pytest.fixture
def toothbrush():
    return Product("toothbrush", ProductUnit.EACH)


@pytest.fixture
def apples():
    return Product("apples", ProductUnit.KILO)


@pytest.fixture
def catalog(toothbrush, apples):
    catalog = FakeCatalog()
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    return catalog


@pytest.fixture
def teller(catalog):
    return Teller(catalog)


@pytest.fixture
def cart():
    return ShoppingCart()
