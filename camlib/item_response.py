import functools

from flask import request, g
from werkzeug import exceptions
from werkzeug.local import LocalProxy

from camlib import item_data
from models import Orders


def get_current_order():
    if "current_order" not in g:
        return None
    else:
        return g.current_order


def get_current_item():
    if "current_item" not in g:
        return None
    else:
        return g.current_item


# For easy access
current_order = LocalProxy(get_current_order)
current_item = LocalProxy(get_current_item)


# Almost all item codes are passed with the form field "itemCode_1".
# However, some vary.
def item_wrapper(item_code_name="itemCode_1"):
    def decorator(func):
        @functools.wraps(func)
        def validity_wrapper(*args, **kwargs):
            order_id = request.form.get("orderID")
            item_code = request.form.get(item_code_name)
            if not order_id or not item_code:
                return exceptions.BadRequest()

            # Ensure the order exists.
            retrieved_order = Orders.query.filter_by(order_id=order_id).first()
            if not retrieved_order:
                return exceptions.Forbidden()

            # Ensure the item exists as well, if needed.
            retrieved_item = item_data.get_item(item_code)
            if not retrieved_item:
                return exceptions.BadRequest()

            # As it does, set to our global context.
            g.current_order = retrieved_order
            g.current_item = retrieved_item

            return func(*args, **kwargs)

        return validity_wrapper

    return decorator
