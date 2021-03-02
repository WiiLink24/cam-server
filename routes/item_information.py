from camlib import response


@response()
def get_item_information(_):
    return {
        "errorItems": [0, 0, 0, 0, 0, 0, 0],
        "message": "",
        "itemCode": ["00001", "00002", "00003", "00004", "00005", "00006", "00007"],
        "itemPriceCode": [
            "00001",
            "00002",
            "00003",
            "00004",
            "00005",
            "00006",
            "00007",
        ],
        "itemName": [
            "Photo Print",
            "Notebook",
            "Calendar",
            "Photo Album",
            "Business Card",
            "Mii Card",
            "Unknown",
        ],
        "itemComment1": [
            "This item is perfect for a simple print. Use it anywhere you'd like.",
            "Create a simple notebook that you can give to people and treasure!",
            "Create a calendar that anyone can love and enjoy.",
            "A fun album that everyone will love.",
            "The perfect business card!",
            "It's as if you were on a business card.",
            "Where does this message show up?",
        ],
        "itemComment2": [
            "Print responsibly.",
            "Print responsibly.",
            "Print responsibly.",
            "Print responsibly.",
            "Print responsibly.",
            "Print responsibly.",
            "Print responsibly.",
        ],
        "size": [1, 1, 1, 1, 1, 1],
        "imageCount": [10, 10, 10, 10, 10, 10],
        "pageCount": [10, 10, 10, 10, 10, 10],
        "price": ["250000000000", 1, 1, 1, 1, 1, 1],
        "imageCountDisp": [10, 10, 10, 10, 10, 10],
        "pageCountDisp": [10, 10, 10, 10, 10, 10],
        "priceUnit": ["Ryal Points", 1, 1, 1, 1, 1],
        "delivery": [
            "Teleports instantly.",
            "Teleports instantly.",
            "Teleports instantly.",
            "Teleports instantly.",
            "Teleports instantly.",
            "Teleports instantly.",
            "Teleports instantly.",
        ],
    }
