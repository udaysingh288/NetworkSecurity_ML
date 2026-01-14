from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
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
        data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipeline_config)
        data_validation= DataValidation(data_ingestion_artifact=dataingestionartifact,
                                        data_validation_config= data_validation_config)
        logging.info("Starting Data Validation")
        datavalidationartifact= data_validation.initiate_data_validation()
        print(datavalidationartifact)
        logging.info("Data Validation Completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
