from source.mlproject.logger import logging
from source.mlproject.expection import CustomException
from source.mlproject.components.data_ingestion import DataIngestion
from source.mlproject.components.data_transformation import DataTransformation
from source.mlproject.components.model_training import ModelTrainer
import sys


if __name__ == "__main__":
    logging.info("Execution inside app.py")
    try:
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        train_dataset, test_dataset, _ = data_transformation.initiate_data_transformation(
            train_path, test_path
        )

        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer (train_dataset, test_dataset))
        print(f"Best Model selected: {model_trainer.best_model}")
        print (f"Train Dataset Metrics: RMSE: {model_trainer.train_rmse}, MSE: {model_trainer.train_mse}, R2 Score: {model_trainer.train_r2_score}")
        print (f"Test Dataset Metrics: RMSE: {model_trainer.test_rmse}, MSE: {model_trainer.test_mse}, R2 Score: {model_trainer.test_r2score}") 

    except Exception as e:
        logging.info("Custom Excpetion")
        raise CustomException (e, sys)
