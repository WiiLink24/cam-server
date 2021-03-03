from camlib import Items, ItemInfo

item_data = Items()

# We need 7 items of data.
# Any more, any less, and getItemInformation fails.
item_data.add(
    ItemInfo(
        itemName="Photo Print",
        itemComment1="This item is perfect for a simple print. Use it anywhere you'd like.",
    )
)
item_data.add(
    ItemInfo(
        itemName="Notebook",
        itemComment1="Create a simple notebook that you can give to people and treasure!",
    )
)
item_data.add(
    ItemInfo(
        itemName="Calendar",
        itemComment1="Create a calendar that anyone can love and enjoy.",
    )
)
item_data.add(
    ItemInfo(
        itemName="Photo Album",
        itemComment1="A fun album that everyone will love.",
    )
)
item_data.add(
    ItemInfo(
        itemName="Business Card",
        itemComment1="The perfect business card!",
    )
)
item_data.add(
    ItemInfo(
        itemName="Mii Card",
        itemComment1="It's as if you were on a business card.",
    )
)
item_data.add(
    ItemInfo(
        itemName="Unknown",
        itemComment1="Where does this message show up?",
    )
)
