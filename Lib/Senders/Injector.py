# IMPORTS ------
import json
import logging
import sys
from pathlib import Path
from typing import Union

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, exc

# LOGGING SETUP ------
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# ADD ADDITIONAL LIB -----
to_add = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(4, to_add)  # TODO
logging.info(f"Path appended to sys.path {to_add}")

from Lib.Sender.SENDER_PROTOCOL import Injector

##############################
###########CLASSES############
##############################
"""
DOC TODO 
"""


class DataBase:
    eng: str = "postgresql+psycopg2"
    user: str = "postgres:adminida"
    port: str = "5432"

    def __init__(self, ip: str):
        """
        Creates a connection and commits
        """
        self.conn_string = f"{self.eng}://{self.user}@{ip}:{self.port}"
        self.engine = create_engine(self.conn_string)
        con = self.engine.connect()
        con.execute("commit;")

    def liste(self) -> None:
        """
        Show all databases
        """
        with self.engine.connect() as self.db:

            result = self.db.execute(
                """
                SELECT datname FROM pg_database;
            """
            )

            for r in result:
                print(r[0])

    def exist(self, dbname: str) -> bool:
        """
        Checks that a database passed exists in the server
        """
        with self.engine.connect() as self.db:

            result = self.db.execute(
                """
                SELECT datname FROM pg_database;
            """
            )

            for r in result:
                if r[0].lower() == dbname.lower():
                    return True
        return False

    def create_template(self, tpname: str) -> None:
        """
        Creates a Template
        """
        tpname = tpname.lower()
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            self.db.execute(
                f"""
                CREATE database {tpname} WITH IS_TEMPLATE = true;"""
            )

        conn_tp = f"{self.conn_string}/{tpname}"
        engine = create_engine(conn_tp)
        with engine.connect() as tp:
            tp.execute("commit;")

            # id int | name text | data json
            tp.execute(
                """
                CREATE TABLE sensor (id integer PRIMARY KEY, name text, data json);
            """
            )

            # id int | name text | data json
            tp.execute(
                """
                CREATE TABLE place (id integer PRIMARY KEY, name text, data json);
            """
            )

            tp.execute(
                """
                CREATE TABLE measures ("dates" timestamp, "val" real,
                "unit" text, "place_id" bigint REFERENCES place (id),
                "sensor_id" integer REFERENCES sensor (id), PRIMARY KEY("dates","val" ,"unit" ));
                """
            )

            tp.execute("commit;")
            tp.close()
        engine.dispose()

    def create(self, dbname: str, tpname: str):
        """
        Creates a database with a template that is already created.
        Do nothing if that database already exists.
        """
        dbname = dbname.lower()
        if self.exist(dbname) is True:
            print("Cette base existe d??j??")
        else:
            with self.engine.connect() as self.db:
                self.db.execute("commit;")

                self.db.execute(
                    f"""
                    CREATE database {dbname} WITH TEMPLATE {tpname.lower()};
                """
                )

                print("Database cr??e")

    def query(self, q: str) -> sqlalchemy.engine.CursorResult:
        """
        Executes an SQL query
        """
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            return self.db.execute(q)


"""
Must implement it's protocol : 
def give_sensor():

def give_data():

def give_place():

Implemented at the end
"""


class Injection(Injector):
    eng: str = "postgresql+psycopg2"
    user: str = "postgres:adminida"
    port: str = "5432"

    def __init__(self, dbname: str, meta: dict, df: pd.DataFrame, ip: str) -> None:
        """
        Meta is an str with JSON format.
        Meta must have the following keys
            - sensor
                - id
                - name
                - data
            - place
                - id
                - name
                - data

        """
        self.dbname = dbname.lower()
        conn_string = f"{self.eng}://{self.user}@{ip}:{self.port}/{self.dbname}"
        self.engine = create_engine(conn_string)
        self.meta: dict = meta
        self.df = df
        self.exist_place_or_sensor()

    def exist_sensor(self) -> bool:
        """
        Verifies that a sensor already exists in the table.
        """
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                """
                SELECT * FROM sensor
            """
            ):

                if str(r[0]) == str(self.meta["sensor"]["id"]):
                    logging.info("Sensor already exists")
                    return True
            return False

    def exist_place(self) -> bool:
        """
        Verifies that a place exists iexist_placen the table
        """
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                """
                SELECT * FROM place
            """
            ):

                if str(r[0]) == str(self.meta["place"]["id"]):
                    logging.info("Place already exists")
                    return True

            return False

    def exist_place_or_sensor(self) -> None:
        """
        Runs all verifications
        """
        logging.info("Verifying Place and Sensor existance")
        self.sensor_bool = self.exist_sensor()
        self.place_bool = self.exist_place()

    def create_sensor(self) -> None:
        """
        Creates sensor row in the table if that sensor is not already defined.
        Sensor data comes from meta object.
        """
        if self.sensor_bool is False:
            with self.engine.connect() as self.db:
                json_payload = json.dumps(self.meta.get("sensor").get("data"))
                self.db.execute("commit;")
                self.db.execute(
                    f"""
                    INSERT INTO sensor VALUES ({self.meta.get("sensor").get("id")},
                    '{self.meta.get("sensor").get("name")}',
                    '{json_payload}');
                """
                )
                self.sensor_bool = True
                logging.info("Sensor created")

    def create_place(self) -> None:
        """
        Creates a place row in the table if that place is not already defined.
        Place data comes from meta object.
        """
        if self.place_bool is False:
            with self.engine.connect() as self.db:
                json_payload = json.dumps(self.meta.get("place").get("data"))
                self.db.execute("commit;")
                self.db.execute(
                    f"""
                    INSERT INTO place VALUES ({self.meta.get("place").get("id")},
                    '{self.meta.get("place").get("name")}',
                    '{json_payload}');
                """
                )
                self.place_bool = True
                logging.info("Place created")

    def injection(self) -> None:
        """
        INJECT DATA (ENTRYPOINT) IN TABLE.
        Place and sensor are tried first.
        Only then, measures is injected in an append fashion  pandas to_sql
        """

        self.create_place()
        self.create_sensor()

        if self.sensor_bool is True and self.place_bool is True:
            with self.engine.connect() as self.db:
                self.db.execute("commit;")
                for i in range(len(self.df)):
                    try:
                        self.df.iloc[i : i + 1].to_sql(
                            "measures",
                            con=self.db,
                            if_exists="append",
                            index=False,
                        )
                    except exc.IntegrityError:
                        logging.info(
                            "exc.IntegrityError. Row already present in db %s" % i
                        )

    def search_sensor(self, string_to_search: Union[str, int]) -> None:
        """
        Handy function to search for a given sensor and show its values.
        Search is possible by id or name
        """
        with self.engine.connect() as self.db:

            if isinstance(string_to_search, str):
                string_to_search = string_to_search.lower()

            for r in self.db.execute(
                f"""
                SELECT * FROM sensor WHERE sensor.id LIKE '%{string_to_search}%' OR
                sensor.name LIKE '%{string_to_search}%'
                """
            ):
                print(r)

    def query(self, q: str) -> sqlalchemy.engine.CursorResult:
        """
        Executes a query.
        Returns the cursor
        """
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            return self.db.execute(q)

    def list_tables(self) -> None:
        """
        Prints all tables in the database
        """
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                """
                SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
            """
            ):
                print(r)

    def show_measures(self) -> None:
        """
        Handy function to show all measures.
        """
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                """
                SELECT * FROM measures
            """
            ):
                print(r)

    def show_sensor(self) -> None:
        """
        Show all sensors from the table
        """
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                """
                SELECT * FROM sensor
            """
            ):
                print(r)
