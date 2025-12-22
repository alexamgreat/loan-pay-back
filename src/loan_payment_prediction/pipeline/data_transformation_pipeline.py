from src.loan_payment_prediction.config.configuration import ConfigurationManager
from src.loan_payment_prediction.components.data_transformation import DataTransformation  
from src.loan_payment_prediction import logger
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import os
import yaml



STAGE_NAME = "Data Transformation Stage"


class DataTransformationPipeline:

    def __init__(self):
        config_manager = ConfigurationManager()
        self.config = config_manager.get_data_transformation_config()

        self.pipeline = None
        self.target_column = self._load_target_column()
        self.drop_columns = self._load_drop_columns()

    # ------------------------
    # Load schema values
    # ------------------------

    def _load_schema(self) -> dict:
        with open(self.config.schema_file_path, "r") as f:
            return yaml.safe_load(f)

    def _load_target_column(self) -> str:
        schema = self._load_schema()

        if "TARGET_COLUMN" not in schema:
            raise KeyError("TARGET_COLUMN not found in schema")

        return schema["TARGET_COLUMN"]["name"]

    def _load_drop_columns(self) -> list:
        schema = self._load_schema()
        return schema.get("DROP_COLUMNS", [])

    # ------------------------
    # Load data
    # ------------------------

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.config.data_dir)
        logger.info(f"Data loaded with shape: {df.shape}")
        return df

    # ------------------------
    # Split features & target
    # ------------------------

    def split_features_target(self, df: pd.DataFrame):
        if self.target_column not in df.columns:
            raise ValueError(
                f"Target column '{self.target_column}' not found in dataset"
            )

        X = df.drop(columns=[self.target_column] + self.drop_columns, errors="ignore")
        y = df[self.target_column]

        return X, y

    # ------------------------
    # Build preprocessing pipeline
    # ------------------------

    def build_pipeline(self, X: pd.DataFrame):

        categorical_cols = X.select_dtypes(include="object").columns.tolist()
        numerical_cols = X.select_dtypes(exclude="object").columns.tolist()

        logger.info(f"Categorical columns: {categorical_cols}")
        logger.info(f"Numerical columns: {numerical_cols}")

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numerical_cols),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
            ]
        )

        self.pipeline = Pipeline(
            steps=[("preprocessor", preprocessor)]
        )

        return categorical_cols, numerical_cols

    # ------------------------
    # Main execution
    # ------------------------

    def initiate_data_transformation(self):

        # 1. Load data
        data = self.load_data()

        # 2. Train-test split
        train_df, test_df = train_test_split(
            data, test_size=0.2, random_state=42
        )

        # 3. Split X & y
        X_train, y_train = self.split_features_target(train_df)
        X_test, y_test = self.split_features_target(test_df)

        logger.info(
            f"Train X shape: {X_train.shape}, Test X shape: {X_test.shape}"
        )

        # 4. Build pipeline
        categorical_cols, numerical_cols = self.build_pipeline(X_train)

        # 5. Fit & transform
        X_train_arr = self.pipeline.fit_transform(X_train)
        X_test_arr = self.pipeline.transform(X_test)

        # 6. Get feature names
        preprocessor = self.pipeline.named_steps["preprocessor"]
        ohe = preprocessor.named_transformers_["cat"]

        ohe_cols = ohe.get_feature_names_out(categorical_cols)
        final_columns = numerical_cols + list(ohe_cols)

        # 7. Convert back to DataFrame
        train_transformed_df = pd.DataFrame(X_train_arr, columns=final_columns)
        train_transformed_df[self.target_column] = y_train.values

        test_transformed_df = pd.DataFrame(X_test_arr, columns=final_columns)
        test_transformed_df[self.target_column] = y_test.values

        # 8. Save outputs
        os.makedirs(self.config.root_dir, exist_ok=True)

        train_path = os.path.join(self.config.root_dir, "train_transformed.csv")
        test_path = os.path.join(self.config.root_dir, "test_transformed.csv")
        pipeline_path = os.path.join(self.config.root_dir, "pipeline.joblib")

        train_transformed_df.to_csv(train_path, index=False)
        test_transformed_df.to_csv(test_path, index=False)
        joblib.dump(self.pipeline, pipeline_path)

        logger.info(f"Train data saved to: {train_path}")
        logger.info(f"Test data saved to: {test_path}")
        logger.info(f"Pipeline saved to: {pipeline_path}")
        logger.info("Data transformation completed successfully")

        return (
            X_train_arr,
            X_test_arr,
            y_train.values,
            y_test.values
        )

        
            
            
if __name__ == "__main__":     
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        data_transformation = DataTransformationPipeline()
        data_transformation.initiate_data_transformation()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

            
            
        