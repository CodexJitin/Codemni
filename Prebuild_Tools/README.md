# 🛠️ Prebuild Tools

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)

Production-ready, plug-and-play tools that seamlessly integrate with Codemni agents to extend their capabilities. These tools are designed to work out-of-the-box with minimal configuration.

## Table of Contents

- [Overview](#overview)
- [Available Tools](#available-tools)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Use Cases](#use-cases)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Overview

Prebuild Tools are professionally crafted, ready-to-use tool implementations that add powerful capabilities to your Codemni agents. Instead of building tools from scratch, simply import and integrate these pre-built solutions into your agents.

### Why Use Prebuild Tools?

- ✅ **Instant Integration**: One-line setup with any Codemni agent
- ✅ **Production Ready**: Tested, optimized, and reliable
- ✅ **Robust Error Handling**: Gracefully manages edge cases
- ✅ **Well Documented**: Comprehensive guides and examples
- ✅ **Maintained**: Regular updates and improvements
- ✅ **Extensible**: Easy to customize for your needs

## Available Tools

### 📚 Wikipedia Tool

Access the world's largest encyclopedia programmatically. Enable your AI agents to search, retrieve, and analyze Wikipedia content.

**Key Features:**
- Search Wikipedia articles with natural language queries
- Retrieve article summaries (configurable length)
- Access full article content
- Get detailed page metadata (categories, links, references)
- Quick lookup with automatic disambiguation
- Multi-language support (200+ languages)

**Perfect For:**
- Research assistants
- Educational chatbots
- Fact-checking systems
- Content generation
- Knowledge retrieval applications

**Quick Example:**
```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

# Setup
llm = GoogleLLM(model="gemini-2.0-flash-exp", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add Wikipedia capabilities
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Use it!
response = agent.invoke("Tell me about quantum computing")
print(response)
```

**📖 [View Full Documentation →](Wikipedia_tool/README.md)**

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Codemni framework installed
- Tool-specific dependencies (see individual tool documentation)

### Install Codemni

```bash
pip install Codemni
```

### Install Tool Dependencies

Each tool may require additional packages. For Wikipedia Tool:

```bash
pip install wikipedia
```

## Quick Start

### Basic Integration Pattern

All Prebuild Tools follow the same integration pattern:

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool  # Import the tool

# 1. Initialize your LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-exp",
    api_key="YOUR_API_KEY_HERE"
)

# 2. Create your agent
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# 3. Create tool instance
wiki = WikipediaTool()

# 4. Add to agent (one line!)
wiki.add_to_agent(agent)

# 5. Use it naturally
response = agent.invoke("Search Wikipedia for artificial intelligence")
print(response)
```

### Using Multiple Tools

Combine multiple tools to create powerful agents:

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import OpenAILLM
from Codemni.Prebuild_Tools import WikipediaTool
# from Codemni.Prebuild_Tools import AnotherTool  # Future tools

llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add multiple tools
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# another_tool = AnotherTool()
# another_tool.add_to_agent(agent)

# Agent can now use all tools intelligently
response = agent.invoke("Research quantum computing and summarize")
```

### With Memory for Context

Enhance tools with conversation memory:

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import GoogleLLM
from Codemni.memory import ConversationalBufferMemory
from Codemni.Prebuild_Tools import WikipediaTool

llm = GoogleLLM(model="gemini-2.0-flash-exp", api_key="YOUR_API_KEY")
memory = ConversationalBufferMemory()

agent = Create_ToolCalling_Agent(
    llm=llm,
    memory=memory,
    verbose=True
)

wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Multi-turn conversation with context
response1 = agent.invoke("Who was Alan Turing?")
response2 = agent.invoke("What were his main contributions?")
response3 = agent.invoke("Tell me more about the Turing Test")
```

## How It Works

### Automatic Tool Registration

When you call `tool.add_to_agent(agent)`, the tool automatically:

1. **Registers Methods**: Adds all relevant methods as tools
2. **Sets Descriptions**: Provides clear descriptions for LLM decision-making
3. **Configures Parameters**: Defines expected parameters and types
4. **Handles Errors**: Wraps methods with robust error handling

### Intelligent Tool Selection

Your agent will automatically:

1. **Analyze User Query**: Understand what the user is asking
2. **Select Appropriate Tool**: Choose the best tool for the task
3. **Execute Tool Call**: Run the tool with correct parameters
4. **Format Response**: Present results in a user-friendly way

### Example Tool Selection Logic

```
User: "Search Wikipedia for machine learning"
Agent Thinks: User wants to search → Uses wikipedia_search tool

User: "Tell me about neural networks"  
Agent Thinks: User wants information → Uses wikipedia_quick_lookup tool

User: "Give me the full article on AI"
Agent Thinks: User wants complete content → Uses wikipedia_content tool
```

## Use Cases

### 1. Research Assistant Bot

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

llm = GoogleLLM(model="gemini-2.0-flash-thinking-exp-1219", api_key="YOUR_API_KEY")
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, verbose=True)

wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Deep research with reasoning
response = agent.invoke(
    "Research the history of artificial intelligence from 1950 to 2020. "
    "Identify key milestones and breakthroughs."
)
```

### 2. Educational Chatbot

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import OpenAILLM
from Codemni.memory import ConversationalWindowMemory
from Codemni.Prebuild_Tools import WikipediaTool

llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
memory = ConversationalWindowMemory(window_size=10)

agent = Create_ToolCalling_Agent(llm=llm, memory=memory, verbose=True)

wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Interactive learning session
while True:
    question = input("Student: ")
    if question.lower() in ['exit', 'quit']:
        break
    response = agent.invoke(question)
    print(f"Teacher: {response}\n")
```

### 3. Fact-Checking System

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

llm = GoogleLLM(model="gemini-2.0-flash-thinking-exp-1219", api_key="YOUR_API_KEY")
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True
)

wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Verify claims with reasoning
claim = "The first computer programmer was Ada Lovelace in the 1840s"
response = agent.invoke(f"Fact-check this claim using Wikipedia: {claim}")
```

### 4. Content Generation Assistant

```python
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.llm import GoogleLLM
from Codemni.Prebuild_Tools import WikipediaTool

llm = GoogleLLM(model="gemini-2.0-flash-exp", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Generate content based on Wikipedia research
response = agent.invoke(
    "Write a 500-word article about quantum computing "
    "using Wikipedia as a reference. Include key concepts and applications."
)
```

## Tool Comparison

| Feature | Wikipedia Tool | Future Tools |
|---------|----------------|--------------|
| **Purpose** | Knowledge retrieval | TBA |
| **Data Source** | Wikipedia | TBA |
| **Languages** | 200+ | TBA |
| **Free Tier** | ✅ Yes | TBA |
| **Authentication** | ❌ Not required | TBA |
| **Rate Limits** | Moderate | TBA |
| **Best For** | Research, Education | TBA |

## Best Practices

### 1. **Choose the Right Agent Type**

```python
# For speed and efficiency
from Codemni.Agents import Create_ToolCalling_Agent

# For basic reasoning
from Codemni.Agents import Create_Reasoning_Tool_Calling_Agent

# For deep analysis and transparency
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
```

### 2. **Use Memory When Needed**

```python
# For multi-turn conversations: Use memory
memory = ConversationalBufferMemory()
agent = Create_ToolCalling_Agent(llm=llm, memory=memory)

# For single queries: Skip memory for speed
agent = Create_ToolCalling_Agent(llm=llm)
```

### 3. **Enable Verbose Mode During Development**

```python
# Development: See what's happening
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Production: Silent operation
agent = Create_ToolCalling_Agent(llm=llm, verbose=False)
```

### 4. **Handle Tool-Specific Configuration**

```python
# Configure tools based on your needs
wiki_en = WikipediaTool(language="en")  # English
wiki_es = WikipediaTool(language="es")  # Spanish
wiki_fr = WikipediaTool(language="fr")  # French
```

## Contributing

We welcome contributions! To add a new Prebuild Tool:

1. **Follow the Pattern**: Study existing tools (e.g., WikipediaTool)
2. **Create Class**: Implement your tool as a class
3. **Add Methods**: Include relevant methods with docstrings
4. **Error Handling**: Implement robust error handling
5. **Add to Agent**: Create an `add_to_agent()` method
6. **Document**: Write comprehensive README
7. **Test**: Ensure it works with all agent types
8. **Submit PR**: Submit a pull request

For detailed contribution guidelines, visit the [main repository](https://github.com/CodexJitin/Codemni).

## Troubleshooting

### Tool Not Working

**Check:**
1. Tool dependencies are installed (`pip install wikipedia`)
2. `add_to_agent()` was called
3. Agent has proper LLM configuration
4. Network connection (for API-based tools)

### Agent Not Using Tool

**Solutions:**
- Make user queries clear and specific
- Enable `verbose=True` to see agent's thinking
- Check tool descriptions are clear
- Ensure tool is actually added to agent

### Import Errors

```python
# ✅ Correct import
from Codemni.Prebuild_Tools import WikipediaTool

# ❌ Wrong import
from Prebuild_Tools import WikipediaTool
```

## Documentation

- **[Wikipedia Tool](Wikipedia_tool/README.md)** - Complete documentation for Wikipedia integration
- **[Main Codemni Docs](../README.md)** - Core framework documentation
- **[Agents Guide](../Agents/README.md)** - Learn about different agent types

## Support

- 📫 Email: codexjitin@gmail.com
- 💼 LinkedIn: [CodexJitin](https://www.linkedin.com/in/codexjitin)
- 🐛 Issues: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- 📚 Documentation: [GitHub Repository](https://github.com/CodexJitin/Codemni)

## Author

**CodexJitin**
- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- LinkedIn: [CodexJitin](https://www.linkedin.com/in/codexjitin)
- Email: codexjitin@gmail.com

## License

This project is licensed under a Proprietary License. See the [LICENSE](../LICENSE) file for details.

---

<div align="center">

Made with ❤️ by [CodexJitin](https://github.com/CodexJitin)

</div>
