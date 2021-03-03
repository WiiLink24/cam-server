from werkzeug import exceptions

from cam import db
from camlib import response, item_data
from models import Orders


@response()
def get_service_information(request):
    order_id = request.form.get("orderID")
    item_code = request.form.get("itemCode_1")
    service_data = request.form.get("serviceData_1")
    if not service_data or not order_id or not item_code:
        return exceptions.BadRequest()

    # Obtain the item we are working with.
    current_item = item_data.get_item(item_code)
    if not current_item:
        return exceptions.BadRequest()

    # Ensure we have a valid order ID.
    current_order = Orders.query.filter_by(order_id=order_id).first()
    if not current_order:
        return exceptions.Forbidden()

    # Update our current order.
    current_order.order_schema = service_data
    db.session.commit()

    # Formulate a response.
    # First, we need to set that it was available.
    item_response = {"available": 1}
    # Next, merge our item's data to our response.
    item_response |= current_item.map_list()
    # Lastly, add a tax amount.
    item_response["taxInAmt_1"] = "1000000"

    return item_response
