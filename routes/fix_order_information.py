import os

from cam import db, app
from camlib import response, item_wrapper, current_order, current_item
from routes.utils import generate_zip_password
from render import render
from sender import digicam_sender


@response()
@item_wrapper()
def fix_order_information(_):
    current_order.complete = True
    db.session.commit()

    try:
        render(current_order.order_schema, current_order.order_id)
    except Exception as e:
        app.logger.exception(e)
        return ""

    password = generate_zip_password(10)

    os.system(
        f"cd orders/{current_order.order_id}; zip --password {password} {current_order.order_id}.zip -r *.png"
    )

    digicam_sender(
        f"orders/{current_order.order_id}/{current_order.order_id}.zip",
        current_order.email,
        password,
    )

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
