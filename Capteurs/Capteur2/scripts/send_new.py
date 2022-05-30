# COMMON IMPORTS ------
import logging
import sys
from pathlib import Path

# LOGGING SETUP ------
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.insert(4, to_add)  # TODO
logger.info(f"Path appended to sys.path {to_add}")
from Lib.Getters.ENEDIS.get_enedis import ENEDIS
from Lib.Senders.Injector import Injection

# CONFIGS ------
CON_ = "localhost"
DB_NAME_ = "enedis_cristiona_v2"
CONFIG_ = (
    "/home/camilodlt/Documents/energie/Project/Capteurs/Capteur2/config/config.json"
)
# APPEND PARENT ------
# e = ENEDIS(config_file=CONFIG_)
# * Get data ---
# data = e.give_measure_info()
# meta = e.give_meta_info()
# assert data is not None

# # INJECTION ------
# logger.info("Creating Injection instance")
# inject = Injection(dbname=DB_NAME_, meta=meta, df=data, ip=CON_)

# logger.info("Injecting data")
# inject.injection()
# logger.info("Injected")

# RUN MAIN  ------
# LOOP
import datetime
import time

today = datetime.datetime.today()
day_init = today - datetime.timedelta(days=10)  # old 140  old 200
days = 10
for i in range(days):
    from_ = day_init.strftime("%Y-%m-%d")
    to_ = day_init + datetime.timedelta(days=1)
    to_ = to_.strftime("%Y-%m-%d")
    print(f"Doing {from_} to : {to_}")
    try:
        e = ENEDIS(
            start_date=from_,
            end_date=to_,
            config_file=CONFIG_,
        )
        # * Get data ---
        data = e.give_measure_info()
        meta = e.give_meta_info()
        inject = Injection(dbname=DB_NAME_, meta=meta, df=data, ip=CON_)
        inject.injection()
        logger.info("Injected")
    except Exception as e:
        logger.error("Exception catched")
        print(e)

    day_init = day_init + datetime.timedelta(days=1)
    time.sleep(30)
