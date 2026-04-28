import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files(self) -> bool:
        try:
            dataset_dir = os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            all_files = os.listdir(dataset_dir)

            required_files = set(self.config.ALL_REQUIRED_FILES)
            present_files = set(all_files)

            
            missing_files = required_files - present_files

            
            extra_files = present_files - required_files

            validate_status = len(missing_files) == 0 and len(extra_files) == 0

            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Data Validation Status: {validate_status}\n")
                f.write(f"Missing Files: {list(missing_files)}\n")
                f.write(f"Extra Files: {list(extra_files)}\n")

            return validate_status

        except Exception as e:
            raise e