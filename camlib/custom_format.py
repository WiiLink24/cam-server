import functools
from .status_values import STATUS_OK


def response():
    def decorator(func):
        @functools.wraps(func)
        def serialization_wrapper(*args, **kwargs):
            print("hi")
            returned_value = func(*args, **kwargs)

            # Ensure we are truly dealing with a dictionary.
            if isinstance(returned_value, dict):
                # Insert common elements. These should be at the start.
                response_dict = {
                    "statusCode": STATUS_OK,
                    "latestClientVersion": "0x02",
                }

                response_dict.update(returned_value)

                return dict_to_custom_format(response_dict)
            else:
                return returned_value

        return serialization_wrapper

    return decorator


def dict_to_custom_format(passed_dict: dict) -> str:
    result = ""

    for key, value in passed_dict.items():
        if isinstance(value, list):
            # Given a name "foo" and value ["a", "b", "c"],
            # this is expected to produce
            # foo_1 = a
            # foo_2 = b
            # foo_3 = c
            #
            # We must index from one for insertion.
            for index, list_val in enumerate(value):
                current_index = index + 1
                current_value = value[index]

                result += f"{key}_{current_index}={current_value}\n"

        if isinstance(value, str) or isinstance(value, int):
            result += f"{key}={value}\n"

    return result
