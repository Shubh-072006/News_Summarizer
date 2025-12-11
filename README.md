# 📰 Ollama-Powered Indian News Summarizer (Streamlit App)

## Project Overview
This project is a powerful, real-time news summarization web application built with Streamlit and powered by a local Large Language Model (LLM) using Ollama. 

It fetches the top 5 most recent headlines related to a specific user query (e.g., 'IPL updates') from Indian news sources, and then uses the local LLM to generate a clean, five-sentence narrative summary for each article.

---

## ✨ Key Features

* **Local LLM Integration:** Uses the local Ollama instance (`llama3.2:3b`) for cost-effective and private summarization.
* **Targeted News:** Specifically searches for news relevant to **India** (`country='IN'`).
* **Dynamic Summaries:** Generates exactly 5 unique news items, each summarized into a cohesive 5-sentence paragraph using advanced prompt engineering.
* **Performance Caching:** Utilizes Streamlit's built-in caching to prevent unnecessary repeat calls to the Google News API and Ollama, dramatically improving user experience and speed.
* **Web Interface:** Hosted via a simple, interactive Streamlit application.

---

## 💻 Setup and Installation

### Prerequisites

1.  **Python 3.8+**
2.  **Ollama:** The Ollama application must be downloaded and running locally on your machine.
3.  **LLM Model:** Ensure the required model is pulled:
    ```bash
    ollama pull llama3.2:3b
    ```

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Shubh-072006/News_Summarizer.git
    ```
2.  **Install Dependencies:**
    Create the `requirements.txt` file (see section B), then install the libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App:**
    Start the Streamlit web server:
    ```bash
    streamlit run streamlit_app.py
    ```
    The application will automatically open in your web browser (usually at `http://localhost:8501`).

---

## ⚙️ Configuration

The core configuration is located at the top of `streamlit_app.py`:

| Variable | Description | Default Value |
| :--- | :--- | :--- |
| `OLLAMA_API_URL` | The endpoint for your local Ollama server. | `http://localhost:11434/api/generate` |
| `OLLAMA_MODEL` | The LLM model used for summarization. | `llama3.2:3b` |

---

## 📄 File Structure
