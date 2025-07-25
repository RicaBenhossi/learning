from src.module05.spy.discounts import DiscountManager
from src.module05.spy.model_objects import Product, DiscountData, User


# class StubNotifier:
#     def notify(self, user, message):
#         pass

class SpyNotifier:
    def __init__(self):
        self.notified_users = list()

    def notify(self, user, message) -> None:
        self.notified_users.append(user)

def test_discount_for_users():
    # notifier = StubNotifier()
    notifier = SpyNotifier()
    discount_manager = DiscountManager(notifier)
    product = Product("headphones")
    product.discounts = list()
    discount_details = DiscountData("10% off")
    users = [User("user1", [product]), User("user2", [product])]

    discount_manager.create_discount(product, discount_details, users)

    assert product.discounts == [discount_details]
    assert users[0] in notifier.notified_users
    assert users[1] in notifier.notified_users
