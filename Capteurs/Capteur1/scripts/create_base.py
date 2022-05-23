# COMMON IMPORTS ------
import logging
import sys
from pathlib import Path

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.insert(4, to_add)  # TODO

from Lib.Senders.Injector import DataBase, Injection

# LOGGING SETUP ------
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

logging.info("Create based called")
logging.info(f"Path appended to sys.path {to_add}")

# CONFIGS ------
CONFIG_ = (
    "/home/camilodlt/Documents/energie/Project/Capteurs/Capteur1/config/config.json"
)
CON_ = "localhost"
TEMPLATE_NAME_ = "enedis_2"
DB_NAME_ = "enedis_camilo2"
# from enedis.get_enedis import ENEDIS, Injector
# from Sender.Injector import DataBase, Injection

# RUN CREATION ------
logging.info("Creating Databases ...")
db = DataBase(CON_)
db.create_template(TEMPLATE_NAME_)
db.create(DB_NAME_, tpname=TEMPLATE_NAME_)
logging.info("Create_base end")
