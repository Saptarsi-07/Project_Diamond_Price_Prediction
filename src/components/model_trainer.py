import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet


from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

from dataclasses import dataclass

import os,sys


@dataclass
class ModelTrainerconfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
     self.model_trainer_config=ModelTrainerconfig()

    def initiate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting Dependent and Independent variables from train and test data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                'LinearRegression':LinearRegression(),
                'Lasso':Lasso(),
                'Ridge':Ridge(),
                'ElasticNet':ElasticNet(),
                
                    
            }

            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print('\n=================================================================')
            logging.info(f'model Report : {model_report}')

             #To get the best score
            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            print(f'BEST MODEL NAME: {best_model_name}, R2: {(best_model_score)}')
            print('\n===============================================================================')
            logging.info("best model found")


            save_object(

                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model

            )



        except Exception as e:

         raise CustomException(e,sys)
                                         
