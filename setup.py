# coding: cp1252
import os
import sys
from datetime import datetime
from cx_Freeze import setup, Executable
base = None
dt = datetime.now()

# os.environ['TCL_LIBRARY'] = r'C:/Users/Admin/AppData/Local/Programs/Python/Python310/tcl/tcl8.6'
#
# os.environ['TK_LIBRARY'] = r'C:/Users/Admin/AppData/Local/Programs/Python/Python310/tcl/tk8.6'

if sys.platform == 'win32':
    base = 'Win32GUI'


build_exe_options = {
    "packages": ["threading", "time", "datetime", "struct", "os", "logging", "dotenv", "codecs", "pyodbc",
                 "pyModbusTCP", "signalrcore", "multiprocessing", "portalocker"],
    "include_files": [
        "logs/",
        ".env"
        ]
    }




setup(
    name="DCM ShriRam",
    version="0.1",
    description="DCM ShriRam Synfo Driver",
    options={"build_exe":build_exe_options},
    executables=[Executable("main.py")]
    )