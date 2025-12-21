from source.mlproject.logger import logging
from source.mlproject.expection import CustomException
from source.mlproject.components.data_ingestion import DataIngestion
from source.mlproject.components.data_transformation import DataTransformation
import sys


if __name__ == "__main__":
    logging.info("Execution inside app.py")
    try:
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        train_dataset, test_dataset, pickle_path = data_transformation.initiate_data_transformation(
            train_path, test_path
        )

    except Exception as e:
        logging.info("Custom Excpetion")
        raise CustomException (e, sys)
