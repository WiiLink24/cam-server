import flask
from flask import Flask, request
from werkzeug import exceptions

from camlib import response
from routes import get_item_information

app = Flask(__name__)
debug = True  # Enable debug printing
import render


class NotImplemented(Exception):
    status_code = 501

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


action_list = {"getItemInformation": get_item_information}


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
def fileopservlet():
    if debug:
        print("Arguments:", request.args)
        try:
            print("JSON:", request.json())
        except:
            print("No JSON")
        print("Headers:", request.headers)
    jpeg = bytes(request.form["jpegData"])
    f = open("temp.jpg", "wb")
    f.write(jpeg)
    f.close()
    render("temp.jpg", "temp.png")
    if hardcode_responses:
        return """
statusCode=1000
latestClientVersion=0x02
errorItems_1=0
message=a
imageID=1
        """

    return NotImplemented("Please enable hardcoded responses", status_code=501)
