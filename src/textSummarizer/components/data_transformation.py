import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataTransformationConfig
from transformers import AutoTokenizer
from datasets import load_from_disk, load_dataset



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)

    
    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'] , max_length = 1024, truncation = True )

        
        target_encodings = self.tokenizer(example_batch['summary'], max_length = 128, truncation=True)

        encodings = {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

        return encodings
    
    def convert(self):
        dataset_samsum = load_from_disk(self.config.transformed_train_file)
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir, "samsum_dataset"))


