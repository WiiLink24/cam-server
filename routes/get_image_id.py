import os

from werkzeug import exceptions
from werkzeug.utils import secure_filename

from cam import db
from camlib import response, item_wrapper, current_order
from models import Images
from routes.utils import generate_unique_id


@response()
# For unknown reasons, this is the only request with such a name.
@item_wrapper(item_code_name="itemCode")
def get_image_id(request):
    # Get our desired filename.
    uploading_filename = request.form.get("imageFileName")
    if not uploading_filename:
        return exceptions.BadRequest()

    # Ensure we have an image.
    if "jpegData" not in request.files:
        return exceptions.BadRequest()

    # An image ID has a maximum size of 7.
    unique_id = generate_unique_id(Images, Images.image_id, 7)
    if unique_id == "":
        return exceptions.InternalServerError()

    filename = f"{unique_id}.jpg"

    # Next, save our file to disk.
    jpeg_image = request.files["jpegData"]
    jpeg_image.save(determine_path(current_order.order_id, filename))

    # Finally, save state to the database.
    added_image = Images(
        image_id=unique_id, order_id=current_order.order_id, filename=filename
    )
    db.session.add(added_image)
    db.session.commit()

    return {
        "imageID": unique_id,
    }


def determine_path(order_id: str, filename: str) -> str:
    path = f"./orders/{order_id}/"
    if not os.path.isdir(path):
        os.makedirs(path)

    path += filename

    return path
