from src.module05.spy.model_objects import Product, DiscountData, User


class DiscountManager:
    def __init__(self, notifier):
        self.notifier = notifier

    def create_discount(self,
                        product: Product,
                        discount_details: DiscountData,
                        users: list[User]
                        ) -> None:
        if users:
            key_user = users[0]
        else:
            raise RuntimeError("Can't create a discount for a product with no key user")

        product.add_discount(discount_details)
        for user in users:
            if user.has_previously_bought(product):
                # Bug! This should not be key_user, it should be 'user'
                self.notifier.notify(user,
                                     f"You may be interested in a discount on this product! {product.name}")
