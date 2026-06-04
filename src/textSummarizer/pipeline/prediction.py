from textSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer
from transformers import pipeline



class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        # Force CPU inference in Streamlit to avoid GPU/CUDA runtime issues.
        self.pipe = pipeline(
            "summarization",
            model=self.config.model_path,
            tokenizer=self.tokenizer,
            device=-1,
        )
        self.gen_kwargs = {"length_penalty": 0.8, "num_beams": 8, "max_length": 128}





    def predict(self, text: str) -> str:
        output = self.pipe(text, **self.gen_kwargs)[0]["summary_text"]
        return output
        