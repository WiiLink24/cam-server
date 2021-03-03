from werkzeug import exceptions

from cam import db
from camlib import response
from models import Orders
from routes.utils import generate_unique_id


@response()
def get_order_id(_):
    # An order ID has a maximum size of 14.
    unique_id = generate_unique_id(Orders, Orders.order_id, 14)
    if unique_id == "":
        return exceptions.InternalServerError()

    current_order = Orders(order_id=unique_id)
    db.session.add(current_order)
    db.session.commit()

    return {
        "exemptionID": "YOO",
        "exemptionTEXT": "Everything is free! You get a photo, you get a photo, and you get a photo.",
        "available": 1,
        "orderID": unique_id,
    }
