from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.model_evaluation import ModelEvaluation    
from src.loan_payment_prediction import logger





STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationPipeline:

    def __init__(self):
        pass
        
        
    def initiate_model_evaluation(self):
        config=ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.log_into_mlflow()
        
        
        
        
        
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        obj= ModelEvaluationPipeline()
        obj.initiate_model_evaluation()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
    except Exception as e:
        logger.exception(e)
        raise e