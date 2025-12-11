import os
import yaml
from src.loan_payment_prediction import logger
import json
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, List
from box.exceptions import BoxValueError



def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (str): The path to input
        
    Raises:
        valeuError: If the YAML file is empty or cannot be read.    
    Return:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
    """
    try:
    
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file) or {}
            logger.info(f"YAML file {path_to_yaml} loaded successfully.")
            return ConfigBox(content)
        
    except Exception as e:
        logger.error(f"Error reading YAML file at {path_to_yaml}: {e}")
        raise e
    
    
    

def create_directories(path_to_directories, verbose:bool = True):
    """Creates multiple directories.
    Args:
        path_to_directories (list): List of directory paths to be created.
        verbose (bool, optional): If True, logs the creation of each directory. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")
            


def save_json(path: Path, data: Any) -> None:
    """Saves a dictionary as a JSON file.
    Args:
        path (Path): The file path where the JSON data will be saved.
        data (dict): The dictionary data to be saved as JSON.
    """
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"JSON file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving JSON file at {path}: {e}")
        raise e   
    
    

def save_bin(path: Path, data: Any) -> None:
    """Saves data to a binary file using joblib.
    Args:
        path (Path): The file path where the binary data will be saved.
        data (Any): The data to be saved in binary format.
    """
    import joblib

    try:
        with open(path, 'wb') as bin_file:
            joblib.dump(data, bin_file)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving binary file at {path}: {e}")
        raise e             
            