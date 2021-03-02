from colorama import Fore, Style
from werkzeug.datastructures import MultiDict


def dict_dump(passed_dict):
    if isinstance(passed_dict, MultiDict):
        passed_dict = passed_dict.items(multi=True)

    for key, value in passed_dict:
        print(f"{Fore.CYAN}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")


def request_dump(request):
    # Arguments may not be present.
    if request.args:
        print(f"{Fore.MAGENTA}Arguments:{Style.RESET_ALL}")
        dict_dump(request.args)

    if request.form:
        print(f"{Fore.MAGENTA}Form items:{Style.RESET_ALL}")
        dict_dump(request.form)

    print(f"{Fore.MAGENTA}Headers:{Style.RESET_ALL}")
    dict_dump(request.headers)
