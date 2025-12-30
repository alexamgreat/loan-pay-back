import pandas as pd
import os
from src.loan_payment_prediction import logger
from src.loan_payment_prediction.entity.config_entity import DataValidationConfig    


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self):
        try:
            # Load your data
            df = pd.read_csv(self.config.data_dir)
            
            # Get expected columns and types from schema
            schema = self.config.all_schema  # dictionary like your COLUMNS
           
            missing_cols = []

            # Loop through schema columns
            for col, dtype in schema.items():
                if col not in df.columns:
                    missing_cols.append(col)
                    continue
                
                # Cast numeric columns
                if dtype in ["float64", "int64"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                # Cast object columns
                else:
                    df[col] = df[col].astype(str)

            if missing_cols:
                raise ValueError(f"Missing columns in dataset: {missing_cols}")

           
            logger.info("All columns validated successfully!")
            return df  # return the cleaned DataFrame

        except Exception as e:
            logger.error(f"Error during column validation: {e}")
            raise e