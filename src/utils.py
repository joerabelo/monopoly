from typing import Any


class Colors:
    endc = "\033[0m"
    blue = "\033[94m"
    green = "\033[92m"
    red = "\033[91m"
    bold = "\033[1m"
    clear = "\x1b[2J\x1b[H"


# def print_header(text):
#     print(f'{Colors.green}+{"-" * 67}+{Colors.endc}')
#     print(f'{Colors.green}| {text:<64} |{Colors.endc}')
#     print(f'{Colors.green}+{"-" * 67}+{Colors.endc}')


def print_head(text: str) -> None:
    print(f"{Colors.green}# {text:<64} {Colors.endc}")


def print_line(text: str, value: Any, ln_break: bool = False, sep: str = ":") -> None:
    text += sep
    line_break = ln_break and "\n" or ""
    print(
        f"{Colors.blue}{text:<14}{Colors.endc}  {Colors.bold}{Colors.red}{value:>10}{Colors.endc}{line_break}"
    )
