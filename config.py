# config.py
import os

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GRANITE_MODEL_ID = "ibm-granite/granite-3.1-3b-a800m-instruct"  # your model ID

# Optional: fail fast if token isn't set
if not HUGGINGFACE_API_TOKEN:
    raise ValueError(
        "Missing Hugging Face API token. Please set the environment variable HUGGINGFACE_API_TOKEN."
    )



# PDF and generation settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_N_RESULTS = 5
MAX_NEW_TOKENS = 250
TEMPERATURE = 0.0
