import os
import requests
from langchain_core.tools import tool
import json

@tool
def search_news(topic: str) -> str:
    """
    Queries the NewsAPI v2 everything endpoint to retrieve the latest articles on a specific topic.
    Use this tool whenever you need to find recent news, events, or updates about a given subject.
    
    Args:
        topic (str): The search phrase or keywords to query (e.g., 'artificial intelligence', 'quantum computing').
        
    Returns:
        list: A list of dictionaries, where each dictionary represents an article containing 
              'title', 'description', 'url', and 'publishedAt'. Returns an empty list or an error 
              message dictionary if the request fails.
    """
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        return [{"error": "NEWSAPI_API_KEY environment variable is missing. Alert the user to configure it."}]
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "pageSize": 5,  
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt" 
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return [{"error": f"NewsAPI returned status code {response.status_code}: {response.text}"}]
            
        data = response.json()
        articles = data.get("articles", [])
        
        cleaned_articles = []
        for art in articles:
           
            title = art.get("title") or "No Title"
            description = art.get("description") or "No Content Provided"
            url_link = art.get("url") or "No URL"
            pub_date = art.get("publishedAt") or "No Date"
            
            cleaned_articles.append({
                "title": title[:100],
                "description": description[:200],
                "url": url_link,
                "publishedAt": pub_date
            })

        return json.dumps(cleaned_articles, ensure_ascii=False)
            


    except Exception as e:
        return json.dumps([{"error": f"Failed to connect to NewsAPI: {str(e)}"}])