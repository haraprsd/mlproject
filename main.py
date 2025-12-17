import sys
from source.mlproject.logger import logging
from source.mlproject.expection import CustomException
from source.mlproject.components.data_ingestion import data_ingestion



def main():
    logging.info("Hello from mlproject!")
    try:
        data_ingestion()
#        1 / 0
    except Exception as e:
        raise CustomException(e, sys)
    

if __name__ == "__main__":
    main()
