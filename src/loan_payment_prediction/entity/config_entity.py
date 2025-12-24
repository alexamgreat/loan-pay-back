from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    
    
    
    
@dataclass
class DataValidationConfig:
    root_dir: Path
    data_dir: Path
    status_file: str
    all_schema: dict
    
    

@dataclass
class DataTransformationConfig:
    root_dir:Path
    data_dir:Path
    schema_file_path:Path
    
    
@dataclass
class ModelTrainerConfig:
    root_dir:Path
    train_data_dir:Path
    test_data_dir:Path
    model_name:str
    alpha:float
    l1_ratio:float
    max_iter:int
    tol:float
    target_column:str    