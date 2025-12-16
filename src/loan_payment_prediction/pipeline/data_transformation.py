from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.data_transformation import DataTransformation  
from src.loan_payment_prediction import logger
from pathlib import Path



STAGE_NAME = "Data Transformation Stage"


class DataTransformationPipeline:
    def __init__(self):
        pass    
    
    
    
    def initiate_data_transformation(self):
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
            config=ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.train_test_splitting()
        
            logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
        except Exception as e:
            logger.exception(e)
            raise e
        
            
            
if __name__ == "__main__":     
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        data_transformation = DataTransformationPipeline()
        data_transformation.initiate_data_transformation()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

            
            
        