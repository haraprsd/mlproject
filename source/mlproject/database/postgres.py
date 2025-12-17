from dotenv import load_dotenv
import os
import sys
from source.mlproject.expection import CustomException
from source.mlproject.logger import logging
import pandas as pd
#import psycopg
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()  # Load .env file FIRST

#host = os.getenv("host")
#uname = os.getenv("uname")
#password = os.getenv("password")
#db = os.getenv("db")
DB_URL = os.getenv("DATABASE_URL")

def get_engine() -> Engine:
    try:
        engine = create_engine(
            DB_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True
        )
        logging.info("Database engine created successfully")
        return engine
    except SQLAlchemyError as e:
        logging.error("Error creating database engine")
        raise CustomException(e, sys)

ENGINE = get_engine()

def read_sql_data():
    logging.info("Reading postgreSQL started")
    try:
        #engine = create_engine(f'postgresql+psycopg://{uname}:{password}@{host}:5432/{db}')
        logging.info ("Connected to Database")
        df = pd.read_sql_query("select * from score", ENGINE)

        return df
    except Exception as e:
        raise CustomException(e, sys)    

def save_to_sql(
    df:pd.DataFrame, table_name:str
) -> None:
    logging.info("Saving data in postgreSQL")
    try:
        with ENGINE.begin() as connection:
            df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)
            logging.info(f"Data saved to table {table_name} successfully")
    except Exception as e:
        raise CustomException(e,sys)
    