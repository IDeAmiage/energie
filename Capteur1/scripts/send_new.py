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

# LOGGER ------
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=handlers,
)
# * Instantiate logger ---
logger = logging.getLogger("ENEDIS_LOGGER")

# RUN MAIN  ------

# LOOP
today = datetime.datetime.today()
day_init = today - datetime.timedelta(days=80)  # old 140  old 200
days = 20
for i in range(days):
    from_ = day_init.strftime("%Y-%m-%d")
    to_ = day_init + datetime.timedelta(days=1)
    to_ = to_.strftime("%Y-%m-%d")
    print(f"Doing {from_} to : {to_}")
    try:
        enedis_instance = ENEDIS(
            start_date=from_,
            end_date=to_,
            config_file="new_compteur/config.json",
        )
        data = enedis_instance.give_data()
        inject = Injection(
            dbname="enedis_camilo", meta=("1", "enedis"), df=data, ip="localhost"
        )
        inject.injection()
        logger.info("Injected")
    except Exception as e:
        logger.error("Exception catched")
        print(e)

    day_init = day_init + datetime.timedelta(days=1)
    time.sleep(30)


# inject = Injection(dbname="enedis_final", meta=("1", "enedis"), df=data, ip="localhost")
# inject.injection()


# enedis_data.to_csv("data.csv")
