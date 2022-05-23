import pandas as pd
from sqlalchemy import create_engine

# meta = [id,nom] du capteur


class DataBase:
    def __init__(self, ip):
        self.conn_string = f"postgresql+psycopg2://postgres:adminida@{ip}:5432"
        self.engine = create_engine(self.conn_string)
        self.engine.connect().execute("commit;")

    # Afficher les bases
    def liste(self):
        with self.engine.connect() as self.db:
            result = self.db.execute("SELECT datname FROM pg_database;")
            for r in result:
                print(r[0])

    # Vérifier l'existance d'une base
    def exist(self, dbname: str):
        with self.engine.connect() as self.db:
            result = self.db.execute("SELECT datname FROM pg_database;")
            for r in result:
                if r[0].lower() == dbname.lower():
                    return True
        # return false

    # Créer le template
    def create_template(self, tpname: str):
        tpname = tpname.lower()
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            self.db.execute(f"CREATE database {tpname} WITH IS_TEMPLATE = true;")

        conn_tp = f"{self.conn_string}/{tpname}"
        engine = create_engine(conn_tp)
        with engine.connect() as tp:
            tp.execute("commit;")

            # id int | name text
            tp.execute("CREATE TABLE sensor (id integer PRIMARY KEY, nom text);")

            # dates timestamp | val real (6 decimal) | unit text | place_id bigint | sensor_id int
            tp.execute(
                """
                CREATE TABLE measures ("dates" timestamp PRIMARY KEY, "val" real PRIMARY KEY,
                "unit" text PRIMARY KEY, "place_id" bigint,
                "sensor_id" integer REFERENCES sensor (id));
                """
            )
            tp.execute("commit;")
            tp.close()
        engine.dispose()

    # Créer une base
    def create(self, dbname, tpname):
        dbname = dbname.lower()
        if self.exist(dbname) == True:
            print("Cette base existe déjà")
        else:
            with self.engine.connect() as self.db:
                self.db.execute("commit;")
                self.db.execute(f"CREATE database {dbname} WITH TEMPLATE {tpname};")
                print("Database crée")

    def querry(self, querry):
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            return self.db.execute(querry)


class Injection:
    def __init__(self, dbname: str, meta: str, df: pd.DataFrame, ip: str):
        conn_string = f"postgresql+psycopg2://postgres:adminida@{ip}:5432/{dbname}"
        self.engine = create_engine(conn_string)

        self.meta = meta
        self.dbname = dbname.lower()
        self.df = df

    # Verificatin existance sensor
    def exist_sensor(self):
        with self.engine.connect() as self.db:
            for r in self.db.execute("SELECT * FROM sensor"):
                if r[1] == self.meta[1]:
                    return True
            return False

    # Si sensor pas existant, le créer ( PENSER A METTRE EN LOWER OU UPPER )
    def create_sensor(self):
        if self.exist_sensor() == False:
            with self.engine.connect() as self.db:
                self.db.execute("commit;")
                self.db.execute(
                    f"INSERT INTO sensor VALUES ({self.meta[0]},'{self.meta[1]}');"
                )

    # Injection des données
    def injection(self):
        self.create_sensor()

        if self.exist_sensor() == True:
            with self.engine.connect() as self.db:
                self.db.execute("commit;")
                self.df.to_sql("measures", con=self.db, if_exists="append", index=False)

    def show_measures(self):
        with self.engine.connect() as self.db:
            for r in self.db.execute("SELECT * FROM measures"):
                print(r)

    def search_sensor(self, string_to_search):
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                f"SELECT * FROM sensor WHERE sensor.id LIKE '%{string_to_search}%' OR sensor.name LIKE '%{string_to_search}%'"
            ):
                print(r)

    def querry(self, querry):
        with self.engine.connect() as self.db:
            self.db.execute("commit;")
            return self.db.execute(querry)

    def list_tables(self):
        with self.engine.connect() as self.db:
            for r in self.db.execute(
                "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
            ):
                print(r)

    def show_sensor(self):
        with self.engine.connect() as self.db:
            for r in self.db.execute("SELECT * FROM sensor"):
                print(r)
