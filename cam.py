# Required to allow reading of jpegData. Flask must be imported after this code.
from werkzeug import formparser

from camlib import response
from formparser_override import parse_multipart_headers_fix

formparser.parse_multipart_headers = parse_multipart_headers_fix

# Now we can continue.
from werkzeug import exceptions
from flask import Flask, request

from routes import (
    get_item_information,
    get_exemption_information,
    get_order_id,
    notice_order_finish,
)
import render

app = Flask(__name__)

# Enable debug printing
debug = __name__ == "__main__"

action_list = {
    "getItemInformation": get_item_information,
    "getExemptionInformation": get_exemption_information,
    "getOrderID": get_order_id,
    "noticeOrderFinish": notice_order_finish,
}


@app.route("/wii_svr/WPOperationServlet", methods=["GET", "POST"])
def op_servlet():
    if debug:
        print("Arguments:", request.args)
        print("Headers:", request.headers)

    try:
        action = request.headers["Operation"]
        return action_list[action](request)
    except KeyError:
        # This is not an action or a format we know of.
        return exceptions.NotFound()


@app.route("/wii_svr/WPFileOperationServlet", methods=["GET", "POST"])
@response()
def file_op_servlet():
    if debug:
        print("Arguments:", request.args)
        print("Headers:", request.headers)

    # TODO: validate
    open('temp.jpg', mode='wb').write(request.files["jpegData"].read())
    render.render('temp.jpg', 'Page{}.jpg')
    return {
        "errorItems_1": 0,
        "message": "a",
        "imageID": 1,
    }
