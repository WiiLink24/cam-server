import glob
import os
import shutil
import zipfile
from os.path import basename

from cam import db, app
from camlib import response, item_wrapper, current_order, current_item
from models import Images
from render import render
from sender import digicam_sender


@response()
@item_wrapper()
def fix_order_information(_):
    # Render our user's order to "Page XX.jpg" files.
    try:
        service_type = render(current_order.order_schema, current_order.order_id)
    except Exception as e:
        app.logger.exception(e)
        return ""

    order_location = os.path.join("orders", current_order.order_id)

    # Create a zip file of our order's images.
    zip_location = os.path.join(order_location, f"{current_order.order_id}.zip")
    order_zip = zipfile.ZipFile(zip_location, "w", zipfile.ZIP_DEFLATED)

    for page_file in glob.glob(f"{order_location}/Page *.jpg"):
        order_zip.write(page_file, basename(page_file))

    order_zip.close()

    # Send the user's order.
    digicam_sender(zip_location, current_order.email)

    if service_type == 3:
        # We will preserve rendered business cards for Digicard.
        current_order.is_business_card = True
    else:
        # Finally, delete the order once fully complete.
        shutil.rmtree(order_location)

        db.session.query(Images).filter(
            Images.order_id == current_order.order_id
        ).delete()
        db.session.delete(current_order)

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
