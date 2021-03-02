from camlib import response


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
