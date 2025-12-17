import os
import sys
# Use package-relative imports so this module works when executed as part
# of the `source.mlproject` package (run with `-m` or from package entry).
from ..expection import CustomException
from ..logger import logging
import pandas as pd
from dataclasses import dataclass
from source.mlproject.database.postgres import read_sql_data, save_to_sql
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_csv:str = os.path.join('artifact', 'train.csv')
    train_data_parquet = os.path.join('artifact', 'train.parquet')
    test_data_csv:str = os.path.join('artifact', 'test.csv')
    test_data_parquet = os.path.join('artifact', 'test.parquet')
    raw_data_path:str = os.path.join('artifact','raw.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Reading from PostgreSQL")
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df = read_sql_data()
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            train_data, test_data = train_test_split(df, train_size=.2, random_state=42)
            
            train_data.to_csv(self.ingestion_config.train_data_csv, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_csv, index=False, header=True)

            train_data.to_parquet(self.ingestion_config.train_data_parquet, index=False)
            test_data.to_parquet(self.ingestion_config.test_data_parquet, index=False)

            save_to_sql(train_data, table_name="train_data")
            save_to_sql(test_data, table_name="test_data")
            
            logging.info("Data ingestion is completed")
        except Exception as e:
            raise CustomException(e, sys)
