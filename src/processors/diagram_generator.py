
import logging
from typing import List, Dict

def extract_flowchart_steps(summary: str) -> List[str]:
    """
    Heuristically extract architecture steps from a summary or method description.
    You can later replace this with NLP chunking or even a GPT model.

    Args:
        summary (str): Summarized text from a paper

    Returns:
        List[str]: Ordered list of architecture steps
    """
    # Simplistic approach: split by indicative connectors
    keywords = ["input", "embedding", "encoder", "decoder", "attention", "classifier", "output"]
    steps = []

    for word in keywords:
        if word in summary.lower():
            steps.append(word.title())  # capitalize for visual clarity

    # Ensure no duplicates and preserve order
    return list(dict.fromkeys(steps))


def generate_mermaid_diagram(entry: Dict) -> str:
    """
    Generates a simple Mermaid.js flowchart from paper summary.

    Args:
        entry (Dict): A paper or news item with a summary

    Returns:
        str: Mermaid diagram code block (flowchart)
    """
    try:
        summary = entry.get("summary", "")
        steps = extract_flowchart_steps(summary)

        if len(steps) < 2:
            return "%% Not enough architecture info to generate flowchart."

        # Build Mermaid code block
        diagram = ["```mermaid", "graph TD"]
        for i in range(len(steps) - 1):
            diagram.append(f"    {steps[i]} --> {steps[i+1]}")
        diagram.append("```")

        mermaid_code = "\n".join(diagram)
        entry["diagram"] = mermaid_code
        return mermaid_code

    except Exception as e:
        logging.error(f"Failed to generate diagram: {e}")
        return "%% Diagram generation failed."
