import os

os.system("python -m pip uninstall discord")
os.system("python -m pip uninstall discord.py")
os.system("python -m pip uninstall discord.py-self")

os.system("python -m pip uninstall selfcord.py")
os.system("python -m pip install discord.py-self")
os.system("python -m pip install -r requirements.txt")
