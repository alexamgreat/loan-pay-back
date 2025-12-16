import urllib.request as request
from src.loan_payment_prediction import logger
import zipfile 
import os 
from src.loan_payment_prediction.entity.config_entity import (DataIngestionConfig)

from pathlib import Path



class DataIngestion:
    def __init__(self, config):
        self.config = config

            
            
            
    def extract_zip_file(self, zip_file_path: str, extract_dir: str):
        import zipfile
        zip_file_path = Path(zip_file_path)
        extract_dir = Path(extract_dir)
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        
        logger.info(f"Extracting zip file: {zip_file_path} into dir: {extract_dir}")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        logger.info(f"Extraction completed")