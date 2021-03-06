from camlib import response, item_wrapper


@response()
@item_wrapper()
def fix_item_information(_):
    return {}
