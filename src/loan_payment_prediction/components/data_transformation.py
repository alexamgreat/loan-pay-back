import os
from src.loan_payment_prediction import logger
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from src.loan_payment_prediction.entity.config_entity import DataTransformationConfig


class DataTransformation:
    
    def __init__(self, config:DataTransformationConfig):
        self.config = config
     
     
    def train_test_splitting(self)-> None:
        data= pd.read_csv(self.config.data_dir)
    #split the data inti training and testing
        train, test = train_test_split(data, test_size=0.2, random_state=42)
        
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)
        
        logger.info(f"train and test data saved in {self.config.root_dir} ")
        logger.info(f"train data shape: {train.shape} ") 
        logger.info(f"test data shape: {test.shape} ")
        
        
        print("train.shape")
        print("test.shape")    