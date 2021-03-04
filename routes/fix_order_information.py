from cam import db
from camlib import response, item_wrapper, current_order, current_item


@response()
@item_wrapper()
def fix_order_information(request, item_code=None):
    # TODO: Start rendering of order
    current_order.complete = True
    db.session.commit()

    eventual_response = {
        "available": 1,
        "itemCode": item_code,
        "itemPriceCode": item_code,
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
