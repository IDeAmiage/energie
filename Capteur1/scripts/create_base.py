# COMMON IMPORTS ------
import datetime
import logging
import sys
import time
from pathlib import Path

# APPEND PARENT ------
sys.path.insert(4, str(Path(__file__).resolve().parent.parent))  # TODO

from enedis.get_enedis import ENEDIS, Injector
from Sender.Injector import DataBase, Injection

db = DataBase("localhost")
# db.create_template("enedis_2")
db.create("enedis_camilo", tpname="enedis_2")
