import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import yaml

# Load API key from config file
def load_api_key():
    try:
        # ✅ Streamlit Cloud: use secrets
        import streamlit as st
        if "news_api_key" in st.secrets:
            return st.secrets["news_api_key"]
    except ImportError:
        pass  # Streamlit not installed or running outside Streamlit

    # ✅ GitHub Actions or CLI: use environment variable
    import os
    if "news_api_key" in os.environ:
        return os.environ["news_api_key"]

    # ✅ Local dev: load from config/config.yaml
    import yaml
    config_path = "config/config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            return config.get("news_api_key")

    raise RuntimeError("news_api_key not found in Streamlit secrets, environment, or config.yaml")


# def load_api_key():
#     return st.secrets["news_api_key"]

def fetch_latest_news(query: str = "artificial intelligence OR AI OR ML OR machine learning OR Large Language Models OR Generative AI OR Data Science OR Agentic AI OR MCP", max_results: int = 10) -> List[Dict]:
    """
    Fetches the latest news articles using NewsAPI.

    Args:
        query (str): The keyword(s) to search for.
        max_results (int): Number of articles to retrieve.

    Returns:
        List[Dict]: A list of article dictionaries.
    """
    api_key = load_api_key()
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",  # or 'relevancy', 'popularity'
        "pageSize": max_results,
        "from": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
        "to": datetime.now().strftime('%Y-%m-%d'),
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        logging.info(f"Fetched {len(articles)} news articles.")
        return [
            {
                "title": a["title"],
                "url": a["url"],
                "source": a["source"]["name"],
                "published_at": a["publishedAt"],
                "description": a["description"],
                "content": a.get("content") or a.get("description"),
            }
            for a in articles
        ]
    except Exception as e:
        logging.error(f"Failed to fetch news: {e}")
        return []
