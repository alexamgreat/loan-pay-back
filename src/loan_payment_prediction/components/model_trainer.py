import pandas as pd
import numpy as np
import os
from src.loan_payment_prediction import logger
from sklearn.linear_model import SGDRegressor
import joblib
from pathlib import Path
from src.loan_payment_prediction.entity.config_entity import ModelTrainerConfig 
from src.loan_payment_prediction.utils.common import create_directories, read_yaml




class ModelTrainer:
    def __init__(self, config):
        self.config = config

    def train_model(self):
        logger.info("Starting model training step")

        # Load data
        train_data = pd.read_csv(self.config.train_data_dir)
        test_data = pd.read_csv(self.config.test_data_dir)

        logger.info("Training and test data loaded")

        # Split features and target
        train_x = train_data.drop([self.config.target_column], axis=1)
        train_y = train_data[self.config.target_column]

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]

        #Memory optimization
        train_x = train_x.astype("float32")
        test_x = test_x.astype("float32")
        train_y = train_y.astype("float32")
        test_y = test_y.astype("float32")

        # Initialize SGDRegressor with ElasticNet penalty
        model = SGDRegressor(
            penalty="elasticnet",
            alpha=self.config.alpha,
            l1_ratio=self.config.l1_ratio,
            max_iter=self.config.max_iter,
            tol=self.config.tol,
            random_state=42
        )

        logger.info("Training SGDRegressor (ElasticNet)")
        model.fit(train_x, train_y)

        # Save model
        os.makedirs(self.config.root_dir, exist_ok=True)    
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(model, model_path)

        logger.info(f"Model saved at {model_path}")

        return model




