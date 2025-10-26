# LLM Module

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)

Production-ready LLM wrappers with robust error handling, retries, and minimal dependencies.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Supported Providers](#supported-providers)
- [Two Ways to Use](#two-ways-to-use)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Exception Hierarchy](#exception-hierarchy)
- [Environment Variables](#environment-variables)
- [Best Practices](#best-practices)
- [Author](#author)
- [License](#license)
- [Support](#support)

## Overview

A unified Python module that provides simple, consistent interfaces to multiple Large Language Model (LLM) providers. Each wrapper is designed for production use with built-in retry logic, timeout handling, and clear exception hierarchies.

**Two Interfaces Available:**
- **Function-based**: For one-off calls with all parameters
- **Class-based**: For stateful usage with agents (NEW!)

## Features

- Automatic Retries: Built-in exponential backoff for transient failures
- Timeout Support: Configurable request timeouts to prevent hanging
- Robust Error Handling: Clear exception hierarchy for each provider
- No Logging: Silent operation by design
- Minimal Dependencies: Only install what you need
- Consistent API: Same interface across all providers
- Production-Ready: Input validation and defensive coding practices
- Two Interfaces: Functions for one-off calls, Classes for stateful usage

## Installation

### Prerequisites

- Python 3.8 or higher

### Install via PyPI

```bash
pip install Codemni
```

> **Note:** Codemni is available exclusively through PyPI. For documentation and support, visit the [GitHub repository](https://github.com/CodexJitin/Codemni).

### Optional Dependencies

Install provider-specific packages as needed:

```bash
# For OpenAI
pip install openai>=1.0.0

# For Anthropic Claude
pip install anthropic>=0.18.0

# For Groq
pip install groq>=0.4.0

# For Google Gemini
pip install google-generativeai>=0.3.0

# For Ollama (local models)
pip install ollama>=0.1.0
```

## Supported Providers

| Provider | Function | Class | Models Supported |
|----------|----------|-------|-----------------|
| **Google Gemini** | `google_llm()` | `GoogleLLM` | gemini-2.5-flash, gemini-2.0-flash, gemini-2.5-pro, gemini-2.0-flash-lite, gemini-2.5-flash-lite |
| **OpenAI** | `openai_llm()` | `OpenAILLM` | gpt-4, gpt-3.5-turbo, o1, o3 |
| **Anthropic Claude** | `anthropic_llm()` | `AnthropicLLM` | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| **Groq** | `groq_llm()` | `GroqLLM` | llama3-70b-8192, mixtral-8x7b-32768 |
| **Ollama** | `ollama_llm()` | `OllamaLLM` | llama2, mistral, codellama (local) |

## Two Ways to Use

### Option 1: Function-Based

Perfect for one-off calls where you pass all parameters each time:

```python
from Codemni.llm import openai_llm

response = openai_llm(
    prompt="What is Python?",
    model="gpt-4",
    api_key="your-api-key"
)
```

### Option 2: Class-Based

Perfect for agents and repeated calls with the same configuration:

```python
from Codemni.llm import OpenAILLM

llm = OpenAILLM(model="gpt-4", api_key="your-api-key")

response1 = llm.generate_response("What is Python?")
response2 = llm.generate_response("What is JavaScript?")
```

## Quick Start

### Function-Based Examples

#### Google Gemini

```python
from Codemni.llm import google_llm, GoogleLLMError

try:
    response = google_llm(
        prompt="Explain Python in one sentence",
        model="gemini-pro",
        api_key="your-api-key-here"  # or set GOOGLE_API_KEY env var
    )
    print(response)
except GoogleLLMError as e:
    print(f"Error: {e}")
```

#### OpenAI

```python
from Codemni.llm import openai_llm, OpenAILLMError

try:
    response = openai_llm(
        prompt="Write a haiku about programming",
        model="gpt-3.5-turbo",
        api_key="your-api-key-here",  # or set OPENAI_API_KEY env var
        temperature=0.7,
        max_tokens=50
    )
    print(response)
except OpenAILLMError as e:
    print(f"Error: {e}")
```

### Class-Based Examples

#### OpenAI Class

```python
from Codemni.llm import OpenAILLM

llm = OpenAILLM(
    model="gpt-4",
    api_key="your-api-key",  # or set OPENAI_API_KEY env var
    temperature=0.7
)

response = llm.generate_response("What is artificial intelligence?")
print(response)
```

#### Google Gemini Class

```python
from Codemni.llm import GoogleLLM

llm = GoogleLLM(
    model="gemini-2.5-pro",
    api_key="your-api-key",  # or set GOOGLE_API_KEY env var
    temperature=0.9
)

response = llm.generate_response("Write a creative story")
print(response)
```

#### Anthropic Claude Class

```python
from Codemni.llm import AnthropicLLM

llm = AnthropicLLM(
    model="claude-3-sonnet-20240229",
    api_key="your-api-key",  # or set ANTHROPIC_API_KEY env var
    max_tokens=4096
)

response = llm.generate_response("Explain quantum computing")
print(response)
```

#### Groq Class

```python
from Codemni.llm import GroqLLM

llm = GroqLLM(
    model="llama3-70b-8192",
    api_key="your-api-key",  # or set GROQ_API_KEY env var
    temperature=0.3
)

response = llm.generate_response("What is AI?")
print(response)
```

#### Ollama Class

```python
from Codemni.llm import OllamaLLM

llm = OllamaLLM(
    model="llama2",
    base_url="http://localhost:11434",  # or set OLLAMA_BASE_URL env var
    temperature=0.8
)

response = llm.generate_response("Explain Docker")
print(response)
```

#### Use with Agents

Classes are perfect for use with agents that expect a `generate_response()` method:

```python
from Codemni.llm import OpenAILLM
from Codemni.Agents import Create_ToolCalling_Agent

# Initialize LLM
llm = OpenAILLM(model="gpt-4", api_key="your-key")

# Pass to agent
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add tools
agent.add_tool("calculator", "Calculate expressions", lambda x: eval(x))

# Use agent
result = agent.invoke("What is 100 + 200?")
```

## API Reference

All LLM functions and classes share a similar signature.

### Common Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | `str` | Yes | - | The input text/prompt to send to the model |
| `model` | `str` | Yes | - | Model identifier (e.g., "gpt-4", "gemini-pro") |
| `api_key` | `str` | No | `None` | API key (falls back to environment variable) |
| `max_retries` | `int` | No | `3` | Number of retry attempts on failures |
| `timeout` | `float` | No | `30.0` | Request timeout in seconds (60s for Ollama) |
| `backoff_factor` | `float` | No | `0.5` | Exponential backoff multiplier for retries |
| `temperature` | `float` | No | `None` | Sampling temperature (0.0-1.0 or 0.0-2.0) |
| `max_tokens` | `int` | No | Provider-specific | Maximum tokens in response |

### Provider-Specific Notes

**Google Gemini:**
- Environment variable: `GOOGLE_API_KEY`
- Robust response extraction handles different client versions
- Supports safety settings and generation config

**OpenAI:**
- Environment variable: `OPENAI_API_KEY`
- Supports both chat models (gpt-4) and legacy completion models
- Temperature range: 0.0-2.0

**Anthropic Claude:**
- Environment variable: `ANTHROPIC_API_KEY`
- `max_tokens` parameter is required (default: 4096)
- Temperature range: 0.0-1.0

**Groq:**
- Environment variable: `GROQ_API_KEY`
- Fast inference with open-source models
- Temperature range: 0.0-2.0

**Ollama:**
- Environment variable: `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- Requires Ollama server running locally
- No API key required
- Default timeout: 60 seconds

## Exception Hierarchy

Each provider has its own exception hierarchy:

```
{Provider}LLMError
    ├── {Provider}LLMImportError     # SDK not installed or import failed
    ├── {Provider}LLMAPIError         # API request failed after retries
    └── {Provider}LLMResponseError    # Response parsing/validation failed
```

Example for Google:

```python
from Codemni.llm import (
    GoogleLLMError,
    GoogleLLMImportError,
    GoogleLLMAPIError,
    GoogleLLMResponseError
)
```

## Environment Variables

Set these environment variables to avoid passing API keys in code:

```bash
export GOOGLE_API_KEY="your-google-key"
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GROQ_API_KEY="your-groq-key"
export OLLAMA_BASE_URL="http://localhost:11434"  # Optional, has default
```

Or use a `.env` file with `python-dotenv`:

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()

# Now environment variables are loaded
from Codemni.llm import google_llm
response = google_llm(prompt="Hello", model="gemini-pro")
```

## Best Practices

### 1. Choose the Right Interface

- **Function-based**: One-off calls, quick scripts
- **Class-based**: Agents, repeated calls, stateful usage

### 2. Handle Exceptions Properly

```python
from Codemni.llm import openai_llm, OpenAILLMError

try:
    response = openai_llm(prompt="Hello", model="gpt-4", api_key="key")
except OpenAILLMError as e:
    print(f"Error occurred: {e}")
```

### 3. Use Environment Variables

Store API keys in environment variables, not in code:

```python
# Good
llm = OpenAILLM(model="gpt-4")  # Uses OPENAI_API_KEY env var

# Avoid
llm = OpenAILLM(model="gpt-4", api_key="sk-...")  # Hardcoded
```

### 4. Configure Retries and Timeouts

Adjust for your use case:

```python
llm = OpenAILLM(
    model="gpt-4",
    max_retries=5,
    timeout=60.0,
    backoff_factor=1.0
)
```

### 5. Minimal Dependencies

Only install the providers you need to keep your environment lean.

## Author

**CodexJitin**

- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- LinkedIn: [linkedin.com/in/codexjitin](https://www.linkedin.com/in/codexjitin)
- Email: codexjitin@gmail.com

### About the Developer

Passionate about building production-ready AI tools and frameworks. Creator of Codemni, a comprehensive toolkit for developing AI agents with advanced reasoning capabilities.

## License

This project is licensed under a **Proprietary License**. See the [LICENSE](../../LICENSE) file for details.

© 2025 CodexJitin. All rights reserved.

## Acknowledgments

- Built with support from the open-source AI community
- Designed for seamless integration with multiple LLM providers
- Optimized for production use with robust error handling

## Support

- **Documentation**: [GitHub Repository](https://github.com/CodexJitin/Codemni)
- **Issues**: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions)

**Part of the Codemni AI Agent Framework** | Built by [CodexJitin](https://github.com/CodexJitin)
