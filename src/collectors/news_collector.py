# src/collectors/news_collector.py

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import os
import yaml
import streamlit as st


# Load API key from config file
# def load_api_key():
    # config_path = "config/config.yaml"
    # with open(config_path, "r") as file:
    #     config = yaml.safe_load(file)
    # return config["news_api_key"]

def load_api_key():
    return st.secrets["news_api_key"]

def fetch_latest_news(query: str = "artificial intelligence OR machine learning", max_results: int = 10) -> List[Dict]:
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
