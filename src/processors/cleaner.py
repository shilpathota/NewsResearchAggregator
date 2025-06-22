# src/processors/cleaner.py

import hashlib
import logging
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Basic text cleaner to remove HTML tags, extra spaces, etc.
    """
    if not text:
        return ""
    text = re.sub(r'<.*?>', '', text)             # remove HTML tags
    text = re.sub(r'\s+', ' ', text).strip()      # normalize whitespace
    return text.lower()

def generate_hash(entry: Dict) -> str:
    """
    Create a hash based on title + content to detect duplicates.
    """
    base_string = f"{entry.get('title', '')} {entry.get('content', '') or entry.get('summary', '')}"
    return hashlib.md5(base_string.encode("utf-8")).hexdigest()

def clean_and_deduplicate(entries: List[Dict]) -> List[Dict]:
    """
    Cleans and removes duplicate entries from a list of articles or papers.

    Args:
        entries (List[Dict]): Raw list of content items (news or papers).

    Returns:
        List[Dict]: Cleaned and deduplicated list.
    """
    seen_hashes = set()
    cleaned_entries = []

    for entry in entries:
        entry["title"] = clean_text(entry.get("title", ""))
        entry["content"] = clean_text(entry.get("content", "") or entry.get("summary", ""))
        entry_hash = generate_hash(entry)

        if entry_hash not in seen_hashes:
            seen_hashes.add(entry_hash)
            cleaned_entries.append(entry)
        else:
            logging.debug(f"Duplicate removed: {entry['title'][:50]}...")

    logging.info(f"{len(cleaned_entries)} items retained after cleaning and deduplication.")
    return cleaned_entries
