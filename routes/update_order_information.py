from werkzeug import exceptions

from cam import db
from camlib import response, item_data
from models import Orders


@response()
def update_order_information(request):
    order_id = request.form.get("orderID")
    item_code = request.form.get("itemCode_1")
    email = request.form.get("email")
    if not order_id or not item_code or not email:
        return exceptions.BadRequest()

    current_order = Orders.query.filter_by(order_id=order_id).first()
    if not current_order:
        return exceptions.Forbidden()

    current_order.email = email
    db.session.commit()

    # We only need a subset of the full item data.
    current_item = item_data.get_item(item_code)
    if not current_item:
        return exceptions.BadRequest()

    eventual_response = {
        "available": 1,
        "itemCode": item_code,
        "itemPriceCode": item_code,
        "orderID": order_id,
        "orderDate": "today",
        "commodityCount": [1],
        "commodityPrice": [100000000],
        "taxOffAmt": [210000],
        "tax": [210000],
        "taxInAmt": [210000],
        "totalAmt": 0,
        "deliveryFee": 0,
        "daibikiFee": 0,
        "totalTax": 0,
        "otherFee": 0,
        "amountTotal": 0,
        "totalItemPrice": 0,
        "totalShipping": 0,
        "totalHandling": 0,
    }

    # Add our item data.
    eventual_response |= current_item.map_list()

    return eventual_response
