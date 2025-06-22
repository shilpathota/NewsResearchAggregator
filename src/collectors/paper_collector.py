# src/collectors/paper_collector.py

import feedparser
import logging
from typing import List, Dict

def fetch_latest_papers(
        query: str = "all:(generative AI OR large language models OR LLM OR foundation models OR multimodal OR diffusion OR image-to-text OR vision-language OR multi-modal)",
        max_results: int = 10
) -> List[Dict]:
    """
    Fetches the latest AI/ML papers from arXiv using the arXiv RSS/Atom API.

    Args:
        query (str): Search query in arXiv format (default: machine learning categories).
        max_results (int): Number of papers to fetch.

    Returns:
        List[Dict]: List of parsed paper metadata.
    """
    base_url = "http://export.arxiv.org/api/query?"
    url = f"{base_url}search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

    try:
        feed = feedparser.parse(url)
        entries = feed.entries
        papers = []

        for entry in entries:
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "summary": entry.summary,
                "published": entry.published,
                "link": entry.link,
                "arxiv_id": entry.id.split('/')[-1],
                "categories": entry.tags if "tags" in entry else [],
            }
            papers.append(paper)

        logging.info(f"Fetched {len(papers)} papers from arXiv.")
        return papers

    except Exception as e:
        logging.error(f"Failed to fetch arXiv papers: {e}")
        return []
