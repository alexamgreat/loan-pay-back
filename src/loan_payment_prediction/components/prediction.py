import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import os
import pandas as pd
import joblib
import logging  

from src.loan_payment_prediction import logger
from src.loan_payment_prediction.entity.config_entity import PredictionConfig
   







logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionPipeline:
    def __init__(self, config):
        self.config = config   # Store the config

    def load_artifacts(self):
        logger.info("Loading saved model and preprocessing pipeline...")

        if not os.path.exists(self.config.model_dir):
            raise FileNotFoundError(f"Model not found at {self.config.model_dir}")

        if not os.path.exists(self.config.pipeline_path):
            raise FileNotFoundError(f"Pipeline not found at {self.config.pipeline_path}")

        self.model = joblib.load(self.config.model_dir)
        self.pipeline = joblib.load(self.config.pipeline_path)

        logger.info(f"Model loaded from: {self.config.model_dir}")
        logger.info(f"Pipeline loaded from: {self.config.pipeline_path}")

    def load_input_data(self):
        if not os.path.exists(self.config.input_file):
            raise FileNotFoundError(f"Input file not found at {self.config.input_file}")

        logger.info(f"Loading test data from {self.config.input_file}")
        df = pd.read_csv(self.config.input_file)
        logger.info(f"Test data shape: {df.shape}")
        return df

    def transform_data(self, df: pd.DataFrame):
        logger.info("Applying saved transformations to test data...")
        return self.pipeline.transform(df)

    def predict(self, transformed_data):
        logger.info("Generating predictions...")
        return self.model.predict(transformed_data)

    def save_predictions(self, predictions, df):
        os.makedirs(self.config.root_dir, exist_ok=True)

        result_df = pd.DataFrame({
            "id": df["id"].values,
            "loan_paid_back": predictions
        })

        result_df.to_csv(self.config.output_file, index=False)
        logger.info(f"Predictions saved to {self.config.output_file}")

    def run(self):
        self.load_artifacts()
        df = self.load_input_data()
        transformed_data = self.transform_data(df)
        predictions = self.predict(transformed_data)
        self.save_predictions(predictions, df)
        return predictions
