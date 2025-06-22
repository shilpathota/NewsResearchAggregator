# src/processors/summarizer.py

import logging
from typing import List, Dict
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# if using OpenAI
# import openai
# import yaml

# Initialize Hugging Face summarizer
hf_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    tokenizer="facebook/bart-large-cnn"
)

# Optionally load OpenAI key from config.yaml
# def load_openai_key():
#     with open("config/config.yaml", "r") as f:
#         return yaml.safe_load(f)["openai_api_key"]

def summarize_with_huggingface(text: str, max_length=33, min_length=30) -> str:
    try:
        summary = hf_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        logging.warning(f"HuggingFace summarization failed: {e}")
        return ""

# if using OpenAI
# def summarize_with_openai(text: str) -> str:
#     try:
#         openai.api_key = load_openai_key()
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are an AI summarization assistant."},
#                 {"role": "user", "content": f"Summarize this: {text}"}
#             ],
#             max_tokens=150,
#             temperature=0.3
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         logging.warning(f"OpenAI summarization failed: {e}")
#         return ""

def summarize_content(items: List[Dict], content_type="news", method="huggingface") -> List[Dict]:
    """
    Adds a 'summary' field to each item using selected summarization method.

    Args:
        items (List[Dict]): List of news or papers.
        content_type (str): 'news' or 'paper'.
        method (str): 'huggingface' or 'openai'.

    Returns:
        List[Dict]: Same list with 'summary' field added.
    """
    summarized_items = []
    for item in items:
        text = item.get("content") or item.get("summary") or item.get("description", "")
        if not text:
            item["summary"] = ""
            continue

        if method == "huggingface":
            summary = summarize_with_huggingface(text)
        # elif method == "openai":
        #     summary = summarize_with_openai(text)  # requires OpenAI key and module
        else:
            raise ValueError("Unsupported summarization method")

        item["summary"] = summary
        summarized_items.append(item)

    logging.info(f"Summarized {len(summarized_items)} items using {method}.")
    return summarized_items
from transformers import pipeline

# Load Flan-T5 model for instruction-style prompting
flan_t5 = pipeline("text2text-generation", model="google/flan-t5-base")

def extract_insights_with_flan(summary: str) -> Dict[str, str]:
    prompt = f"""
Extract key insights in JSON format:
Summary: {summary}
Return format:
{{
  "Problem Statement": "...",
  "Dataset Used": "...",
  "Model Type": "...",
  "Evaluation Metrics": "..."
}}
"""
    try:
        output = flan_t5(prompt, do_sample=False)[0]['generated_text']
        insights = eval(output) if output.startswith("{") else {}
        logging.info(f'insights  - > {insights}')
        return insights
    except Exception as e:
        logging.warning(f"Flan-T5 insights extraction failed: {e}")
        return {}