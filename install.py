import os

os.system("python -m pip uninstall discord")
os.system("python -m pip uninstall discord.py")
os.system("python -m pip uninstall discord.py-self")

os.system("python -m pip uninstall selfcord.py")
os.system("python -m pip install git+https://github.com/dolfies/discord.py-self@085884923bf16fafe268ceb5bdf35e7aa0fe60e4#egg=selfcord.py[voice]")
os.system("python -m pip install -r requirements.txt")
