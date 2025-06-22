import json

import streamlit as st
import sqlite3
from pathlib import Path

DB_PATH = "data/news_papers.db"

def load_data(content_type: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if content_type == "news":
        cursor.execute("SELECT title, url, source, published_at, summary, diagram, score FROM news ORDER BY score DESC LIMIT 10")
    elif content_type == "papers":
        cursor.execute("SELECT title, link, arxiv_id, published, authors, summary, diagram, insights, score FROM papers ORDER BY score DESC LIMIT 10")
    else:
        return []

    rows = cursor.fetchall()
    conn.close()
    return rows

def display_news():
    st.subheader("📰 Top News Articles")
    articles = load_data("news")

    for title, url, source, published, summary, diagram, score in articles:
        st.markdown(f"### [{title}]({url})")
        st.caption(f"**Source:** {source} | **Published:** {published} | **Score:** {score:.2f}")
        st.write(summary)
        if diagram:
            st.markdown(diagram)
        st.markdown("---")

def display_papers():
    st.subheader("📄 Top Research Papers")
    papers = load_data("papers")

    for title, link, arxiv_id, published, authors, summary, diagram, insights_str, score in papers:
        with st.expander(f"📘 {title}"):
            st.markdown(f"[🔗 View Full Paper]({link})", unsafe_allow_html=True)
            st.caption(f"**Authors:** {authors} | **Published:** {published} | **Score:** {score:.2f}")

            st.markdown("### 📝 Summary")
            st.write(summary)

            try:
                insights = json.loads(insights_str) if isinstance(insights_str, str) else {}
                if insights:
                    st.markdown("### 🔍 Extracted Research Insights")
                    for key, value in insights.items():
                        st.markdown(f"- **{key}:** {value}")
                else:
                    st.info("No insights available.")
            except Exception:
                st.warning("Could not parse insights.")

            if diagram:
                st.markdown("### 📊 Architecture Diagram")
                st.markdown(diagram)

            st.markdown("---")
def main():
    st.set_page_config(page_title="AI/ML News & Research Dashboard", layout="wide")
    st.title("🧠 AI & ML News + Research Paper Summarizer")
    st.markdown("Explore the most relevant and recent updates in AI/ML from top news and research sources.")

    tab1, tab2 = st.tabs(["📰 News", "📄 Research Papers"])
    with tab1:
        display_news()
    with tab2:
        display_papers()

if __name__ == "__main__":
    main()
