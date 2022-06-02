#
import datetime

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

df = pd.read_csv("/home/camilodlt/Downloads/Histo_meteo.csv")

eng: str = "postgresql+psycopg2"
user: str = "postgres:adminida"
port: str = "5432"
ip: str = "localhost"
dbname: str = "enedis_cristiona_v2"

conn_string = f"{eng}://{user}@{ip}:{port}/{dbname}"
print(conn_string)
engine = create_engine(conn_string)

df = df.rename(columns={"Date": "dates"})
df["dates"] = pd.to_datetime(df["dates"])
df.to_sql("histo_meteo", con=engine)
