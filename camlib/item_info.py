from dataclasses import dataclass, asdict, field
from typing import Optional

DEFAULT_COMMENT_TWO = "Print responsibly."
DEFAULT_PRICE_UNIT = "$"
DEFAULT_DELIVERY_TEXT = "Emails within 1 to 10 minutes."


# The following class's variable names are horribly non-Pythonic.
# For any further questions or comments, please blame Digicam for using these names.
@dataclass
class ItemInfo:
    itemCode: str = field(default="00000")
    itemPriceCode: str = field(default="00000")
    itemName: str = field(default="Zane")
    itemComment1: str = field(default="A witty comment.")
    itemComment2: str = field(default=DEFAULT_COMMENT_TWO)
    size: int = field(default=1)
    imageCount: int = field(default=10)
    pageCount: int = field(default=10)
    price: int = field(default=100)
    imageCountDisp: int = field(default=10)
    pageCountDisp: int = field(default=10)
    priceUnit: str = field(default=DEFAULT_PRICE_UNIT)
    delivery: str = field(default=DEFAULT_DELIVERY_TEXT)

    def map(self) -> dict:
        return asdict(self)

    def map_list(self) -> dict:
        return asdict(self, dict_factory=item_map)


def item_map(data) -> dict:
    """
    Returns a dictionary where every key's value is in a list.

    In a perfect world, we might be able to have data looking similar to
    ```
    name=Testing
    comment=Hello!
    price=1
    ```
    but Digicam, alas, is not a perfect world.
    With a tuple and our custom response format, we can achieve
    ```
    name_1=Testing
    comment_1=Hello!
    price_1=1
    ```
    repeatedly.
    """
    return {k: [v] for k, v in data}


class Items:
    items: list[ItemInfo] = []
    count: int = 1

    def add(self, item: ItemInfo):
        """Used to add an item. Updates item code and item price code accordingly."""
        proper_code = f"{self.count:05}"
        item.itemCode = proper_code
        item.itemPriceCode = proper_code

        self.items.append(item)

        self.count += 1

    def get_item(self, code) -> Optional[ItemInfo]:
        return next((item for item in self.items if item.itemCode == code), None)
