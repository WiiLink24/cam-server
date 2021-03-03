from camlib import response


@response()
def get_exemption_information(_):
    return {
        "exemptionID": "YOO",
        "exemptionTEXT": "Congratulations on the free everything! Valid from now until the server crashes.",
    }
