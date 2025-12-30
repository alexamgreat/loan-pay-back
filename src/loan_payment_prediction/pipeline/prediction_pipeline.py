from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.prediction import PredictionPipeline
from src.loan_payment_prediction import logger

STAGE_NAME = "Prediction Stage"

class PredictionPipelineRunner:

    def __init__(self):
        pass

    def initiate_prediction(self):
        config_manager = ConfigurationManager()
        prediction_config = config_manager.get_prediction_config()

        # Use the actual imported PredictionPipeline
        predictor = PredictionPipeline(config=prediction_config)
        predictor.run()     # <-- executes load, transform, predict, save


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        obj = PredictionPipelineRunner()
        obj.initiate_prediction()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e

