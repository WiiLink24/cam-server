import os

from werkzeug import exceptions
from werkzeug.utils import secure_filename

from cam import db
from camlib import response
from models import Images, Orders
from routes.utils import generate_unique_id


@response()
def get_image_id(request):
    # Get common parameters
    uploading_filename = request.form.get("imageFileName")
    order_id = request.form.get("orderID")
    if not uploading_filename or not order_id:
        return exceptions.BadRequest()

    # Ensure we have an image.
    if "jpegData" not in request.files:
        return exceptions.BadRequest()

    # Ensure the order ID is valid before further processing.
    if not Orders.query.filter_by(order_id=order_id).first():
        return exceptions.Forbidden()

    # Sanitize for when we write to disk.
    filename = secure_filename(uploading_filename)
    # Necessary as render templates require the original filename with ".jpg" appended.
    # Nobody here is fond of this.
    filename += ".jpg"

    # An image ID has a maximum size of 7.
    unique_id = generate_unique_id(Images, Images.image_id, 7)
    if unique_id == "":
        return exceptions.InternalServerError()

    jpeg_image = request.files["jpegData"]
    jpeg_image.save(determine_path(order_id, filename))

    # Finally, save state to the database.
    current_order = Images(image_id=unique_id, order_id=order_id, filename=filename)
    db.session.add(current_order)
    db.session.commit()

    return {
        "orderID": unique_id,
    }


def determine_path(order_id: str, filename: str) -> str:
    path = f"./orders/{order_id}/"
    if not os.path.isdir(path):
        os.makedirs(path)

    path += filename

    return path
