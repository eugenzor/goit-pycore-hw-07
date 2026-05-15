from colorama import Fore, Style


def red(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def green(text: str) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
