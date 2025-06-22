from datetime import datetime
from typing import List, Dict
import logging
import heapq

def compute_recency_score(published_at: str, date_format: str = "%Y-%m-%dT%H:%M:%SZ") -> float:
    """
    Computes a recency score based on how recently the item was published.

    Args:
        published_at (str): Date in ISO 8601 format.
        date_format (str): Format to parse date string.

    Returns:
        float: Recency score between 0 and 1 (1 = most recent).
    """
    try:
        pub_date = datetime.strptime(published_at, date_format)
        days_diff = (datetime.utcnow() - pub_date).days
        return max(0, 1 - (days_diff / 30))  # decay over ~1 month
    except Exception as e:
        logging.warning(f"Failed to parse date '{published_at}': {e}")
        return 0.0

def compute_final_score(item: Dict, weights: Dict[str, float]) -> float:
    """
    Combine recency and relevance to compute final score.

    Args:
        item (Dict): Item with 'published_at' and optional 'relevance_score'
        weights (Dict): Weights for each component

    Returns:
        float: Final score
    """
    recency = compute_recency_score(item.get("published_at", ""))
    relevance = item.get("relevance_score", 0.5)  # default neutral relevance

    score = weights["recency"] * recency + weights["relevance"] * relevance
    item["score"] = score
    return score

def rank_items(items: List[Dict], top_k: int = 5, weights: Dict[str, float] = {"recency": 0.5, "relevance": 0.5}) -> List[Dict]:
    """
    Rank items by final score and return the top K.

    Args:
        items (List[Dict]): List of news or papers
        top_k (int): Number of top items to return
        weights (Dict[str, float]): Weights for scoring

    Returns:
        List[Dict]: Top K scored and ranked items
    """
    try:
        for item in items:
            compute_final_score(item, weights)

        top_items = heapq.nlargest(top_k, items, key=lambda x: x["score"])
        logging.info(f"Ranked and selected top {top_k} items.")
        return top_items

    except Exception as e:
        logging.error(f"Failed to rank items: {e}")
        return items[:top_k]
