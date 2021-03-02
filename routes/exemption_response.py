from camlib import response


@response()
def get_exemption_information(_):
    return {
        "errorItems": [0, 0, 0, 0],
        "message": "Everything is free! Congratulations!",
        "exemptionID": "YOO",
        "exemptionTEXT": "Congratulations on the free everything! Valid from now until the server crashes.",
    }
