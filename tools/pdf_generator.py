import os
from datetime import datetime
from langchain_core.tools import tool
import markdown
from fpdf import FPDF

@tool
def generate_pdf_report(markdown_content: str, topic: str, importance: str) -> str:
    """
    Converts a markdown summary into an HTML structure and saves it as a polished PDF report.
    Use this tool ONLY after the news summary text has been completely generated.
    
    Args:
        markdown_content (str): The complete, well-formatted markdown text to include in the report.
        topic (str): The subject matter of the report (e.g., 'quantum_computing').
        importance (str): The calculated importance level: 'high', 'medium', or 'low'.
        
    Returns:
        str: A success message with the file path, or an error message if generation fails.
    """
    try:
       
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(' ', '_')
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_{safe_topic}_{importance.lower()}.pdf"
        
        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, filename)
        
        html_body = markdown.markdown(markdown_content, extensions=['extra'])
        
        pdf = FPDF()
        pdf.add_page()
        
        full_html = f"""
        <h1 align="center">Intelligence Report</h1>
        <p><b>Topic:</b> {topic.title()}</p>
        <p><b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><b>Evaluated Importance:</b> {importance.upper()}</p>
        <hr>
        {html_body}
        """
        
        pdf.write_html(full_html)
        pdf.output(pdf_path)
            
        return f"Success: PDF report generated successfully at absolute path: {os.path.abspath(pdf_path)}"
        
    except Exception as e:
        return f"Error during PDF generation: {str(e)}"