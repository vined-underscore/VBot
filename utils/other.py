import os

def clear_console():
  os.system("clear" if os.name != "nt" else "cls")