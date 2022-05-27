# DROP TABLES AND TEMPLATES


# COMMON IMPORTS ------
import logging
import sys
from pathlib import Path

# LOGGING SETUP ------
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent)
sys.path.insert(4, to_add)  # TODO
logger.info(f"Path appended to sys.path {to_add}")
from Lib.Getters.ENEDIS.get_enedis import ENEDIS
from Lib.Senders.Injector import DataBase

# CONFIGS ------
CON_ = "localhost"
DB_NAME_ = "rmm"

# Injection
db = DataBase(ip=CON_)

db.liste()

# to_drop
to_drop = ["rmm"]

for i in to_drop:
    db.query(f"UPDATE pg_database SET datistemplate='false' WHERE datname='{i}';")
    db.query(f"DROP DATABASE {i} WITH (FORCE);")
    db.query("commit;")
