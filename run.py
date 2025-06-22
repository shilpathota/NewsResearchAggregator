# run.py

import logging
from src.collectors.news_collector import fetch_latest_news
from src.collectors.paper_collector import fetch_latest_papers
from src.processors.cleaner import clean_and_deduplicate
from src.processors.summarizer import summarize_content, extract_insights_with_flan
from src.ranking.ranker import rank_items
from src.storage.database import save_to_db
from src.processors.diagram_generator import generate_mermaid_diagram


# Optional: streamlit or flask can be triggered here or elsewhere
# from src.ui.dashboard import launch_dashboard

def main():
    logging.basicConfig(
        filename='logs/pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Pipeline started.")

    try:
        # Step 1: Collect content
        news = fetch_latest_news()
        papers = fetch_latest_papers()

        # Step 2: Preprocess
        cleaned_news = clean_and_deduplicate(news)
        cleaned_papers = clean_and_deduplicate(papers)

        # Step 3: Summarize
        summarized_news = summarize_content(cleaned_news, content_type="news")
        summarized_papers = summarize_content(cleaned_papers, content_type="paper")


        for paper in summarized_papers:
            generate_mermaid_diagram(paper)
                # After summarizing papers
        for paper in summarized_papers:
            insights = extract_insights_with_flan(paper["summary"])
            logging.info(insights)
            paper["insights"] = insights
        # Step 4: Rank
        top_news = rank_items(summarized_news, top_k=5)
        top_papers = rank_items(summarized_papers, top_k=5)

        # Step 5: Store
        save_to_db("news", top_news)
        save_to_db("papers", top_papers)

        # (Optional Step) Serve or display results
        # launch_dashboard()

        logging.info("Pipeline completed successfully.")

    except Exception as e:
        logging.exception("Pipeline failed: %s", str(e))

if __name__ == "__main__":
    main()
