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
