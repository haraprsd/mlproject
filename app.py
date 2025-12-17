from source.mlproject.logger import logging
from source.mlproject.expection import CustomException
from source.mlproject.components.data_ingestion import DataIngestion
import sys


if __name__ == "__main__":
    logging.info("Execution inside app.py")
    try:
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()

    except Exception as e:
        logging.info("Custom Excpetion")
        raise CustomException (e, sys)
