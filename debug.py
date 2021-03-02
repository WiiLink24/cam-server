from colorama import Fore, Style


def dict_dump(passed_dict):
    for key, value in passed_dict:
        print(f"{Fore.CYAN}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")


def request_dump(request):
    # Arguments may not be present.
    if request.args:
        print(f"{Fore.MAGENTA}Arguments:{Style.RESET_ALL}")
        dict_dump(request.args)

    print(f"{Fore.MAGENTA}Headers:{Style.RESET_ALL}")
    dict_dump(request.headers)
