import pandas as pd
import os
from src.loan_payment_prediction import logger
from src.loan_payment_prediction.entity.config_entity import DataValidationConfig    


class DataValidation:
    def __init__(self, config: DataValidationConfig ):
        self.config = config
         

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True
            
            # Load dataset
            data = pd.read_csv(self.config.data_dir)
            all_columns = list(data.columns)
            
            # Schema keys
            required_columns = self.config.all_schema.keys()
            
            # Validate each column
            for column in required_columns:
                if column not in all_columns:
                    validation_status = False
                    with open(self.config.status_file, "a") as f: 
                        f.write(f"Column {column} is missing in the data\n")
                    logger.info(f"Column {column} is missing in the data")
                    
            return validation_status
        
        except Exception as e:
            logger.exception(e)
            raise e


