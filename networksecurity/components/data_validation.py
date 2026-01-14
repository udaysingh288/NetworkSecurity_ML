
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import sys
import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp ###to check the data drift
from networksecurity.utils.main_utils import read_yaml_file,write_yaml_file


class DataValidation:
    def __init__(self,data_validation_config, data_ingestion_artifact):
        try:
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns= len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)== number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_required_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            schema_columns = self._schema_config["columns"]
            required_columns = [list(column.keys())[0] for column in schema_columns]
            missing_columns = set(required_columns) - set(dataframe.columns)
            if missing_columns:
                logging.info(f"Missing columns in dataframe: {sorted(missing_columns)}")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self,base_dataframe:pd.DataFrame, current_dataframe:pd.DataFrame, threshold:float=0.05)-> bool:
        try:
            drift_report= {}
            drift_found = False
            for column in base_dataframe.columns:
                d_statistic, p_value= ks_2samp(base_dataframe[column], current_dataframe[column])
                if p_value>threshold:
                    drift_report[column]={
                        "p_value": float(p_value),
                        "d_statistic": float(d_statistic),
                        "same_distribution": True
                    }
                else:
                    drift_found = True
                    drift_report[column]={
                        "p_value": float(p_value),
                        "d_statistic": float(d_statistic),
                        "same_distribution": False
                    }
            drif_report_file_path= self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drif_report_file_path), exist_ok=True) 
            write_yaml_file(file_path= drif_report_file_path, content= drift_report)
            return not drift_found
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
        
    
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            logging.info("Starting Data Validation")

            #reading the train and test file
            train_file_path= self.data_ingestion_artifact.trained_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            train_datframe= DataValidation.read_data(train_file_path)
            test_dataframe= DataValidation.read_data(test_file_path)

            #validating the number of columns
            status= self.validate_number_of_columns(train_datframe)
            if not status:
                raise Exception("Number of columns in training data is not as per schema")
            
            status= self.validate_number_of_columns(test_dataframe)
            if not status:
                raise Exception("Number of columns in testing data is not as per schema")
            
            #validating the columns names
            status= self.validate_required_columns(train_datframe)
            if not status:
                raise Exception("Columns in training data are not as per schema")

            status= self.validate_required_columns(test_dataframe)
            if not status:
                raise Exception("Columns in testing data are not as per schema")
            
            #checking data drift
            status = self.detect_data_drift(base_dataframe= train_datframe, current_dataframe= test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_datframe.to_csv(self.data_validation_config.valid_train_file_path, index= False)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index= False)
           

            validation_artifact= DataValidationArtifact(
                validation_status= status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info("Data Validation Completed")

            return validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
