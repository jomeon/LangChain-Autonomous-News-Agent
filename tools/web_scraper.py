import asyncio
from langchain_core.tools import tool
from crawl4ai import AsyncWebCrawler

@tool
def scrape_article_content(url: str) -> str:
    """
    Crawls a website URL and extracts the main text content in Markdown format.
    Use this tool as a SECOND step after 'search_news' to read the full body 
    of the most relevant article URLs before summarizing.
    
    Args:
        url (str): The valid HTTP or HTTPS URL of the article to scrape.
        
    Returns:
        str: The full text of the article in markdown, or an error message if the site is unreachable.
    """
    async def run_crawler():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            if not result.success:
                return f"Error: Could not scrape the site. Reason: {result.error_message}"
            if hasattr(result, 'markdown') and hasattr(result.markdown, 'fit_markdown'):
                    return result.markdown.fit_markdown
            return result.markdown

    try:
        return asyncio.run(run_crawler())
    except Exception as e:
        return f"Error: An unexpected error occurred while scraping: {str(e)}"