from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import sys  

if __name__=="__main__":
    try:
        trainingpipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=trainingpipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Starting Data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data Ingestion Completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)