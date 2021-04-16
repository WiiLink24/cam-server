from camlib import response


@response()
def notice_order_finish(_):
    return {
        "errorItems": [0],
        "available": 0,
        "fixOrderText": "Your order has been finalized!",
        "messageBoardText": "Congratulations!\nYour order has been dispatched via email.\n"
        "Please wait up to 5 minutes for delivery.",
    }
