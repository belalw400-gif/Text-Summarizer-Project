# Text Summarizer Project

This repository contains a modular text summarization pipeline and a small demo app. The project demonstrates data ingestion, validation, transformation, model training, evaluation, and a Streamlit demo for generating abstractive summaries.

Key points:
- Modular Python package located in `src/textSummarizer`.
- Working with the SAMSum conversation summarization dataset (stored under `artifacts/data_ingestion/samsum_dataset`).
- Pipeline stages implemented as standalone components for easy reuse and testing.

Features
--------
- Data ingestion and validation
- Text transformation and preprocessing
- Model training and evaluation
- Streamlit demo app for quick experimentation

Quick start
-----------
1. Create a Python environment (recommended Python 3.8+):

	pip install -r requirements.txt

2. To run the Streamlit demo:

	streamlit run streamlit_app.py

3. Pipeline entry points:

- `main.py` — orchestration entry for running pipeline stages
- `app.py` — alternative CLI-style runner

Project structure
-----------------
- `src/textSummarizer/` — main package with components and pipeline stages
- `artifacts/` — data artifacts, ingested datasets, and outputs
- `research/` — notebooks used during development
- `streamlit_app.py` — lightweight demo UI

Data
----
The SAMSum dataset is present under `artifacts/data_ingestion/samsum_dataset` with `train`, `validation`, and `test` splits.

Contributing
------------
Contributions and issues are welcome. Open a PR with a clear description of changes and tests where applicable.

License
-------
See the `LICENSE` file for licensing details.
