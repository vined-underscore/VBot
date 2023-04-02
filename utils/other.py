import os
from datetime import datetime
from colorama import Fore as F
from typing import Any


def clear_console() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def log(text: Any) -> None:
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f"{F.LIGHTBLACK_EX}[{time}] {text}")
