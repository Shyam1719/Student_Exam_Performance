import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocess_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    def get_data_transformation_object(self,input_train_data):
        try:
            numerical_columns=list(input_train_data.select_dtypes(exclude='object').columns)
            categorical_columns= list(input_train_data.select_dtypes(include='object').columns)
            
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('std_scaler', StandardScaler()),
                ]
            )
            logging.info("Numerical pipline created")
            cate_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder()),
                    # ('std_scaler',StandardScaler())
                ]
            )
            logging.info("Categorical pipline created")
            #Combine both pipline
            preprocessor = ColumnTransformer(
                [
                    ('num', num_pipeline, numerical_columns),
                    ('cat', cate_pipeline, categorical_columns)
                ]
            )
            logging.info("Column transformer created")
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path,target_columns):
        try:
            logging.info("Initiating data transformation")
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)
            logging.info("Train and Test Data read successfully")
            input_feature_train_df=train_data.drop(columns=[target_columns],axis=1)
            target_feature_train_df=train_data[target_columns]
            
            input_feature_test_df=test_data.drop(columns=[target_columns],axis=1)
            target_feature_test_df=test_data[target_columns]
            logging.info("Applying preprocessing object on train and test data")
            
            preprocessor_obj = self.get_data_transformation_object(input_train_data=input_feature_train_df)
            logging.info("Data transformation object obtained")
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            logging.info("Input feature of Training data transformed successfully")
            
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
            logging.info("Input feature of test data transformed successfully")
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            
            logging.info("Data transformation completed successfully")
            
            logging.info("Saving preprocessing object")
            save_object(file_path=self.data_transformation_config.preprocess_obj_file_path,obj=preprocessor_obj)
            logging.info("Preprocessing object saved successfully")
            
            return (train_arr,test_arr)
        except Exception as e:
            raise CustomException(e,sys)