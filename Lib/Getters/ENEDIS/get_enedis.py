# IMPORTS ------

import datetime
import http.client
import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional, Protocol

import pandas as pd

# LOGGING SETUP ------
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.insert(4, to_add)  # TODO
logging.info(f"Path appended to sys.path {to_add}")
from Lib.Get.SENSOR_PROTOCOL import sensor

############# DEFAULTS ####################
# DEFAULT DATE  ------
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
start_date_init = yesterday.strftime("%Y-%m-%d")
end_date_init = today.strftime("%Y-%m-%d")
##########################################

# EXCEPTION ------
class NoResponse(Exception):
    """
    Common exception
    """

    pass


# ENEDIS GETTER ------
"""
ENEDIS

should implement : 

give_measure_info()

give_place_info()

def give_sensor_info()

"""


class ENEDIS(sensor):
    """
    start_date : Start date for enedis query
    end_date : End date for enedis query
    config_file : which config file to use (i.e. the token etc)...
    """

    sensor_info = {}
    place_info = {}
    data_info = {}

    def __init__(
        self,
        start_date: Optional[str] = start_date_init,
        end_date: Optional[str] = end_date_init,
        config_file: str = "config/config.json",
    ):
        self.config_file = config_file

        # date related settings, might be passed or defaulted at today
        self.start = start_date
        self.end = end_date

        # read ---
        self.read_sensor()
        self.read_place()
        self.read_data()

    # INITIALIZE THE INSTANCE ------
    def read_json(self, key: str):
        """
        Read configuration from file.
        """
        f = open(self.config_file)
        config = json.load(f)
        specific_config = config.get(key)
        return specific_config

    def read_sensor(self) -> None:
        self.sensor_info = self.read_json("sensor")

    def read_place(self) -> None:
        self.place_info = self.read_json("place")

    def read_data(self) -> None:
        self.data_info = self.read_json("entry_point")

    # CONNECTION FUNCTIONS ------
    def create_con_reqs(self, query_type: str = "consumption_load_curve") -> tuple:
        """
        Create payloads
        """
        APARTMENT_ID: str = self.place_info.get("id")
        PAYLOAD: dict = {
            "type": query_type,
            "usage_point_id": self.data_info.get("usage_point_id"),
            "start": self.start,
            "end": self.end,
        }

        HEADERS: dict = {
            "Authorization": self.data_info.get("token"),
            "Content-Type": "application/json",
        }

        logging.info("Connection Payload: %s" % PAYLOAD)
        logging.info("Connection Headers: %s" % HEADERS)

        return (APARTMENT_ID, PAYLOAD, HEADERS)

    # CREATE CONNECTION TO SERVER ------
    def enedis_con(self, http_con: str = "enedisgateway.tech") -> None:
        """
        Create connection
        """
        conn = http.client.HTTPSConnection(http_con)
        self.conn = conn
        time.sleep(2)

    # DATA QUERIES ------
    def request_enedis_con(self, payload: dict, headers: dict):
        """
        Query the connection with the payload
        """
        logging.info("Querying Enedis")

        self.conn.request("POST", "/api", json.dumps(payload), headers)
        res = self.conn.getresponse()
        if not res:
            logging.error("NO RESPONSE FROM QUERY EXCEPTION")
            raise NoResponse

        logging.info("Data queried from Enedis")
        data = res.read()
        data = data.decode("utf-8")
        return data

    def read_json_data(self, data):
        """
        Read the Json response
        """
        json_data = json.loads(data)
        return json_data

    def iterate_over_enedis_data(self, json_data):
        """
        Build a Dataframe from the Json response
        """
        unit_read = json_data.get("meter_reading").get("reading_type").get("unit")

        if unit_read:
            unit = unit_read
        else:
            unit = pd.NA

        rows = []
        for sample in json_data["meter_reading"]["interval_reading"]:
            new_row = {"dates": sample["date"], "val": sample["value"], "unit": unit}
            rows.append(new_row)

        enedis_data = pd.DataFrame(rows)
        # Append other cols
        enedis_data["place_id"] = self.place_info.get("id")
        enedis_data["sensor_id"] = self.sensor_info.get("id")
        logging.info(
            "Retrieved data has the following shape : %s" % str(enedis_data.shape)
        )
        df_data_type = ["DATE", "NUMBER", "TEXT", "NUMBER"]
        return enedis_data, df_data_type

    def coerce_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data["dates"] = pd.to_datetime(data["dates"])
        return data

    # API QUERY -----
    def get_enedis_data_daily_consumption(self):
        """
        Get energy consomption
        """
        # Create request
        place_id, payload, headers = self.create_con_reqs()
        # Create connection
        self.enedis_con()

        try:
            data = self.request_enedis_con(payload, headers)
        except NoResponse as e:
            logging.error("NoResponse Exception %s" % e)
            return None, None
        json_data = self.read_json_data(data)
        enedis_data, df_data_type = self.iterate_over_enedis_data(json_data)
        return enedis_data, df_data_type

    # TODO
    def if_error(self, cond: bool = True):
        if cond:
            con_reqs = self.read_config()
            id = con_reqs.get("appt_id")
            msg = {"id": id, "params": con_reqs, "action": "rerun", "interval": "hour"}
            with open("last_action.txt", "w") as json_file:
                json.dump(msg, json_file)

    # PROTOCOL QUERIES ------
    def give_sensor_info(self) -> dict:
        return self.sensor_info

    def give_measure_info(self) -> pd.DataFrame:
        data, _ = self.get_enedis_data_daily_consumption()
        data = self.coerce_data(data)
        return data

    def give_place_info(self) -> dict:
        return self.place_info

    def give_meta_info(self) -> dict:
        return {"sensor": self.give_sensor_info(), "place": self.give_place_info()}
