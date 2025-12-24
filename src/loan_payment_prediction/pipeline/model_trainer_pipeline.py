from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.model_trainer import ModelTrainer    
from src.loan_payment_prediction import logger



STAGE_NAME = "Model Trainer Stage"

class ModelTrainerTrainingPipeline:

    def __init__(self):
        pass
        
        
    def initiate_model_training(self):
        config=ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model = model_trainer.train_model()
        logger.info(f"Trained model: {model}")
        
        
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        obj= ModelTrainerTrainingPipeline()
        obj.initiate_model_trainer()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
    except Exception as e:
        logger.exception(e)
        raise e