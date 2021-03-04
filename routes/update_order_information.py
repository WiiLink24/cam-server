from werkzeug import exceptions

from cam import db
from camlib import response, item_wrapper, current_item, current_order


@response()
@item_wrapper()
def update_order_information(request):
    # Ensure we have an email to work with.
    email = request.form.get("email")
    if not email:
        return exceptions.BadRequest()

    # Update our current order to include an email.
    current_order.email = email
    db.session.commit()

    eventual_response = {
        "available": 1,
        "itemCode": current_item.itemCode,
        "itemPriceCode": current_item.itemCode,
        "orderID": current_order.order_id,
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
