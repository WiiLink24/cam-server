from camlib import response


@response()
def get_item_information(_):
    return {
        "errorItems": [0, 0, 0, 0, 0, 0, 0],
        "message": "aaaaa",
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
        "itemName": ["As", "I", "sit", "I", "watch", "the", "sky"],
        "itemComment1": ["The", "fire", "burns", "I", "shut", "my", "eyes"],
        "itemComment2": [
            "but this",
            "broken",
            "city",
            "and the",
            "millions",
            "of",
            "wings",
        ],
        "size": [1, 1, 1, 1, 1, 1],
        "imageCount": [10, 10, 10, 10, 10, 10],
        "pageCount": [10, 10, 10, 10, 10, 10],
        "price": [99999999, 99999999, 99999999, 99999999, 99999999, 99999999, 99999999],
        "imageCountDisp": [10, 10, 10, 10, 10, 10],
        "pageCountDisp": [10, 10, 10, 10, 10, 10],
        "priceUnit": [1, 1, 1, 1, 1, 1],
        "delivery": [1, 1, 1, 1, 1, 1],
    }
