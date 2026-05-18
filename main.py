import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# NAJNOWSZY IMPORT (Zgodnie z ostrzeżeniem z Twojej konsoli):
from langchain.agents import create_agent

# Import Twoich narzędzi
from tools.news_search import search_news
from tools.web_scraper import scrape_article_content
from tools.evaluator import summarize_news_content
from tools.pdf_generator import generate_pdf_report

from prompts.system_prompt import AGENT_SYSTEM_PROMPT

load_dotenv()

def main():
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0.0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [search_news, scrape_article_content, summarize_news_content, generate_pdf_report]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=AGENT_SYSTEM_PROMPT
    )

    print("--- Launching Autonomous AI Agent (Modern LangChain Framework) ---")
    topic = "recent breakthroughs in quantum computing"
    
    try:
        response = agent.invoke({
            "messages": [("user", f"Execute your grade 5.0 research protocol for the topic: {topic}. Discover news, deep-scrape the best article content, evaluate importance, summarize the full text, and output a PDF report.")]
        })
        
        print("\n--- Autonomous Message History Trace ---")
        for i, msg in enumerate(response["messages"]):
            role = msg.__class__.__name__
            print(f"Step {i} [{role}]: {msg.content[:200]}...")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   -> Agent autonomously decided to invoke tool: {msg.tool_calls[0]['name']}")
                
    except Exception as e:
        print(f"\nCritical System Error: {e}")

if __name__ == "__main__":
    main()