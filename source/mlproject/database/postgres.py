from dotenv import load_dotenv, find_dotenv
import os
import sys
from source.mlproject.expection import CustomException
from source.mlproject.logger import logging
import pandas as pd
#import psycopg
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path, override=True)
else:
    load_dotenv(override=True)

# Try direct DATABASE_URL first, otherwise build from components
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    DB_USER = os.getenv("uname")
    DB_PASSWORD = os.getenv("password")
    DB_HOST = os.getenv("DB_HOST") or os.getenv("host") or "localhost"
    DB_PORT = os.getenv("DB_PORT") or os.getenv("port") or "5432"
    DB_NAME = os.getenv("DB_NAME") or os.getenv("db")

    if DB_USER and DB_PASSWORD and DB_NAME:
        DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        logging.error(
            "DATABASE_URL not set and missing components to build it from env (user=%s host=%s db=%s)",
            DB_USER,
            DB_HOST,
            DB_NAME,
        )
        raise CustomException("DATABASE_URL not set and missing components to build it from env", sys)

logging.info("Using DATABASE_URL: %s", DB_URL if DB_URL else "<none>")
engine = create_engine(
    DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)


def read_sql_data():
    logging.info("Reading postgreSQL started")
    try:
        #engine = create_engine(f'postgresql+psycopg://{uname}:{password}@{host}:5432/{db}')
        logging.info ("Connected to Database")
        df = pd.read_sql_query("select * from score", engine)

        return df
    except Exception as e:
        raise CustomException(e, sys)    

def save_to_sql(
    df:pd.DataFrame, table_name:str
) -> None:
    logging.info("Saving data in postgreSQL")
    try:
        with engine.begin() as connection:
            df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)
            logging.info(f"Data saved to table {table_name} successfully")
    except Exception as e:
        raise CustomException(e,sys)
    