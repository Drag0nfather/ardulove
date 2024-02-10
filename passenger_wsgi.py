import sys

import os

INTERP = os.path.expanduser("/var/www/u1991005/data/www/ardulove.ru/venv/bin/python")
if sys.executable != INTERP:
   os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from app.app import application
