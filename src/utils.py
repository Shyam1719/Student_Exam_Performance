import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging
def save_object(file_path, obj):
    try:
        logging.info("In save_object function")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
        logging.info("In save_object function object saved successfully")
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_models(X_train, Y_train,X_test,Y_test,models):
    try:
        logging.info("In evaluate_models function")
        results = {}
        for i in range(len(models)):
            model =list(models.values())[i]
            model.fit(X_train,Y_train)
            Y_train_pred = model.predict(X_train)
            Y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(Y_train,Y_train_pred)
            test_model_score = r2_score(Y_test,Y_test_pred)
            results[list(models.keys())[i]] = test_model_score
        logging.info("In evaluate_models function models evaluated successfully")
        return results
    except Exception as e:
        raise CustomException(e, sys)