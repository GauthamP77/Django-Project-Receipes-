import json
from huggingface_hub.inference_api import InferenceApi
from config import (
    HUGGINGFACE_API_TOKEN,
    GRANITE_MODEL_ID,
    MAX_NEW_TOKENS,
    TEMPERATURE
)

# Initialize API client once
inference = InferenceApi(
    repo_id=GRANITE_MODEL_ID,
    token=HUGGINGFACE_API_TOKEN
)

def get_llm_answer(query, chunks):
    """
    Generate answer from Granite model on Hugging Face using relevant context.
    """
    # Prepare context from chunks
    context_texts = [f"(Page {chunk['page']}): {chunk['text']}" for chunk in chunks]
    context_str = "\n\n".join(context_texts)

    # Build simple prompt (can be adapted to chat style)
    prompt_text = (
        f"You are an academic assistant. Based ONLY on the following context, "
        f"answer the question with references to page numbers.\n\n"
        f"CONTEXT:\n{context_str}\n\nQUESTION: {query}\n\nANSWER:"
    )

    # Prepare request payload
    api_input = {
        "inputs": prompt_text,
        "parameters": {
            "max_new_tokens": MAX_NEW_TOKENS,
            "temperature": TEMPERATURE,
            "return_full_text": True
        }
    }

    # Call HF API
    raw_response = inference(api_input, raw_response=True)
    response_text = raw_response.text

    if not response_text.strip():
        return "Error: Empty response from Hugging Face API."

    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        return f"Error: Invalid response from API. Raw: {response_text}"

    if isinstance(response_json, list) and len(response_json) > 0:
        if "error" in response_json[0]:
            return f"API Error: {response_json[0]['error']}"
        if "generated_text" in response_json[0]:
            return response_json[0]["generated_text"].split("ANSWER:")[-1].strip()

    return "Error: No valid response from Hugging Face API."
