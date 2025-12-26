import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow   
import mlflow.sklearn
import numpy as np
import joblib 
from src.loan_payment_prediction import logger
from src.loan_payment_prediction.entity.config_entity import ModelEvaluationConfig
from src.loan_payment_prediction.utils.common import save_json
from pathlib import Path
import os
os.environ['MLFLOW_TRACKING_URI'] = "https://dagshub.com/alexamgreat/loan-pay-back.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "alexamgreat"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "3a89fd7489fff804a2a2ef260ce8c6773ad8561f"

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, predicted) -> dict:
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        r2 = r2_score(actual, predicted)

        return {
            "rmse": rmse,
            "mae": mae,
            "r2_score": r2
        }

    def log_into_mlflow(self):
        #close any existing mlflow runs
        if mlflow.active_run() is not None:
            mlflow.end_run()
        # Load data and model
        test_data = pd.read_csv(self.config.test_data_dir)
        model = joblib.load(self.config.model_dir)

        # SAFE pandas usage (NO list, NO Box)
        test_x = test_data.drop(columns=self.config.target_column, axis=1)
        test_y = test_data[self.config.target_column]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_uri_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predictions = model.predict(test_x)
            metrics = self.eval_metrics(test_y, predictions)

            rmse  = metrics["rmse"]
            mae   = metrics["mae"]
            r2    = metrics["r2_score"]
        # Save metrics locally  
        metrics_path = Path(self.config.root_dir) / self.config.metrics_file_name
        metrics_path.parent.mkdir(parents=True, exist_ok=True)

        save_json(path=metrics_path, data=metrics)  

        # Log params correctly
        mlflow.log_params(self.config.all_params)

# Log metrics to MLflow
        mlflow.log_metric("rmse", metrics["rmse"])
        mlflow.log_metric("mae", metrics["mae"])
        mlflow.log_metric("r2_score", metrics["r2_score"])

        
        
        # Log model
        if tracking_uri_store != "file":
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name="LoanPayBackModel"
            )
        else:
            mlflow.sklearn.log_model(model, "model")
        print("Model evaluation metrics logged into MLflow successfully.")  