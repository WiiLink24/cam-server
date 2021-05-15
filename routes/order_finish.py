from camlib import response


@response()
def notice_order_finish(_):
    return {
        "errorItems": [0],
        "available": 0,
        "fixOrderText": "Your order has been finalized!",
        "messageBoardText": "Congratulations! Your order has been dispatched via email. "
        "Please allow up to 10 minutes for delivery.",
    }
