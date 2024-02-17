#!/bin/python3
from pathlib import Path
import os
import customtkinter

if os.path.exists("boundaries.py"):
    os.remove("boundaries.py")

Path('boundaries.py').symlink_to('../../bin/main.py')

os.system("chmod +x main.py")
