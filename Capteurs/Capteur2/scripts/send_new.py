# COMMON IMPORTS ------
import logging
import sys
from pathlib import Path

# LOGGING SETUP ------
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.insert(4, to_add)  # TODO
logging.info(f"Path appended to sys.path {to_add}")
from Lib.Getters.ENEDIS.get_enedis import ENEDIS

CONFIG_ = (
    "/home/camilodlt/Documents/energie/Project/Capteurs/Capteur1/config/config.json"
)
# APPEND PARENT ------
e = ENEDIS(config_file=CONFIG_)
# * Get data ---
data = e.give_measure_info()
sensor = e.give_sensor_info()
assert data is not None
# place = e.give_place_info()

# INJECTION ------
logging.info("Creating Injection instance")
inject = Injection(dbname="enedis_camilo2", meta=sensor, df=data, ip="localhost")

logging.info("Injecting data")
inject.injection()

logger.info("Injected")

# RUN MAIN  ------
# # LOOP
# today = datetime.datetime.today()
# day_init = today - datetime.timedelta(days=80)  # old 140  old 200
# days = 20
# for i in range(days):
#     from_ = day_init.strftime("%Y-%m-%d")
#     to_ = day_init + datetime.timedelta(days=1)
#     to_ = to_.strftime("%Y-%m-%d")
#     print(f"Doing {from_} to : {to_}")
#     try:
#         enedis_instance = ENEDIS(
#             start_date=from_,
#             end_date=to_,
#             config_file="new_compteur/config.json",
#         )
#         data = enedis_instance.give_data()
#         inject = Injection(
#             dbname="enedis_camilo", meta=("1", "enedis"), df=data, ip="localhost"
#         )
#         inject.injection()
#         logger.info("Injected")
#     except Exception as e:
#         logger.error("Exception catched")
#         print(e)

#     day_init = day_init + datetime.timedelta(days=1)
#     time.sleep(30)


# inject = Injection(dbname="enedis_final", meta=("1", "enedis"), df=data, ip="localhost")
# inject.injection()


# enedis_data.to_csv("data.csv")
