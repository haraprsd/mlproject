import sys
import os
import numpy as np
from source.mlproject.expection import CustomException
from source.mlproject.logger import logging
from dataclasses import dataclass

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from source.mlproject.utils import save_pickle_object

@dataclass
class ModelTrainerConfig:
    model_trainer_file_path = os.path.join('artifact', 'model.pkl')

class ModelTrainer:
    def __init__(self):
       self.model_trainer_config = ModelTrainerConfig()
       self.train_rmse = -1
       self.train_mse = -1
       self.train_r2_score = -1
       self.test_rmse = -1
       self.test_mse = -1
       self.test_r2score = -1
       self.best_model = None


    def initiate_model_trainer(self, train_arr, test_arr):
       try:
           logging.info("Split data into X and Y")
           X_train, y_train, X_test, y_test = (
               train_arr[:,:-1],
               train_arr[:,-1],
               test_arr[:,:-1],
               test_arr[:,-1]
           )

           model = {
               "Decision Tree": DecisionTreeRegressor(),
               "Linear Regression": LinearRegression(),
               "XGBRegressor": XGBRegressor(),
           }

           hyper_params = {
               "Decision Tree" : {
                   'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                   'splitter':['best', 'random'],
                   'max_features':['sqrt','log2'],
               },
               "Linear Regression" : {},
               "XGBRegressor" : {
                   'learning_rate': [.001,.01,.05,.1],
                   'n_estimators': [8,16,32,64,128,256],
               }
           } 
       
           model_report:dict = self.evaluate_model(X_train, y_train, X_test, y_test, model, hyper_params)

           #Get best model score from the dist
           best_model_score = max(sorted(model_report.values()))
           best_model_name = list(model_report.keys())[
               list(model_report.values()).index(best_model_score)
           ] 
           best_model = model[best_model_name]

           if best_model_score <0.6:
                raise CustomException("No best model found")
           logging.info(f"Best model found for traning and test data {best_model_name}: {best_model_score}")    

           save_pickle_object(
               self.model_trainer_config.model_trainer_file_path,
               obj=best_model
           ) 

           return best_model_score
       
       except Exception as e:
           raise CustomException(e, sys)

    def evaluate_model(self, X_train, y_train, X_test, y_test, models, param):
        try:
            report = {}

            for i in range(len(list(models))):
                model = list(models.values())[i]
                params = list(param.values())[i]

                gs = GridSearchCV(model, params, cv=3)
                gs.fit(X_train, y_train)

                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                test_r2_score = r2_score(y_test, y_test_pred)
                if (test_r2_score > self.test_r2score):
                    self.train_r2_score = r2_score(y_train, y_train_pred)
                    self.train_mse = mean_squared_error (y_train, y_train_pred)
                    self.train_rmse = np.sqrt(self.train_mse)

                    self.test_r2score = r2_score(y_test, y_test_pred)
                    self.test_mse = mean_squared_error(y_test, y_test_pred)
                    self.test_rmse = np.sqrt(self.test_mse)
                    self.best_model = model

                report[list(models.keys())[i]] = test_r2_score
                #report[list(models.keys())[i]] = test_model_MSE
            return report
        except Exception as e:
            raise CustomException (e, sys)