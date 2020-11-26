from flask import Flask, request

app = Flask(__name__)
debug = True  # Enable debug printing
from render import render

hardcode_responses = True  # Enable hardcoded responses


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


if debug:
    print("[WARN] Code output may be very messy!")
if hardcode_responses:
    print("[WARN] Hardcoded responses are enabled, do not use in production!")


@app.route("/wii_svr/WPOperationServlet", methods=["GET", "POST"])
def op_servlet():
    if debug:
        print("Arguments:", request.args)
        try:
            print("JSON:", request.json())
        except:
            print("No JSON")
        print("Headers:", request.headers)

    if hardcode_responses:
        return """
statusCode=1000
latestClientVersion=0x02
errorItems_1=0
errorItems_2=0
errorItems_3=0
errorItems_4=0
errorItems_5=0
errorItems_6=0
errorItems_7=0
message=aaaaa
itemCode_1=00001
itemCode_2=00002
itemCode_3=00003
itemCode_4=00004
itemCode_5=00005
itemCode_6=00006
itemCode_7=00010
itemPriceCode_1=00001
itemPriceCode_2=00002
itemPriceCode_3=00003
itemPriceCode_4=00004
itemPriceCode_5=00005
itemPriceCode_6=00006
itemPriceCode_7=00007
itemName_1=1
itemName_2=WiiLink24
itemName_3=1
itemName_4=1
itemName_5=1
itemName_6=1
itemName_7=1
itemComment1_1=WL24
itemComment1_2=1
itemComment1_3=1
itemComment1_4=1
itemComment1_5=1
itemComment1_6=1
itemComment1_7=1
itemComment2_1=1
itemComment2_2=1
itemComment2_3=1
itemComment2_4=1
itemComment2_5=1
itemComment2_6=1
itemComment2_7=1
size_1=1
size_2=1
size_3=1
size_4=1
size_5=1
size_6=1
size_7=1
imageCount_1=10
imageCount_2=1
imageCount_3=1
imageCount_4=1
imageCount_5=1
imageCount_6=1
imageCount_7=3
pageCount_1=10
pageCount_2=1
pageCount_3=1
pageCount_4=1
pageCount_5=1
pageCount_6=1
pageCount_7=1
price_1=99999999
price_2=1
price_3=1
price_4=1
price_5=1
price_6=1
price_7=1
imageCountDisp_1=10
imageCountDisp_2=1
imageCountDisp_3=1
imageCountDisp_4=1
imageCountDisp_5=1
imageCountDisp_6=1
imageCountDisp_7=1
pageCountDisp_1=1
pageCountDisp_2=1
pageCountDisp_3=1
pageCountDisp_4=1
pageCountDisp_5=1
pageCountDisp_6=1
pageCountDisp_7=1
priceUnit_1=2
priceUnit_2=1
priceUnit_3=1
priceUnit_4=1
priceUnit_5=1
priceUnit_6=1
priceUnit_7=1
delivery_1=1
delivery_2=1
delivery_3=1
delivery_4=1
delivery_5=1
delivery_6=1
delivery_7=0
            """
        return NotImplemented("Please enable hardcoded responses", status_code=501)


@app.route("/wii_svr/WPFileOperationServlet", methods=["GET", "POST"])
def fileopservlet():
    if debug:
        print("Arguments:", request.args)
        try:
            print("JSON:", request.json())
        except:
            print("No JSON")
        print("Headers:", request.headers)
    render("temp.png")
    if hardcode_responses:
        return """
statusCode=1000
latestClientVersion=0x02
errorItems_1=0
message=a
imageID=1
        """

    return NotImplemented("Please enable hardcoded responses", status_code=501)
