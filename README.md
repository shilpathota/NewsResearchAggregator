# 🧠 AI & ML News + Paper Summarizer

A research aggregation pipeline and interactive dashboard that automatically fetches, summarizes, ranks, and visualizes the latest **AI/ML news and research papers** from top sources like **arXiv** and **NewsAPI**. It uses **Hugging Face models**, **OpenAI GPT-4**, and **Streamlit** for a rich user experience.

---

## 🚀 Features

- 🔍 Fetches recent news articles and research papers on AI/ML
- ✂️ Summarizes content using `facebook/bart-large-cnn` (HuggingFace)
- 🧠 Extracts structured insights using GPT-4:
  - Problem Statement
  - Dataset Used
  - Model Type
  - Evaluation Metrics
- 📊 Automatically generates Mermaid.js architecture diagrams
- ⭐ Ranks items based on recency and relevance
- 💾 Stores results in a SQLite database
- 📺 Visualizes everything in an interactive **Streamlit dashboard**

---

## 📂 Folder Structure

```
├── run.py                  # Pipeline entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── config.yaml         # OpenAI and News API keys
├── data/
│   └── news_papers.db      # SQLite database
├── logs/
│   └── pipeline.log        # Log output
├── src/
│   ├── collectors/
│   │   ├── news_collector.py
│   │   └── paper_collector.py
│   ├── processors/
│   │   ├── cleaner.py
│   │   ├── summarizer.py
│   │   └── diagram_generator.py
│   ├── ranking/
│   │   └── ranker.py
│   ├── storage/
│   │   └── database.py
│   └── ui/
│       └── dashboard.py    # Streamlit interface
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-ml-news-summarizer.git
cd ai-ml-news-summarizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API Keys
Create a file at `config/config.yaml`:

```yaml
news_api_key: "your-newsapi-key"
```

---

## ▶️ Run the Pipeline

This fetches, processes, and saves top news and research papers:

```bash
python run.py
```

---

## 🖥️ Launch the Dashboard

Start the interactive UI:
```bash
streamlit run src/ui/dashboard.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 🧩 Example Output (UI)

Each paper shows:
- 🔗 Title with link to arXiv
- 📝 Summary of the paper
- 🔍 Expandable insights section:
  - Problem Statement
  - Dataset Used
  - Model Type
  - Evaluation Metrics
- 📊 Mermaid diagram showing architecture flow

---

## 📈 Customization Ideas

- Add user input for keyword/topic-based search
- Enable filtering by model type (e.g., Transformer, CNN, RL)
- Extend to other domains (e.g., BioMed, Finance)
- Replace OpenAI with Llama 3 or local LLMs
- Export summaries to PDF or Markdown

---

## 🙌 Acknowledgements

- Hugging Face Transformers
- OpenAI GPT-4
- arXiv RSS API
- NewsAPI.org
- Streamlit
