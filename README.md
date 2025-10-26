<div align="center">
  <img src="https://raw.githubusercontent.com/CodexJitin/Codemni/main/assets/codemni-logo.jpg" alt="Codemni Logo" width="200"/>
  
# Codemni

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)
[![PyPI](https://img.shields.io/badge/PyPI-Codemni-brightgreen.svg)](https://pypi.org/project/Codemni/)

### *Build Intelligent AI Agents with Full Control and Zero Complexity*

**Lightweight • Modular • Production-Ready**

</div>

Codemni is a Python framework that puts you in control of AI agent development. Build powerful tool-calling agents with custom logic, multi-provider LLM support, and flexible memory—without the bloat of heavy abstractions.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
  - [AI Agents](#1-ai-agents)
  - [LLM Module](#2-llm-module)
  - [Memory Module](#3-memory-module)
  - [Prebuild Tools](#4-prebuild-tools)
- [Complete Examples](#complete-examples)
- [Comparison Guide](#comparison-guide)
- [Best Practices](#best-practices)
- [Advanced Usage](#advanced-usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Author](#author)
- [Acknowledgments](#acknowledgments)
- [Changelog](#changelog)
- [Quick Reference](#quick-reference)

## Overview

**What is Codemni?**

Codemni empowers developers to create sophisticated AI agents without getting lost in complexity. Whether you're building chatbots, automation tools, or research assistants, Codemni provides the essential building blocks while keeping your code clean and maintainable.

**Why Choose Codemni?**

- **Full Control**: Write your own logic without fighting framework constraints
- **Clean Architecture**: Minimal abstractions mean you understand exactly what's happening
- **Production-Ready**: Built-in retries, error handling, and timeouts from day one
- **Truly Modular**: Use only what you need—every component works independently
- **Multi-Provider**: Switch between OpenAI, Google, Anthropic, Groq, and Ollama seamlessly

**Core Capabilities:**

- **3 Agent Types**: Standard, Reasoning, and Deep Reasoning agents for different use cases
- **5 LLM Providers**: OpenAI, Google Gemini, Anthropic Claude, Groq, and Ollama
- **4 Memory Strategies**: Buffer, Window, Token Buffer, and Summary Memory
- **Prebuild Tools**: Ready-to-use tools like Wikipedia integration
- **Custom Tools**: Add your own tools with simple Python functions

## Key Features

### Intelligent AI Agents

- **Three agent types** with varying reasoning capabilities
- **Dynamic tool selection** and execution based on context
- **Custom prompt support** to shape agent personality
- **Verbose mode** for debugging and monitoring
- **Memory integration** for stateful conversations

### Multi-Provider LLM Support

- **Unified interface** across all major LLM providers
- **Automatic retries** with exponential backoff for reliability
- **Configurable timeouts** to prevent hanging requests
- **Function and class-based APIs** for flexibility
- **Clear exception hierarchies** for better error handling

### Flexible Memory Management

- **Four memory strategies** optimized for different scenarios
- **Token-aware management** to control API costs
- **Intelligent summarization** for maintaining long conversation context
- **Sliding window** for recent message prioritization
- **Simple buffer** for complete conversation history

### Extensible Architecture

- **Easy tool creation** using standard Python functions
- **Plugin-style prebuild tools** that integrate in one line
- **Custom agent prompts** for specialized behaviors
- **Modular design** that scales with your needs

## Architecture

```
Codemni/
├── Agents/                          # AI Agent implementations
│   ├── TOOL_CALLING_AGENT/          # Standard tool-calling agent
│   ├── REASONING_TOOL_CALLING_AGENT/    # Agent with basic reasoning
│   └── DEEP_REASONING_TOOL_CALLING_AGENT/  # Advanced reasoning agent
├── llm/                             # LLM provider wrappers
│   ├── OpenAI_llm.py               # OpenAI GPT models
│   ├── Google_llm.py               # Google Gemini models
│   ├── Anthropic_llm.py            # Anthropic Claude models
│   ├── Groq_llm.py                 # Groq models
│   └── Ollama_llm.py               # Ollama local models
├── memory/                          # Conversation memory strategies
│   ├── conversational_buffer_memory.py      # Store all messages
│   ├── conversational_window_memory.py      # Sliding window
│   ├── conversational_token_buffer_memory.py  # Token-limited buffer
│   └── conversational_summary_memory.py     # Intelligent summarization
├── Prebuild_Tools/                  # Ready-to-use tools
│   └── Wikipedia_tool/              # Wikipedia search & retrieval
└── core/                            # Core utilities
    └── adapter.py                   # Tool execution engine
```

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- An API key for your chosen LLM provider

### Install from PyPI

```bash
# Install core package (includes all modules)
pip install Codemni

# Install with specific LLM provider
pip install Codemni[openai]      # For OpenAI
pip install Codemni[google]      # For Google Gemini
pip install Codemni[anthropic]   # For Anthropic Claude
pip install Codemni[groq]        # For Groq
pip install Codemni[ollama]      # For Ollama

# Install with all providers
pip install Codemni[all]

# Install for development
pip install Codemni[dev]
```

### Dependencies

**Core (always installed):**
- `requests>=2.31.0`
- `python-dotenv>=1.0.0`

**Optional (install as needed):**
- `openai>=1.0.0` - For OpenAI models
- `google-generativeai>=0.3.0` - For Google Gemini
- `anthropic>=0.25.0` - For Anthropic Claude
- `groq>=0.4.0` - For Groq
- `ollama>=0.1.0` - For Ollama
- `wikipedia>=1.4.0` - For Wikipedia tool

## Quick Start

### Basic Tool-Calling Agent

```python
from Agents import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM
import datetime

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash",
    api_key="YOUR_API_KEY"  # or set GOOGLE_API_KEY env var
)

# Create agent
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Define a tool
def get_current_time():
    """Get the current date and time"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Add tool to agent
agent.add_tool(
    name="get_current_time",
    description="Get the current date and time",
    function=get_current_time
)

# Use the agent
response = agent.run("What time is it?")
print(response)
```

### With Memory

```python
from Agents import Create_ToolCalling_Agent
from llm.OpenAI_llm import OpenAILLM
from memory import ConversationalWindowMemory

# Initialize with memory
llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
memory = ConversationalWindowMemory(window_size=10)

agent = Create_ToolCalling_Agent(
    llm=llm,
    memory=memory,
    verbose=True
)

# Conversations maintain context
agent.run("My name is Alice")
agent.run("What's my name?")  # Agent remembers: "Your name is Alice"
```

### Using Prebuild Tools

```python
from Agents import Create_ToolCalling_Agent
from llm.Anthropic_llm import AnthropicLLM
from Prebuild_Tools import WikipediaTool

llm = AnthropicLLM(model="claude-3-5-sonnet-20241022", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add Wikipedia tool
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Query Wikipedia through the agent
response = agent.run("Tell me about quantum computing")
print(response)
```

## Core Components

Codemni consists of four main components. Each has detailed documentation in its respective directory:

### 1. AI Agents

Three types of agents with varying reasoning capabilities:

| Agent Type | Speed | Best For | Documentation |
|------------|-------|----------|---------------|
| **TOOL_CALLING_AGENT** | Fastest | Production APIs | [Agent Docs](Agents/TOOL_CALLING_AGENT/README.md) |
| **REASONING_TOOL_CALLING_AGENT** | Fast (4.6s) | General applications | [Agent Docs](Agents/REASONING_TOOL_CALLING_AGENT/README.md) |
| **DEEP_REASONING_TOOL_CALLING_AGENT** | Slower (11.1s) | Research & debugging | [Agent Docs](Agents/DEEP_REASONING_TOOL_CALLING_AGENT/README.md) |

**Quick Example:**
```python
from Agents import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM

llm = GoogleLLM(model="gemini-2.0-flash", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add tools and use
def calculator(expression):
    return str(eval(expression))

agent.add_tool("calculator", "Evaluate math expressions", calculator)
response = agent.run("What is 125 * 48?")
```

**Key Differences:**
- **Standard Agent**: Direct tool calling, fastest, lowest cost
- **Reasoning Agent**: Shows thinking process, balanced speed/transparency
- **Deep Reasoning Agent**: Comprehensive analysis, self-reflection, error recovery

**[View Full Agent Documentation](Agents/)**

### 2. LLM Module

Unified interface for multiple LLM providers with built-in retries and error handling.

**Supported Providers:**
- **OpenAI** - GPT-4, GPT-3.5-turbo, GPT-4-turbo
- **Google** - Gemini Pro, Gemini 2.0 Flash
- **Anthropic** - Claude 3 (Opus, Sonnet, Haiku)
- **Groq** - Llama, Mixtral, Gemma
- **Ollama** - Any local model

**Quick Example:**
```python
# Function-based API (one-off calls)
from llm.OpenAI_llm import openai_llm

response = openai_llm(
    prompt="Explain Python in one sentence",
    model="gpt-4",
    api_key="YOUR_API_KEY"
)

# Class-based API (for agents)
from llm.Google_llm import GoogleLLM

llm = GoogleLLM(model="gemini-2.0-flash", api_key="YOUR_API_KEY")
response = llm.generate_response("What is machine learning?")
```

**Features:**

- Automatic retries with exponential backoff
- Configurable timeouts
- Clear exception hierarchies
- Both function and class-based APIs
- Production-ready error handling

**[View Full LLM Documentation](llm/README.md)**

**Features:**
- ✅ Automatic retries with exponential backoff
- ✅ Configurable timeouts
- ✅ Clear exception hierarchies
- ✅ Both function and class-based APIs
- ✅ Production-ready error handling

📚 **[View Full LLM Documentation →](llm/README.md)**

---

### 3. Memory Module

Four strategies for managing conversation history:

| Memory Type | Limit | Best For | Documentation |
|-------------|-------|----------|---------------|
| **Buffer Memory** | None | Short conversations | [📖 Memory Docs](memory/README.md#1-conversationalbuffermemory) |
| **Window Memory** | Message count | Long conversations | [📖 Memory Docs](memory/README.md#2-conversationalwindowmemory) |
| **Token Buffer** | Token count | Cost-conscious apps | [� Memory Docs](memory/README.md#3-conversationaltokenbuffermemory) |
| **Summary Memory** | Intelligent | Very long conversations | [📖 Memory Docs](memory/README.md#4-conversationalsummarymemory) |

**Quick Example:**
```python
from memory import ConversationalWindowMemory

# Keep last 10 messages
memory = ConversationalWindowMemory(window_size=10)
memory.add_user_message("Hello!")
memory.add_ai_message("Hi! How can I help?")

history = memory.get_history()
```

**Integration with Agents:**
```python
from Agents import Create_ToolCalling_Agent
from memory import ConversationalBufferMemory

memory = ConversationalBufferMemory()
agent = Create_ToolCalling_Agent(llm=llm, memory=memory)

# Agent maintains conversation context
agent.run("My name is Alice")
agent.run("What's my name?")  # Remembers: "Alice"
```

**[View Full Memory Documentation](memory/README.md)**

### 4. Prebuild Tools

Ready-to-use tools for common tasks:

**Available Tools:**
- **Wikipedia Tool** - Search and retrieve Wikipedia content

**Quick Example:**
```python
from Prebuild_Tools import WikipediaTool

wiki = WikipediaTool(language="en")

# Search Wikipedia
results = wiki.search("Python programming")

# Get article summary
summary = wiki.get_summary("Python (programming language)", sentences=3)

# Add all Wikipedia tools to an agent
wiki.add_to_agent(agent)
```

**Automatic Integration:**
The `add_to_agent()` method automatically registers all Wikipedia-related tools with your agent, enabling natural language queries like:
- "Search Wikipedia for quantum computing"
- "Get me a summary of machine learning from Wikipedia"
- "Find information about Albert Einstein on Wikipedia"

**[View Full Tools Documentation](Prebuild_Tools/README.md)**

## Complete Examples

### Example 1: Multi-Tool Calculator Agent

```python
from Agents import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM
import math
import datetime

# Initialize
llm = GoogleLLM(model="gemini-2.0-flash", api_key="YOUR_API_KEY")
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Define tools
def calculator(expression):
    """Evaluate mathematical expressions"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

def get_time():
    """Get current time"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def square_root(number):
    """Calculate square root"""
    try:
        return str(math.sqrt(float(number)))
    except Exception as e:
        return f"Error: {str(e)}"

# Add tools
agent.add_tool("calculator", "Evaluate math expressions", calculator)
agent.add_tool("get_time", "Get current time", get_time)
agent.add_tool("square_root", "Calculate square root", square_root)

# Use agent
print(agent.run("What is 125 * 48?"))
print(agent.run("What is the square root of 144?"))
print(agent.run("What time is it?"))
```

### Example 2: Research Assistant with Memory

```python
from Agents.REASONING_TOOL_CALLING_AGENT import Create_ToolCalling_Agent
from llm.Anthropic_llm import AnthropicLLM
from memory import ConversationalSummaryMemory
from Prebuild_Tools import WikipediaTool

# Initialize components
llm = AnthropicLLM(model="claude-3-5-sonnet-20241022", api_key="YOUR_API_KEY")
memory = ConversationalSummaryMemory(llm=llm, max_messages_before_summary=15)

# Create agent
agent = Create_ToolCalling_Agent(llm=llm, memory=memory, verbose=True)

# Add Wikipedia tool
wiki = WikipediaTool()
wiki.add_to_agent(agent)

# Multi-turn research conversation
agent.run("Tell me about quantum computing")
agent.run("What are its practical applications?")
agent.run("Who are the pioneers in this field?")
agent.run("Summarize everything we discussed")  # Memory maintains context
```

### Example 3: Deep Reasoning Problem Solver

```python
from Agents.DEEP_REASONING_TOOL_CALLING_AGENT import Create_Deep_Reasoning_Tool_Calling_Agent
from llm.OpenAI_llm import OpenAILLM

# Initialize with deep reasoning
llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True,
    min_confidence=0.7
)

# Define complex tool
def analyze_data(dataset_name):
    """Analyze a dataset and return statistics"""
    # Simulated analysis
    return f"Dataset '{dataset_name}': Mean=45.2, Median=43.0, StdDev=12.5"

agent.add_tool(
    "analyze_data",
    "Analyze dataset and return statistical summary",
    analyze_data
)

# Complex query - shows deep reasoning process
response = agent.run(
    "I need to understand the statistical properties of the sales_2024 dataset. "
    "Analyze it and explain what the numbers mean for business decisions."
)
```

### Example 4: Custom Prompt Agent

```python
from Agents import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM

llm = GoogleLLM(model="gemini-2.0-flash", api_key="YOUR_API_KEY")

# Custom agent personality
custom_prompt = """You are a friendly and enthusiastic math tutor for children.
Always explain concepts in simple terms and use encouraging language.
Make math fun and approachable!"""

agent = Create_ToolCalling_Agent(
    llm=llm,
    prompt=custom_prompt,
    verbose=True
)

# Agent responds with custom personality
def calculator(expression):
    return str(eval(expression))

agent.add_tool("calculator", "Calculate math problems", calculator)
response = agent.run("What is 7 times 8?")
```

## Comparison Guide

### Agent Types Comparison

| Feature | TOOL_CALLING | REASONING | DEEP_REASONING |
|---------|-------------|-----------|----------------|
| **Speed** | Fastest | Fast (4.63s) | Slower (11.11s) |
| **Token Usage** | Lowest | Low (600-900) | High (1500-2800) |
| **Reasoning Display** | None | Basic | Deep chain-of-thought |
| **Problem Analysis** | None | Minimal | Comprehensive |
| **Situation Awareness** | No | No | Yes |
| **Self-Reflection** | No | No | Confidence + alternatives |
| **Error Recovery** | Basic | Basic retry | Strategic alternatives |
| **Best For** | Production APIs | General apps | Research & debugging |
| **Cost** | Lowest | Medium | Highest |
| **Transparency** | Low | Medium | Highest |

### Memory Types Comparison

| Memory Type | Size Limit | Use Case | Token Cost |
|-------------|-----------|----------|------------|
| **Buffer** | None | Short conversations | Can grow large |
| **Window** | Fixed count | Long conversations | Predictable |
| **Token Buffer** | Token limit | Cost-conscious apps | Optimized |
| **Summary** | Intelligent | Very long conversations | Medium + summary cost |

### LLM Providers Comparison

| Provider | Speed | Cost | Best For |
|----------|-------|------|----------|
| **OpenAI (GPT-4)** | Medium | High | Best quality |
| **Google (Gemini)** | Fast | Low | Fast, cost-effective |
| **Anthropic (Claude)** | Medium | Medium | Long context, reasoning |
| **Groq** | Very Fast | Very Low | Speed priority |
| **Ollama** | Varies | Free | Local/private |

## Best Practices

### 1. Choosing the Right Agent

```python
# For production APIs - use TOOL_CALLING_AGENT
# Fast, cost-efficient, reliable
from Agents.TOOL_CALLING_AGENT import Create_ToolCalling_Agent

# For user-facing apps - use REASONING_TOOL_CALLING_AGENT
# Shows thinking, still efficient
from Agents.REASONING_TOOL_CALLING_AGENT import Create_ToolCalling_Agent

# For research/debugging - use DEEP_REASONING_TOOL_CALLING_AGENT
# Deep analysis, comprehensive reasoning
from Agents.DEEP_REASONING_TOOL_CALLING_AGENT import Create_Deep_Reasoning_Tool_Calling_Agent
```

### 2. Memory Selection

```python
# Short conversations (<10 exchanges)
memory = ConversationalBufferMemory()

# Long conversations (need recent context)
memory = ConversationalWindowMemory(window_size=10)

# Budget-conscious (control token usage)
memory = ConversationalTokenBufferMemory(max_tokens=2000, model="gpt-4")

# Very long conversations (need full context)
memory = ConversationalSummaryMemory(llm=llm)
```

### 3. Tool Design

```python
# GOOD: Clear, focused tool
def get_weather(city):
    """Get current weather for a specific city"""
    # Implementation
    return weather_data

# BAD: Too broad, unclear purpose
def do_stuff(input):
    """Does various things"""
    # Implementation
```

**Tool Best Practices:**

- Clear, descriptive names
- Focused functionality (one tool = one task)
- Good error handling
- Detailed docstrings
- Return strings or serializable data

### 4. Error Handling

```python
from llm.OpenAI_llm import OpenAILLM, OpenAILLMError

try:
    llm = OpenAILLM(model="gpt-4", api_key="YOUR_API_KEY")
    response = llm.generate_response("Hello")
except OpenAILLMError as e:
    # Handle LLM-specific errors
    print(f"LLM Error: {e}")
except Exception as e:
    # Handle other errors
    print(f"Unexpected error: {e}")
```

### 5. API Key Management

```python
import os
from dotenv import load_dotenv

# Use environment variables
load_dotenv()

llm = GoogleLLM(
    model="gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY")  # From .env file
)
```

**.env file:**
```bash
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
ANTHROPIC_API_KEY=your_anthropic_key
GROQ_API_KEY=your_groq_key
```

### 6. Verbose Mode Usage

```python
# Development: verbose=True for debugging
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Production: verbose=False for clean logs
agent = Create_ToolCalling_Agent(llm=llm, verbose=False)
```

## Advanced Usage

### Custom Tool with Complex Parameters

```python
def temperature_converter(temperature, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin
    
    Args:
        temperature: Temperature value
        from_unit: Source unit (C, F, or K)
        to_unit: Target unit (C, F, or K)
    """
    temp = float(temperature)
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    # Convert to Celsius first
    if from_unit == 'F':
        celsius = (temp - 32) * 5/9
    elif from_unit == 'K':
        celsius = temp - 273.15
    else:
        celsius = temp
    
    # Convert to target
    if to_unit == 'F':
        result = (celsius * 9/5) + 32
    elif to_unit == 'K':
        result = celsius + 273.15
    else:
        result = celsius
    
    return f"{result:.2f} {to_unit}"

agent.add_tool(
    "temperature_converter",
    "Convert temperature between Celsius (C), Fahrenheit (F), and Kelvin (K)",
    temperature_converter
)
```

### Multi-Agent System

```python
# Create specialized agents
research_agent = Create_ToolCalling_Agent(llm=llm1)
wiki = WikipediaTool()
wiki.add_to_agent(research_agent)

analysis_agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm2)
# Add analysis tools...

# Coordinate agents
def coordinated_research(query):
    # First agent gathers information
    info = research_agent.run(f"Find information about {query}")
    
    # Second agent analyzes
    analysis = analysis_agent.run(f"Analyze this information: {info}")
    
    return analysis
```

### Dynamic Tool Loading

```python
def load_tools_from_config(agent, config):
    """Load tools from configuration"""
    for tool_config in config["tools"]:
        name = tool_config["name"]
        description = tool_config["description"]
        
        # Dynamically import tool function
        module = __import__(tool_config["module"])
        function = getattr(module, tool_config["function"])
        
        agent.add_tool(name, description, function)
```

### Streaming Responses (Future Enhancement)

```python
# Note: Streaming support coming in future version
# Current: Get complete response
response = agent.run("Tell me about AI")

# Future: Stream response chunks
for chunk in agent.run_stream("Tell me about AI"):
    print(chunk, end="", flush=True)
```

## Project Structure

```
Codemni/
│
├── __init__.py                      # Package initialization
├── pyproject.toml                   # Project configuration
├── requirements.txt                 # Dependencies
├── LICENSE                          # Proprietary license
├── README.md                        # This file
│
├── Agents/                          # AI Agent implementations
│   ├── __init__.py
│   ├── TOOL_CALLING_AGENT/
│   │   ├── __init__.py
│   │   ├── agent.py                 # Standard agent
│   │   ├── prompt.py                # Agent prompts
│   │   └── README.md                # Agent documentation
│   ├── REASONING_TOOL_CALLING_AGENT/
│   │   ├── __init__.py
│   │   ├── agent.py                 # Reasoning agent
│   │   ├── prompt.py
│   │   └── README.md
│   └── DEEP_REASONING_TOOL_CALLING_AGENT/
│       ├── __init__.py
│       ├── agent.py                 # Deep reasoning agent
│       ├── prompt.py
│       └── README.md
│
├── llm/                             # LLM provider wrappers
│   ├── __init__.py
│   ├── OpenAI_llm.py               # OpenAI integration
│   ├── Google_llm.py               # Google Gemini integration
│   ├── Anthropic_llm.py            # Anthropic Claude integration
│   ├── Groq_llm.py                 # Groq integration
│   ├── Ollama_llm.py               # Ollama integration
│   └── README.md                    # LLM documentation
│
├── memory/                          # Conversation memory
│   ├── __init__.py
│   ├── conversational_buffer_memory.py
│   ├── conversational_window_memory.py
│   ├── conversational_token_buffer_memory.py
│   ├── conversational_summary_memory.py
│   └── README.md                    # Memory documentation
│
├── Prebuild_Tools/                  # Ready-to-use tools
│   ├── __init__.py
│   ├── README.md
│   └── Wikipedia_tool/
│       ├── __init__.py
│       ├── wikipedia_tool.py
│       └── README.md
│
└── core/                            # Core utilities
    ├── __init__.py
    └── adapter.py                   # Tool execution engine
```

## Development

### Setting Up Development Environment

```bash
# Clone repository (if contributing)
git clone https://github.com/CodexJitin/Codemni.git
cd Codemni

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install all providers
pip install -e .[all]
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Contributing

Codemni is proprietary software. However, we welcome:

- **Bug reports** - Submit issues on GitHub
- **Feature requests** - Share your ideas
- **Documentation improvements** - Help others learn
- **Example contributions** - Share your use cases

**To contribute:**

1. Open an issue describing your contribution
2. Wait for approval from maintainers
3. Submit a pull request if approved

## License

**Proprietary License** - Copyright (c) 2025 CodexJitin. All Rights Reserved.

### Permitted Use

- Install via PyPI (`pip install Codemni`)
- Use in commercial/non-commercial projects
- Integrate as a dependency

### Restrictions

- Cannot copy, modify, or redistribute source code
- Cannot reverse engineer
- Cannot remove proprietary notices

See [LICENSE](LICENSE) file for complete terms.

## Support

### Documentation

- **Main Documentation**: This README
- **LLM Module**: [llm/README.md](llm/README.md)
- **Memory Module**: [memory/README.md](memory/README.md)
- **Agent Guides**: Individual README in each agent folder
- **Tools**: [Prebuild_Tools/README.md](Prebuild_Tools/README.md)

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions)
- **Email**: Contact CodexJitin

### Useful Links

- **Homepage**: [https://github.com/CodexJitin/Codemni](https://github.com/CodexJitin/Codemni)
- **PyPI**: [https://pypi.org/project/Codemni/](https://pypi.org/project/Codemni/)
- **Bug Tracker**: [https://github.com/CodexJitin/Codemni/issues](https://github.com/CodexJitin/Codemni/issues)
- **Documentation**: [GitHub README](https://github.com/CodexJitin/Codemni#readme)

## Author

**CodexJitin**

- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- Project: [Codemni](https://github.com/CodexJitin/Codemni)

## Acknowledgments

Built for the AI developer community.

Special thanks to:
- OpenAI, Google, Anthropic, Groq, and Ollama for their amazing LLM APIs
- The Python community for excellent tools and libraries
- All contributors and users of Codemni

## Changelog

### Version 1.2.2 (Current)
- Stable release with all core features
- Three agent types with varying reasoning capabilities
- Five LLM provider integrations
- Four memory management strategies
- Wikipedia prebuild tool
- Comprehensive documentation

### Roadmap

- Streaming response support
- More prebuild tools
- Agent analytics and monitoring
- Web search tool
- Database tool integration
- Enhanced customization options

## Quick Reference

### Installation
```bash
pip install Codemni[all]
```

### Basic Agent
```python
from Agents import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM

llm = GoogleLLM(model="gemini-2.0-flash", api_key="KEY")
agent = Create_ToolCalling_Agent(llm=llm)
agent.add_tool("name", "description", function)
response = agent.run("query")
```

### With Memory
```python
from memory import ConversationalWindowMemory
memory = ConversationalWindowMemory(window_size=10)
agent = Create_ToolCalling_Agent(llm=llm, memory=memory)
```

### With Prebuild Tools
```python
from Prebuild_Tools import WikipediaTool
wiki = WikipediaTool()
wiki.add_to_agent(agent)
```

<div align="center">

**Made by CodexJitin**

**Star this project if you find it useful!**

[Report Bug](https://github.com/CodexJitin/Codemni/issues) · [Request Feature](https://github.com/CodexJitin/Codemni/issues) · [Documentation](https://github.com/CodexJitin/Codemni#readme)

</div>
