from camlib import response, item_data


@response()
def get_item_information(_):
    # For unknown reasons, we require errorItems for each 7 items.
    item_information = {"errorItems": [0, 0, 0, 0, 0, 0, 0]}

    # Merge the dictionaries of all registered items.
    for individual_info in item_data.items:
        for key, value in individual_info.map().items():
            if key not in item_information:
                item_information[key] = []

            item_information[key].append(value)

    return item_information
