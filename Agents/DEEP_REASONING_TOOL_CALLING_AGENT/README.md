# 🧠 Deep Reasoning Tool Calling Agent

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)

An advanced AI agent with **deep chain-of-thought reasoning**, dynamic problem analysis, self-reflection, and error recovery capabilities.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Comparison](#comparison-reasoning-vs-deep-reasoning-agent)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration-options)
- [Best Practices](#best-practices)
- [Performance Considerations](#performance-considerations)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Overview

The `Create_Deep_Reasoning_Tool_Calling_Agent` provides sophisticated reasoning capabilities that go far beyond simple tool execution. Unlike basic agents that simply call tools, this agent:

- **Understands** the problem deeply before acting
- **Analyzes** the current situation dynamically at each step
- **Reasons** through complex multi-step problems
- **Reflects** on its decisions with confidence scoring
- **Recovers** from errors with alternative approaches

**Performance Note:** This agent is ~2.4x slower than the basic reasoning agent but provides significantly deeper transparency and reasoning capabilities. Use it when you need to understand *how* the AI is thinking, not just *what* it's doing.

## Key Features

### 1. **Problem Understanding**

- Deeply analyzes the user's query
- Identifies key requirements and constraints
- Breaks down complex questions into components
- Understands the real intent behind questions

### 2. **Current Situation Awareness**

- Tracks what information has been gathered
- Identifies what's still missing
- Shows progress toward the goal
- Adapts reasoning based on context

### 3. **Deep Reasoning Process**

- **What I Need Now:** Identifies immediate requirements
- **Why I Need It:** Explains the reasoning behind each action
- **Thought Process:** Shows step-by-step logical thinking
- **Expected Outcome:** Predicts what will happen

### 4. **Tool Decision Logic**

- Explains why a specific tool is chosen
- Details what parameters to use and why
- Shows how the tool output will be used

### 5. **Self-Reflection & Verification**

- Provides confidence scoring (0.0-1.0)
- Plans for error recovery ("If This Fails")
- Questions if its approach makes sense
- Transparent about uncertainty

### 6. **Error Recovery**

- Doesn't give up on first failure
- Analyzes errors and adjusts parameters
- Tries alternative tools if needed
- Maintains reasoning even when tools fail

## Comparison: Reasoning vs Deep Reasoning Agent

| Feature | REASONING Agent | DEEP_REASONING Agent |
|---------|-----------------|----------------------|
| **Speed** | Fast (4.63s avg) | Slower (11.11s avg) |
| **Token Usage** | Low (600-900) | High (1500-2800) |
| **Thinking Display** | Basic | Deep chain-of-thought |
| **Problem Analysis** | None | Comprehensive breakdown |
| **Situation Awareness** | None | Dynamic context tracking |
| **Reasoning Depth** | Surface-level | Multi-layered reasoning |
| **Self-Reflection** | None | Confidence + alternatives |
| **Error Recovery** | Basic retry | Strategic alternatives |
| **Best For** | Production APIs | Research & Debugging |
| **Verification** | None | Checks results make sense |
| **Ambiguity Handling** | Limited | Identifies unclear aspects |

## Installation

### Prerequisites

- Python 3.8 or higher
- An LLM API key (Google Gemini, OpenAI, Anthropic, etc.)

### Install via PyPI

```bash
pip install Codemni
```

> **Note:** Codemni is available exclusively through PyPI. For documentation and support, visit the [GitHub repository](https://github.com/CodexJitin/Codemni).

## Quick Start

### Basic Example

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-thinking-exp-1219",
    api_key="your-api-key"
)

# Create agent
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True
)

# Add a tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

agent.add_tool(
    name="calculator",
    description="Evaluate mathematical expressions",
    function=calculator
)

# Ask a question
response = agent.invoke("What is 15% of 240?")
print(response)
```

## Usage Examples

### Example 1: Complex Multi-Step Problem

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-thinking-exp-1219",
    api_key="your-api-key"
)

# Create deep reasoning agent
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True,
    min_confidence=0.7
)

# Add calculator tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    return str(eval(expression))

agent.add_tool(
    name="calculator",
    description="Evaluate mathematical expressions",
    function=calculator
)

# Use the agent
response = agent.invoke(
    "If I have 100 apples and give away 23%, "
    "then buy 50 more, how many do I have?"
)
print(response)
```

### Example 2: Integration with Memory

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import OpenAILLM
from Codemni.memory import ConversationalWindowMemory

# Initialize components
llm = OpenAILLM(model="gpt-4", api_key="your-api-key")
memory = ConversationalWindowMemory(window_size=10)

# Create agent with memory
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    memory=memory,
    verbose=True,
    show_reasoning=True
)

# Conversation with context
agent.invoke("My budget is $1000")
agent.invoke("If I spend 30% on rent, how much is left?")
agent.invoke("What if I save 20% of what's left?")
```

### Example 3: Custom Domain Expert

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import AnthropicLLM

llm = AnthropicLLM(model="claude-3-opus-20240229", api_key="your-api-key")

# Create a financial advisor agent
custom_prompt = """You are an expert financial advisor who provides detailed 
reasoning for all calculations and recommendations."""

agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    prompt=custom_prompt,
    verbose=True,
    show_reasoning=True,
    min_confidence=0.85  # High confidence for financial advice
)

# Add financial tools
def compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculate compound interest."""
    return principal * ((1 + rate) ** years)

agent.add_tool(
    name="compound_interest",
    description="Calculate compound interest: principal * (1 + rate)^years",
    function=compound_interest
)

response = agent.invoke(
    "If I invest $10,000 at 7% annual return for 10 years, "
    "what will it be worth?"
)
```

## Best Use Cases

1. **Complex Multi-Step Problems**
   - Math word problems
   - Multi-stage calculations
   - Problems requiring verification

2. **Ambiguous Queries**
   - Questions with unclear requirements
   - Situations needing clarification
   - Edge case handling

3. **High-Stakes Decisions**
   - When accuracy is critical
   - When you need to see the reasoning
   - When transparency matters

4. **Learning & Education**
   - Show step-by-step working
   - Explain mathematical processes
   - Demonstrate problem-solving approaches

## Configuration Options

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `llm` | LLM Instance | **Required** | The language model instance (GoogleLLM, OpenAILLM, etc.) |
| `verbose` | bool | `False` | Enable detailed console logging |
| `show_reasoning` | bool | `True` | Display the agent's reasoning process (highly recommended) |
| `prompt` | str | `None` | Custom system prompt to define agent behavior |
| `memory` | Memory | `None` | Memory instance for conversation history |
| `min_confidence` | float | `0.7` | Minimum confidence threshold (0.0-1.0) for warnings |

### Configuration Example

```python
from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm import GoogleLLM
from Codemni.memory import ConversationalBufferMemory

llm = GoogleLLM(model="gemini-2.0-flash-thinking-exp-1219", api_key="key")
memory = ConversationalBufferMemory()

agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,              # Show all operations
    show_reasoning=True,       # Display thinking process
    prompt="You are a helpful mathematics tutor.",
    memory=memory,             # Track conversation
    min_confidence=0.8         # Alert if confidence < 80%
)
```

## Output Structure

The agent provides rich, structured reasoning:

```text
🧠 Reasoning Iteration 1
═══════════════════════════════════════════════════════════════════════

📊 Problem Analysis:
  Understanding: Calculate percentage decrease, then addition
  Complexity: moderate
  Key Components:
    • Percentage calculation
    • Subtraction
    • Addition

📋 Execution Plan:
  ▸ Step 1: Calculate 23% of 100 apples
  ▸ Step 2: Subtract from original amount
  ▸ Step 3: Add 50 more apples
  ▸ Step 4: Verify result is reasonable

💭 Deep Reasoning:
  Current Step: Step 1
  Thought Process: Need to find 23% of 100. That's 0.23 × 100 = 23 apples
  Why This Approach: Percentage calculations require decimal conversion
  Expected Outcome: Should get 23 apples to subtract

🔍 Self-Reflection:
  Makes Sense? Yes, percentage logic is sound
  Confidence: 0.95
  🔄 Alternatives:
    • Could break into multiple calculator calls
    • Could calculate mentally and verify with tool
```

## Best Practices

### 1. **Enable Reasoning Display**

Always set `show_reasoning=True` to see the agent's thought process:

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    show_reasoning=True  # See the thinking!
)
```

### 2. **Set Appropriate Confidence Thresholds**

```python
# For critical applications
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, min_confidence=0.9)

# For exploratory tasks
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, min_confidence=0.6)
```

### 3. **Use Memory for Context**

```python
from Codemni.memory import ConversationalWindowMemory

memory = ConversationalWindowMemory(window_size=5)
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, memory=memory)
```

### 4. **Provide Clear Tool Descriptions**

```python
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax amount.
    
    Args:
        amount: The base amount
        rate: Tax rate as decimal (e.g., 0.15 for 15%)
    
    Returns:
        The calculated tax amount
    """
    return amount * rate

agent.add_tool(
    name="calculate_tax",
    description="Calculate tax: amount * rate (rate as decimal, e.g., 0.15 for 15%)",
    function=calculate_tax
)
```

### 5. **Handle Complex Queries**

Break down complex problems into clear components:

```python
# Good: Clear and specific
response = agent.invoke(
    "Calculate the total cost: $100 base + 8% tax + $15 shipping"
)

# Less ideal: Vague
response = agent.invoke("How much will it cost?")
```

## Performance Considerations

### Token Usage

- **Average tokens per query**: 1,500 - 2,800 tokens
- **Basic agent comparison**: 2-3x more tokens
- **Optimization tip**: Use for complex tasks, not simple lookups

### Speed

- **Average response time**: 8-12 seconds
- **Basic agent comparison**: ~2.4x slower
- **Trade-off**: Speed vs. reasoning depth

### Cost Optimization

```python
# For production: Use efficient models
llm = GoogleLLM(model="gemini-1.5-flash")  # Faster, cheaper

# For research: Use advanced models
llm = GoogleLLM(model="gemini-2.0-flash-thinking-exp-1219")  # Deeper reasoning
```

### When to Use Each Approach

**Use Deep Reasoning Agent:**
- Complex multi-step problems
- High-stakes decisions
- Learning and education
- Debugging and verification
- When transparency is critical

**Use Basic Reasoning Agent:**
- Simple tool calls
- Production APIs with latency constraints
- Cost-sensitive applications
- Straightforward queries

## API Reference

### Class: `Create_Deep_Reasoning_Tool_Calling_Agent`

#### Methods

##### `__init__(llm, verbose=False, show_reasoning=True, prompt=None, memory=None, min_confidence=0.7)`

Initialize the deep reasoning agent.

**Parameters:**
- `llm` (LLM): Language model instance
- `verbose` (bool): Enable detailed logging
- `show_reasoning` (bool): Display reasoning process
- `prompt` (str, optional): Custom system prompt
- `memory` (Memory, optional): Conversation memory
- `min_confidence` (float): Confidence threshold

##### `add_tool(name, description, function)`

Register a tool with the agent.

**Parameters:**
- `name` (str): Tool identifier
- `description` (str): Clear description of what the tool does
- `function` (callable): The function to execute

**Example:**
```python
def search_web(query: str) -> str:
    """Search the web for information."""
    return search_api(query)

agent.add_tool("web_search", "Search the internet", search_web)
```

##### `invoke(query)`

Execute a query with deep reasoning.

**Parameters:**
- `query` (str): The user's question or request

**Returns:**
- `str`: The agent's response

**Example:**
```python
response = agent.invoke("What is 25% of 80?")
```

##### `clear_memory()`

Clear conversation history (if memory is enabled).

**Example:**
```python
agent.clear_memory()
```

## Use Case Examples

### Educational Mathematics

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    prompt="You are a patient math tutor who shows all steps.",
    show_reasoning=True
)

agent.invoke("Solve for x: 2x + 5 = 15")
```

### Financial Planning

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    prompt="You are a financial advisor who explains calculations clearly.",
    min_confidence=0.85
)

agent.invoke("If I save $500/month at 6% annual return, how much in 5 years?")
```

### Scientific Research

```python
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    prompt="You are a research assistant who verifies all calculations.",
    verbose=True,
    show_reasoning=True
)

agent.invoke("Calculate the kinetic energy of a 2kg object moving at 10m/s")
```

## Design Philosophy

This agent embodies:

- **Transparency**: Shows all reasoning steps clearly
- **Thoroughness**: Doesn't skip intermediate steps
- **Self-awareness**: Questions and verifies its own logic
- **Reliability**: Validates results before responding
- **Adaptability**: Recovers gracefully from errors
- **Explainability**: Makes AI decision-making understandable

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? [Open an issue](https://github.com/CodexJitin/Codemni/issues)
2. **Suggest Features**: Have an idea? [Start a discussion](https://github.com/CodexJitin/Codemni/discussions)
3. **Improve Docs**: Help make documentation better

For questions and support, please use [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions).

## Author

**CodexJitin**

- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- LinkedIn: [linkedin.com/in/codexjitin](https://www.linkedin.com/in/codexjitin)
- Email: codexjitin@gmail.com

### About the Developer

Passionate about building production-ready AI tools and frameworks. Creator of Codemni, a comprehensive toolkit for developing AI agents with advanced reasoning capabilities.

## License

This project is licensed under a **Proprietary License**. See the [LICENSE](../../../LICENSE) file for details.

© 2025 CodexJitin. All rights reserved.

## Acknowledgments

- Built with support from the open-source AI community
- Powered by state-of-the-art LLM providers (Google, OpenAI, Anthropic, Groq)
- Inspired by advanced reasoning frameworks and chain-of-thought prompting research

## Support

- **Documentation**: [GitHub Repository](https://github.com/CodexJitin/Codemni)
- **Issues**: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions)

**Part of the Codemni AI Agent Framework** | Built by [CodexJitin](https://github.com/CodexJitin)
