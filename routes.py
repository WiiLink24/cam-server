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
        "itemName": [
            "Item one",
            "Item two",
            "Item three",
            "Item four",
            "Item five",
            "Item six",
            "Item seven",
        ],
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


@response()
def get_exemption_information(_):
    return {
        "errorItems": [0, 0, 0, 0],
        "message": "Everything is free! Congratulations!",
        "exemptionID": "YOO",
        "exemptionTEXT": "Congratulations on the free everything! Valid from now until the server crashes.",
    }


@response()
def get_order_id(_):
    return {
        "errorItems": [0, 0, 0, 0],
        "message": "Everything is free! Congratulations!",
        "exemptionID": "YOO",
        "exemptionTEXT": "Congratulations on the free everything! Valid from now until the server crashes.",
        "available": "a",
        "orderID": "1000",
    }


@response()
def notice_order_finish(_):
    return {
        "errorItems": [0],
        "message": "woohoo",
        "available": 0,
        "fixOrderText": "Your order is finished congratulations omg",
        "messageBoardText": "YEAHHH",
    }
