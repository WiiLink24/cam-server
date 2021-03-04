from werkzeug import exceptions

from cam import db
from camlib import response, current_order, current_item, item_wrapper


@response()
@item_wrapper()
def get_service_information(request):
    service_data = request.form.get("serviceData_1")
    if not service_data:
        return exceptions.BadRequest()

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
