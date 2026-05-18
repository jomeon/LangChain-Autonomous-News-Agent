# Autonomous Research Agent

This repository contains an autonomous research agent built using the LangChain and LangGraph frameworks. The system dynamically orchestrates data collection, web scraping, content synthesis, and document generation to produce comprehensive intelligence reports in PDF format. 

The project demonstrates advanced agentic workflows, including dynamic function calling, state management, and error handling (self-correction protocols) without relying on hard-coded execution paths.

## Architecture

The system operates on a ReAct (Reasoning and Acting) loop, powered by the Llama-3.1-8b-instant model via the Groq API. The agent acts on a high-level user prompt and independently plans its execution sequence using the following toolchain:

1. **News Search (`search_news`)**: Integrates with NewsAPI to fetch the latest articles and metadata based on the requested topic.
2. **Web Scraper (`scrape_article_content`)**: Utilizes `Crawl4AI` to asynchronously extract the full markdown body of the selected target URLs, bypassing generic HTML boilerplate and cookie banners.
3. **Content Evaluator (`summarize_news_content`)**: Synthesizes the raw scraped markdown into a structured executive summary using a dedicated LLM sub-chain.
4. **PDF Generator (`generate_pdf_report`)**: Evaluates the domain importance (HIGH/MEDIUM/LOW) and compiles the synthesized markdown into a formatted PDF using `fpdf2`, applying a standardized naming convention: `<date>_<topic>_<importance>.pdf`.

## Prerequisites

- Python 3.10+
- [NewsAPI Key](https://newsapi.org/)
- [Groq API Key](https://console.groq.com/keys)

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/autonomous-research-agent.git](https://github.com/yourusername/autonomous-research-agent.git)
cd autonomous-research-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright binaries (required by Crawl4AI for asynchronous web scraping):
```bash
python -m playwright install chromium
```

4. Create a `.env` file in the root directory and configure your environment variables:
```env
GROQ_API_KEY=your_groq_api_key_here
NEWSAPI_API_KEY=your_newsapi_key_here
```

## Usage

To initialize the agent and start the research protocol, execute the main script:

```bash
python main.py
```

By default, the script triggers a research pipeline on "recent breakthroughs in quantum computing". The agent will log its ReAct execution steps (Thoughts, Actions, Observations) to the standard output. 

Upon successful execution, the compiled report will be saved in the `/reports` directory.

## Project Structure

- `main.py`: The entry point establishing the LangGraph agent and the execution context.
- `prompts/system_prompt.py`: Contains the system instructions and data pipeline protocol driving the agent's behavior.
- `tools/news_search.py`: NewsAPI integration.
- `tools/web_scraper.py`: Crawl4AI integration.
- `tools/evaluator.py`: LLM-based summarization logic.
- `tools/pdf_generator.py`: PDF rendering logic.
- `reports/`: Output directory for generated PDF files.

---

## Implementation Report

### 1. AI Agent Architecture

**Data Flow Between Tools and the LLM:**
The architecture relies on a ReAct (Reasoning and Acting) loop. The LLM acts as the orchestrator. It outputs a "Thought" and an "Action" (a specific tool call with generated JSON arguments). The LangGraph execution environment intercepts this call, runs the corresponding Python function, and returns the raw output as an "Observation" back to the LLM. The LLM processes this observation to decide on the subsequent step.

**Error Handling:**
If a tool returns an error (e.g., a network timeout or a scraping block), the system does not crash. Instead, the error string is passed back to the LLM as an observation. The agent reads the error and utilizes its self-correction protocol to try an alternative approach.

**Iterative Tool Usage:**
The agent is fully capable of using tools multiple times. If the initial search yields irrelevant results, or if scraping a specific URL fails, the loop allows the agent to call the search or scrape tools repeatedly until it acquires the necessary data to proceed.

**Self-Correction Example:**
During testing, the `scrape_article_content` tool encountered a library deprecation error (`AttributeError: 'fit_markdown' is deprecated`). Instead of halting execution, the agent analyzed the error observation, realized it lacked the deep-scrape data, and autonomously attempted to generate a fallback summary to ensure the overarching goal (creating a PDF) was still met. Once the tool was patched, the agent seamlessly ingested the correct data.

### 2. Language Model

**Selected Model:** `llama-3.1-8b-instant` (via Groq API).
**Rationale:** This model was chosen for its exceptional inference speed, reliable function-calling capabilities, and robust context management. Furthermore, the Groq API provides a high rate limit, which is essential for iterative agentic workflows that require multiple rapid API calls per session, avoiding the `429 Resource Exhausted` errors encountered with other providers.

### 3. System Prompt

**Construction and Description:**
The system prompt is isolated in a dedicated configuration file (`system_prompt.py`). It establishes a strict persona ("Elite AI Research Agent") and outlines a definitive data pipeline protocol. It avoids hard-coded programmatic loops but provides a strong operational framework.

**Prompting Techniques Used:**
- **Persona Pattern:** Setting a professional context.
- **Constraint Prompting:** Using strict directives (e.g., "ANTI-CONVERSATIONAL GUARDRAIL") to prevent hallucination and enforce data integrity between steps.
- **ReAct Structure:** Explicitly mentioning the Thought -> Action -> Observation loop.

**Enabling Self-Correction:**
A dedicated "SELF-CORRECTION PROTOCOL" section explicitly instructs the model not to halt on errors. It provides contextual advice on what to do if a tool fails (e.g., select an alternative URL from the search results if the scraper returns garbage).

**Goal Definition:**
The primary objective is defined at the very beginning of the prompt: "Your main goal is to create a deeply researched intelligence report saved as a PDF." This provides the agent with a clear termination condition.

### 4. Functions (Tools)

**Implemented Tools and Their Purpose:**
1.  `search_news`: Interfaces with NewsAPI to discover current events. Used by the agent to acquire initial metadata and source URLs.
2.  `scrape_article_content`: Utilizes `Crawl4AI` to perform deep reading. The agent uses this to extract the core markdown body of a specific article, bypassing cookie banners.
3.  `summarize_news_content`: A specialized LLM chain acting as a sub-agent. The main agent passes the raw scraped data here to synthesize it into a clean, structured executive summary.
4.  `generate_pdf_report`: The terminal tool. The agent passes the final markdown, topic, and an autonomously evaluated importance level (HIGH/MEDIUM/LOW) to compile and save the physical `.pdf` file.

**Type Hinting and Docstrings:**
Strict Python type hinting (e.g., `topic: str -> str`) is enforced to maintain data schema integrity. Docstrings are heavily detailed because the LLM relies entirely on them to understand the tool's capabilities, required arguments, and expected output formats. LangChain automatically parses these docstrings into the LLM's system context.

### 5. Agent Decision Making

**Decision Process:**
The agent does not follow a hard-coded script. It receives the user's prompt and reads the available tool docstrings. Based on its current state in the ReAct loop, it generates a "Thought" (e.g., "I need source material first"). It then matches this intent with the `search_news` tool. After receiving the search results, the next "Thought" evaluates the links and selects one for the `scrape_article_content` tool. This dynamic evaluation occurs before every tool invocation.

### 6. Results and Quality Assessment

**Results:**
The system successfully outputs files formatted as `<date>_<topic>_<importance>.pdf` (e.g., `2026-05-18_recent_breakthroughs_in_quantum_computing_high.pdf`). 

**Quality Assessment:**
The quality of the final output is excellent. The integration of `Crawl4AI` with the `fit_markdown` attribute ensures that the LLM is not polluted with website navigation menus or cookie policies. The resulting PDF contains a highly relevant, logically synthesized executive summary with professional formatting, successfully demonstrating a autonomous workflow.

## License

Distributed under the MIT License.

<img width="2883" height="596" alt="image" src="https://github.com/user-attachments/assets/a957319e-dbab-4ea9-8b30-a03d52f8917a" />

<img width="3109" height="1247" alt="image" src="https://github.com/user-attachments/assets/ddbefe74-7cc7-4da0-8902-8d1f153e1415" />
