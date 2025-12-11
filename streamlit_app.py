import streamlit as st
import requests
import json
from pygooglenews import GoogleNews
import time # Needed for adding a slight delay for better user experience

# --- CONFIGURATION (Non-Streamlit functions remain the same) ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"
# -------------------------------------------------------------

# --- CACHED DATA FUNCTIONS (For Performance) ---

@st.cache_data(ttl=3600)  # Cache results for 1 hour (3600 seconds)
def fetch_category_news(category, count=5):
    """Fetches India-specific news using the RSS summary snippet."""
    st.info(f"Fetching NEW data for '{category}' (Cached for 1 hour)...")
    
    gn = GoogleNews(lang='en', country='IN') 
    search = gn.search(category)
    
    articles = []
    for entry in search.get('entries', [])[:count]:
        rss_summary = entry.get('summary')
        
        if rss_summary and len(rss_summary) > 50:
            articles.append({
                "title": entry.title,
                "text": rss_summary,
                "url": entry.link
            })
        
    return articles

@st.cache_resource(ttl=3600) # Cache the costly Ollama API call results
def summarize_with_ollama(text):
    """Sends text to local Ollama instance for summarization."""
    
    # 🌟 UPDATED PROMPT: Requesting 5 bullet points and strict adherence to format
    prompt = f"""
You are a concise summarizer. Your only task is to analyze the text provided below.
Strictly adhere to the following output rules:
1. Generate exactly 5 bullet points.
2. The output must contain ONLY the bullet points, no introductory phrases (e.g., "Here are five points," "Based on the text," "I can summarize this") or closing remarks.
3. Use a standard asterisk (*) for each bullet point.

Text to summarize:
---
{text}
---
"""
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        # Add a slight delay for better user perception of the AI working
        time.sleep(0.5) 
        
        return response.json().get("response", "Ollama failed to generate a summary.")
    except Exception as e:
        if 'ConnectionRefusedError' in str(e):
             return "Ollama Error: Ollama is not running. Please ensure the Ollama app is open."
        return f"Ollama Error: {e}"

# --- STREAMLIT APP LAYOUT ---

def main():
    st.set_page_config(page_title="Indian Sports News Summarizer", layout="centered")
    
    # 1. Title and Header
    st.title("🇮🇳 Daily Indian News Summarizer")
    st.markdown("---")
    
    # 2. User Input (Text box and Button)
    user_input = st.text_input(
        "Enter the specific news topic you want summarized (e.g., 'IPL updates', 'cricket match results', 'Badminton Asia')",
        placeholder="cricket match results"
    )
    
    # 3. Process Button
    if st.button("Get Summaries"):
        if not user_input:
            st.error("Please enter a news topic to search.")
            return

        with st.spinner(f"Searching and summarizing {user_input} with Ollama..."):
            
            # Fetch news data
            news_items = fetch_category_news(user_input)
            
            if not news_items:
                st.warning(f"No recent news found for '{user_input}' in India. Try a different keyword.")
                return

            st.header(f"Top Summaries for: {user_input.upper()}")
            st.markdown("---")

            # 4. Display Results
            for i, item in enumerate(news_items, 1):
                # Summarize the content
                summary = summarize_with_ollama(item['text'])
                
                # Use Streamlit's expander for clean layout
                with st.expander(f"**{i}. {item['title']}**"):
                    st.markdown(summary)
                    st.caption(f"[Read full article here]({item['url']})")
                    
        st.success("Summarization Complete!")

if __name__ == "__main__":
    main()