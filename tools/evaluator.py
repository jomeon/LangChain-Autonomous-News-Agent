import os
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

@tool
def summarize_news_content(raw_articles_text: str) -> str:
    """
    Analyzes a raw string or list of collected news articles and synthesizes them 
    into a cohesive, professional markdown summary. Use this tool after news has 
    been gathered to generate the main textual body of the intelligence report.
    
    Args:
        raw_articles_text (str): A string containing names, titles, descriptions, 
                                 or contents of gathered news articles.
                                 
    Returns:
        str: A beautifully formatted Markdown string summarizing the most significant 
             trends and events found in the data, or an error message.
    """

    if not raw_articles_text or len(raw_articles_text.strip()) < 10:
        return "Error: The provided news content is too brief or empty. Please search for valid news first."
        
    google_key = os.getenv("GROQ_API_KEY")
    if not google_key:
        return "Error: GROQ_API_KEY is missing from environment variables."

    try:
        summary_llm  = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0.0,
        api_key=os.getenv("GROQ_API_KEY")
    )
        
        # Define a strict template for the summary structure
        template = """
        You are an expert Intelligence Analyst. Review the following raw news data and synthesize it into a highly professional, structured report in Markdown format.
        
        Raw Data:
        {data}
        
        Requirements for the output:
        1. Start with a ## Executive Summary section highlighting the main trend.
        2. Break down key events into chronological or thematic sections using bold subheadings.
        3. Do not just list articles; merge overlapping information to tell a unified story.
        4. Cite sources inline if URLs are present in the raw data.
        5. Maintain an objective, academic tone.
        
        Synthesized Markdown Report:
        """
        
        prompt = PromptTemplate.from_template(template)
        chain = prompt | summary_llm
        
        response = chain.invoke({"data": raw_articles_text})
        return response.content

    except Exception as e:
        return f"Error encountered during compilation: {str(e)}"