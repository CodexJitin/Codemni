# 📚 Wikipedia Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)

A powerful Wikipedia integration tool for Codemni agents that enables AI agents to search, retrieve, and analyze Wikipedia content programmatically.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Available Methods](#available-methods)
- [Integration with Agents](#integration-with-agents)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Use Cases](#use-cases)
- [Troubleshooting](#troubleshooting)
- [Author](#author)
- [License](#license)

## Overview

The `WikipediaTool` provides seamless integration between Codemni AI agents and Wikipedia's vast knowledge base. It enables agents to:

- Search for Wikipedia articles
- Retrieve article summaries
- Access full article content
- Get detailed page information
- Perform quick lookups with automatic disambiguation

This tool automatically handles common Wikipedia API challenges like disambiguation pages, page suggestions, and error recovery, making it reliable for production use.

## Key Features

### 1. **Intelligent Search**
- Search Wikipedia with natural language queries
- Configurable result limits
- Automatic error handling

### 2. **Flexible Content Retrieval**
- Get concise summaries (configurable sentence count)
- Retrieve full article content
- Access page metadata (URL, categories, links)

### 3. **Quick Lookup**
- One-call convenience method
- Automatic disambiguation handling
- Smart fallback to search if direct lookup fails

### 4. **Multi-Language Support**
- Support for all Wikipedia language editions
- Easy language switching
- Configurable at initialization

### 5. **Agent Integration**
- One-line integration with Codemni agents
- Automatic tool registration
- Pre-configured tool descriptions

### 6. **Robust Error Handling**
- Handles disambiguation pages gracefully
- Manages page not found errors
- Provides helpful error messages

## Installation

### Prerequisites

- Python 3.8 or higher
- Codemni framework installed
- Wikipedia Python package

### Install via PyPI

```bash
pip install Codemni
pip install wikipedia
```

> **Note:** The `wikipedia` package is required for this tool to function. Install it separately if not already installed.

## Quick Start

### Standalone Usage

```python
from Codemni.Prebuild_Tools import WikipediaTool

# Create Wikipedia tool instance
wiki = WikipediaTool()

# Quick lookup (easiest method)
result = wiki.quick_lookup("Artificial Intelligence")
print(result)

# Search for articles
search_results = wiki.search("Machine Learning")
print(search_results)

# Get a summary
summary = wiki.get_summary("Neural Network", sentences=3)
print(summary)
```

### Integration with Agent (Recommended)

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-exp",
    api_key="YOUR_API_KEY_HERE"
)

# Create agent
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add Wikipedia tools to agent
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Use the agent with Wikipedia capabilities
response = agent.invoke("Tell me about quantum computing")
print(response)
```

## Usage Examples

### Example 1: Basic Wikipedia Search

```python
from Codemni.Prebuild_Tools import WikipediaTool

# Create tool
wiki = WikipediaTool()

# Search for topics
results = wiki.search("Python programming", results=5)
print("Search Results:")
for i, title in enumerate(results, 1):
    print(f"{i}. {title}")

# Output:
# Search Results:
# 1. Python (programming language)
# 2. History of Python
# 3. Python Software Foundation
# 4. Python Package Index
# 5. CPython
```

### Example 2: Get Article Summary

```python
from Codemni.Prebuild_Tools import WikipediaTool

wiki = WikipediaTool()

# Get a brief summary (3 sentences)
summary = wiki.get_summary("Machine Learning", sentences=3)
print(summary)

# Get a longer summary (5 sentences)
detailed_summary = wiki.get_summary("Deep Learning", sentences=5)
print(detailed_summary)
```

### Example 3: Retrieve Full Article Content

```python
from Codemni.Prebuild_Tools import WikipediaTool

wiki = WikipediaTool()

# Get full article content
content = wiki.get_page_content("Artificial Intelligence")
print(f"Article length: {len(content)} characters")
print(content[:500])  # Print first 500 characters
```

### Example 4: Get Detailed Page Information

```python
from Codemni.Prebuild_Tools import WikipediaTool

wiki = WikipediaTool()

# Get comprehensive page info
info = wiki.get_page_info("Neural Network")

print(f"Title: {info['title']}")
print(f"URL: {info['url']}")
print(f"Categories: {info['categories'][:5]}")
print(f"Related Links: {info['links'][:5]}")
print(f"Number of References: {info['references']}")
```

### Example 5: Quick Lookup (Most Convenient)

```python
from Codemni.Prebuild_Tools import WikipediaTool

wiki = WikipediaTool()

# One-call lookup with automatic handling
result = wiki.quick_lookup("Albert Einstein")
print(result)

# Handles ambiguous queries automatically
result = wiki.quick_lookup("Python")  # Could be snake or programming language
print(result)
```

### Example 6: Multi-Language Support

```python
from Codemni.Prebuild_Tools import WikipediaTool

# Create tool for Spanish Wikipedia
wiki_es = WikipediaTool(language="es")
summary_es = wiki_es.get_summary("Inteligencia Artificial", sentences=3)
print(summary_es)

# Create tool for French Wikipedia
wiki_fr = WikipediaTool(language="fr")
summary_fr = wiki_fr.get_summary("Intelligence artificielle", sentences=3)
print(summary_fr)
```

### Example 7: Complete Agent Integration

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import OpenAILLM
from Codemni.memory import ConversationalBufferMemory
from Codemni.Prebuild_Tools import WikipediaTool

# Initialize components
llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
memory = ConversationalBufferMemory()

# Create agent with memory
agent = Create_ToolCalling_Agent(
    llm=llm,
    verbose=True,
    memory=memory
)

# Add Wikipedia capabilities
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Multi-turn conversation with Wikipedia
response1 = agent.invoke("Who was Alan Turing?")
print(response1)

response2 = agent.invoke("What were his contributions to computing?")
print(response2)

response3 = agent.invoke("Tell me more about the Turing Test")
print(response3)
```

### Example 8: Using with Deep Reasoning Agent

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-thinking-exp-1219",
    api_key="YOUR_API_KEY"
)

# Create deep reasoning agent
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True
)

# Add Wikipedia tools
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Ask complex question requiring research
response = agent.invoke(
    "Compare the approaches to artificial intelligence "
    "between symbolic AI and connectionism"
)
print(response)
```

## Available Methods

### `__init__(language: str = "en")`
Initialize the Wikipedia tool.

**Parameters:**
- `language` (str): Wikipedia language code (default: "en" for English)

**Example:**
```python
wiki = WikipediaTool(language="en")
```

---

### `search(query: str, results: int = 10) -> list`
Search Wikipedia for articles matching the query.

**Parameters:**
- `query` (str): Search query string
- `results` (int): Maximum number of results to return (default: 10)

**Returns:**
- List of article titles matching the query

**Example:**
```python
titles = wiki.search("quantum computing", results=5)
```

---

### `get_summary(title: str, sentences: int = 3) -> str`
Get a summary of a Wikipedia article.

**Parameters:**
- `title` (str): Title of the Wikipedia article
- `sentences` (int): Number of sentences to include (default: 3)

**Returns:**
- Summary text of the article

**Example:**
```python
summary = wiki.get_summary("Machine Learning", sentences=5)
```

---

### `get_page_content(title: str) -> str`
Get the full content of a Wikipedia article.

**Parameters:**
- `title` (str): Title of the Wikipedia article

**Returns:**
- Full text content of the article

**Example:**
```python
content = wiki.get_page_content("Neural Network")
```

---

### `get_page_info(title: str) -> Dict[str, Any]`
Get detailed information about a Wikipedia article.

**Parameters:**
- `title` (str): Title of the Wikipedia article

**Returns:**
- Dictionary containing page information:
  - `title`: Article title
  - `url`: Wikipedia URL
  - `summary`: Article summary
  - `categories`: List of categories
  - `links`: Related page links (first 20)
  - `references`: Number of references

**Example:**
```python
info = wiki.get_page_info("Deep Learning")
print(info['url'])
```

---

### `quick_lookup(query: str) -> str`
Quick lookup that searches and returns a summary in one call.

**Parameters:**
- `query` (str): Search query or article title

**Returns:**
- Summary of the most relevant article

**Example:**
```python
result = wiki.quick_lookup("Albert Einstein")
```

---

### `add_to_agent(agent) -> None`
Add all Wikipedia tools to a Codemni agent.

**Parameters:**
- `agent`: A Codemni agent instance (ToolCallingAgent, etc.)

**Example:**
```python
wiki.add_to_agent(agent)
```

This method automatically registers five tools with the agent:
- `wikipedia_search`: Search for articles
- `wikipedia_summary`: Get article summaries
- `wikipedia_content`: Get full article content
- `wikipedia_info`: Get detailed page information
- `wikipedia_quick_lookup`: Quick one-call lookup

## Integration with Agents

### Automatic Tool Registration

When you call `add_to_agent()`, the following tools are automatically registered:

| Tool Name | Description | Use Case |
|-----------|-------------|----------|
| `wikipedia_search` | Search for articles | Finding relevant topics |
| `wikipedia_summary` | Get concise summaries | Quick information retrieval |
| `wikipedia_content` | Get full article text | Detailed research |
| `wikipedia_info` | Get page metadata | Comprehensive information |
| `wikipedia_quick_lookup` | One-call convenience | General queries |

### Agent Decision Making

Agents will automatically select the appropriate Wikipedia tool based on the user's query:

```python
# User: "Search for articles about AI"
# Agent uses: wikipedia_search

# User: "Tell me about machine learning"
# Agent uses: wikipedia_quick_lookup or wikipedia_summary

# User: "I need detailed information about neural networks"
# Agent uses: wikipedia_content

# User: "What categories does the AI article belong to?"
# Agent uses: wikipedia_info
```

## Configuration

### Language Configuration

Set the Wikipedia language at initialization:

```python
# English (default)
wiki_en = WikipediaTool(language="en")

# Spanish
wiki_es = WikipediaTool(language="es")

# French
wiki_fr = WikipediaTool(language="fr")

# German
wiki_de = WikipediaTool(language="de")

# Japanese
wiki_jp = WikipediaTool(language="ja")
```

### Result Limits

Configure the number of search results:

```python
# Default: 10 results
results = wiki.search("AI")

# Custom: 5 results
results = wiki.search("AI", results=5)

# Maximum results (25)
results = wiki.search("AI", results=25)
```

### Summary Length

Control the length of summaries:

```python
# Brief (3 sentences)
brief = wiki.get_summary("AI", sentences=3)

# Medium (5 sentences)
medium = wiki.get_summary("AI", sentences=5)

# Detailed (10 sentences)
detailed = wiki.get_summary("AI", sentences=10)
```

## Best Practices

### 1. **Use Quick Lookup for General Queries**

```python
# ✅ Good: Simple and efficient
result = wiki.quick_lookup("Machine Learning")

# ❌ Less efficient: Multiple calls
results = wiki.search("Machine Learning")
summary = wiki.get_summary(results[0])
```

### 2. **Handle Disambiguation Gracefully**

```python
# Quick lookup automatically handles disambiguation
result = wiki.quick_lookup("Python")  # Auto-handles ambiguity

# Or handle manually with search
results = wiki.search("Python programming language")
summary = wiki.get_summary(results[0])
```

### 3. **Use Appropriate Content Depth**

```python
# For quick facts: use summary
summary = wiki.get_summary("AI", sentences=3)

# For research: use full content
content = wiki.get_page_content("AI")

# For metadata: use page info
info = wiki.get_page_info("AI")
```

### 4. **Combine with Agent Memory**

```python
from Codemni.memory import ConversationalBufferMemory

memory = ConversationalBufferMemory()
agent = Create_ToolCalling_Agent(llm=llm, memory=memory)
wiki.add_to_agent(agent)

# Agent can now reference previous Wikipedia lookups
```

### 5. **Limit Search Results**

```python
# Don't request too many results
results = wiki.search("AI", results=5)  # ✅ Good

# Avoid excessive results
results = wiki.search("AI", results=100)  # ❌ Unnecessary
```

### 6. **Use Specific Article Titles**

```python
# ✅ Specific
summary = wiki.get_summary("Python (programming language)")

# ❌ Ambiguous (may return wrong article)
summary = wiki.get_summary("Python")
```

## Error Handling

The Wikipedia tool includes robust error handling:

### Disambiguation Errors

When multiple articles match a query:

```python
result = wiki.get_summary("Mercury")
# Returns: "Multiple articles found. Options include: 
#          Mercury (planet), Mercury (element), Mercury (mythology), ..."
```

### Page Not Found

When an article doesn't exist:

```python
result = wiki.get_summary("NonexistentArticle12345")
# Returns: "No Wikipedia page found for 'NonexistentArticle12345'. 
#          Try searching first."
```

### General Errors

All methods include exception handling:

```python
try:
    result = wiki.quick_lookup("Your Query")
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

## Use Cases

### 1. **Research Assistant**

```python
agent = Create_ToolCalling_Agent(llm=llm)
wiki.add_to_agent(agent)

response = agent.invoke(
    "Research the history of artificial intelligence and "
    "summarize the key milestones"
)
```

### 2. **Educational Chatbot**

```python
agent = Create_ToolCalling_Agent(llm=llm, memory=memory)
wiki.add_to_agent(agent)

# Student asks questions
response = agent.invoke("Explain how neural networks work")
```

### 3. **Fact-Checking System**

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm)
wiki.add_to_agent(agent)

response = agent.invoke(
    "Verify: Was Alan Turing born in 1912? "
    "Check Wikipedia and report the facts"
)
```

### 4. **Content Generation**

```python
agent = Create_ToolCalling_Agent(llm=llm)
wiki.add_to_agent(agent)

response = agent.invoke(
    "Write a brief article about quantum computing based on "
    "Wikipedia information"
)
```

### 5. **Multi-Topic Analysis**

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm)
wiki.add_to_agent(agent)

response = agent.invoke(
    "Compare and contrast supervised learning and "
    "unsupervised learning using Wikipedia as a reference"
)
```

## Troubleshooting

### Issue: "No module named 'wikipedia'"

**Solution:**
```bash
pip install wikipedia
```

### Issue: Disambiguation errors

**Solution:**
Use more specific article titles or use `quick_lookup()` which handles disambiguation automatically:

```python
# Instead of:
wiki.get_summary("Mercury")

# Use:
wiki.quick_lookup("Mercury planet")
# or
wiki.get_summary("Mercury (planet)")
```

### Issue: Connection timeout

**Solution:**
Check your internet connection. Wikipedia API requires active internet access.

### Issue: Rate limiting

**Solution:**
Wikipedia's API has rate limits. Avoid making hundreds of requests in quick succession. Add delays if needed:

```python
import time
results = wiki.search("topic1")
time.sleep(1)
results = wiki.search("topic2")
```

### Issue: Wrong language results

**Solution:**
Ensure you've set the correct language at initialization:

```python
wiki = WikipediaTool(language="en")  # English
```

### Issue: Agent not using Wikipedia tools

**Solution:**
Ensure you've called `add_to_agent()` and that your agent query is clear:

```python
wiki.add_to_agent(agent)

# Clear query
response = agent.invoke("Search Wikipedia for information about AI")
```

## API Reference

### Factory Function

```python
def create_wikipedia_tool(language: str = "en") -> WikipediaTool
```

Convenience function to create a WikipediaTool instance.

**Example:**
```python
from Codemni.Prebuild_Tools import create_wikipedia_tool

wiki = create_wikipedia_tool(language="en")
result = wiki.quick_lookup("Artificial Intelligence")
```

## Advanced Usage

### Custom Tool Descriptions

You can manually register tools with custom descriptions:

```python
agent = Create_ToolCalling_Agent(llm=llm)
wiki = WikipediaTool()

# Add only specific tools
agent.add_tool(
    name="wiki_search",
    description="Search Wikipedia for articles about any topic",
    function=wiki.search
)

agent.add_tool(
    name="wiki_quick",
    description="Get Wikipedia summary quickly",
    function=wiki.quick_lookup
)
```

### Filtering Search Results

```python
wiki = WikipediaTool()

# Get search results
results = wiki.search("Python programming", results=10)

# Filter for specific keywords
python_results = [r for r in results if "programming" in r.lower()]
print(python_results)
```

### Batch Processing

```python
wiki = WikipediaTool()

topics = ["Machine Learning", "Deep Learning", "Neural Networks"]
summaries = {}

for topic in topics:
    summaries[topic] = wiki.get_summary(topic, sentences=2)

for topic, summary in summaries.items():
    print(f"\n{topic}:")
    print(summary)
```

## Performance Considerations

- **Network Latency**: Wikipedia API calls require internet access; response times vary
- **Content Size**: Full article content can be large (10KB-100KB+)
- **Rate Limits**: Wikipedia has API rate limits; avoid excessive rapid requests
- **Caching**: Consider caching results for frequently accessed articles
- **Language**: Different language editions may have varying content completeness

## Contributing

Contributions are welcome! Please check the main [Codemni repository](https://github.com/CodexJitin/Codemni) for contribution guidelines.

## Author

**CodexJitin**
- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- LinkedIn: [CodexJitin](https://www.linkedin.com/in/codexjitin)
- Email: codexjitin@gmail.com

## License

This project is licensed under a Proprietary License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by [CodexJitin](https://github.com/CodexJitin)

</div>
