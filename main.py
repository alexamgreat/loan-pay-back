from src.loan_payment_prediction import logger
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))
from pathlib import Path

from src.loan_payment_prediction.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from loan_payment_prediction.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.loan_payment_prediction.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.loan_payment_prediction.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline  
from src.loan_payment_prediction.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline 
from src.loan_payment_prediction.pipeline.prediction_pipeline import PredictionPipelineRunner 
   



# Stage 1 - Data Ingestion
STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.initiate_data_ingestion()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    logger.exception(e) 
    raise e


# Stage 2 - Data Validation
STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    logger.exception(e)
    raise e




STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Model Trainer Stage"
try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrainerTrainingPipeline()
    model_trainer.initiate_model_training()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")      
    
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Model Evaluation Stage"
try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationPipeline()
    model_evaluation.initiate_model_evaluation()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
except Exception as e:
        logger.exception(e)
        raise e
    
    
STAGE_NAME = "Prediction Stage"
try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        obj = PredictionPipelineRunner()
        obj.initiate_prediction()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        logger.exception(e)
        raise e