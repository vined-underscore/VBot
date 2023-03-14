import os

os.system("python -m pip uninstall discord")
os.system("python -m pip uninstall discord.py")
os.system("python -m pip uninstall discord.py-self")

os.system("python -m pip install git+https://github.com/dolfies/discord.py-self@renamed#egg=selfcord.py[voice]")