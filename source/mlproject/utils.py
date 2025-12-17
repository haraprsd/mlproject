from dotenv import load_dotenv
import os
import sys
from source.mlproject.expection import CustomException
from source.mlproject.logger import logging
import pandas as pd
#import psycopg
from sqlalchemy import create_engine

load_dotenv()  # Load .env file FIRST

host = os.getenv("host")
uname = os.getenv("uname")
password = os.getenv("password")
db = os.getenv("db")

def read_sql_data():
    logging.info("Reading postgreSQL started")
    try:
        engine = create_engine(f'postgresql+psycopg://{uname}:{password}@{host}:5432/{db}')
        logging.info ("Connected to Database")
        df = pd.read_sql_query("select * from score", engine)

        return df
    except Exception as e:
        raise CustomException(e, sys)    
