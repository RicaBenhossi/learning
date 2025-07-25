from dataclasses import dataclass, field


@dataclass
class DiscountData:
    name: str


@dataclass
class Product:
    name: str
    discounts: list[DiscountData] = field(default_factory=list)

    def add_discount(self, discount_details):
        self.discounts.append(discount_details)


@dataclass
class User:
    name: str
    products: list[Product] = field(default_factory=list)

    def has_previously_bought(self, product):
        return product in self.products
