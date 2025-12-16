
from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.data_ingestion import DataIngestion
from src.loan_payment_prediction import logger




STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:

    def __init__(self):
        pass
        
        
    def initiate_data_ingestion(self):
        config=ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.extract_zip_file(
            zip_file_path=data_ingestion_config.local_data_file,
            extract_dir=data_ingestion_config.unzip_dir
        )
    
    
    
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.initiate_data_ingestion()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
    except Exception as e:
        logger.exception(e)
        raise e
        