from dataclasses import dataclass, asdict, field

DEFAULT_COMMENT_TWO = "Print responsibly."
DEFAULT_PRICE_UNIT = "Ryal Points"
DEFAULT_DELIVERY_TEXT = "Emails within 1 to 10 minutes."


# The following class's variable names are horribly non-Pythonic.
# For any further questions or comments, please blame Digicam for using these names.
@dataclass
class ItemInfo:
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
    return dict((k, [v]) for k, v in data)
