# Memory Module

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-green.svg)](https://github.com/CodexJitin/Codemni)

Memory implementations for AI agents to maintain conversation history and context.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Available Memory Types](#available-memory-types)
- [Common API](#common-api)
- [Integration with Agents](#integration-with-agents)
- [Comparison](#comparison)
- [Best Practices](#best-practices)
- [Author](#author)
- [License](#license)

## Overview

The Memory Module provides four different strategies for managing conversation history in AI agents. Each memory type is optimized for specific use cases, from simple buffering to token-aware management and intelligent summarization.

## Installation

### Prerequisites

- Python 3.8 or higher

### Install via PyPI

```bash
pip install Codemni
```

> **Note:** Codemni is available exclusively through PyPI. For documentation and support, visit the [GitHub repository](https://github.com/CodexJitin/Codemni).

## Available Memory Types

### 1. ConversationalBufferMemory

Simple buffer that stores all conversation history.

**Characteristics:**
- Stores every message without limit
- Complete conversation context
- Can grow very large
- **Best for:** Short conversations

```python
from Codemni.memory import ConversationalBufferMemory

memory = ConversationalBufferMemory()
memory.add_user_message("Hello!")
memory.add_ai_message("Hi! How can I help?")

print(memory.get_history())
# [{"role": "user", "content": "Hello!"}, ...]
```

### 2. ConversationalWindowMemory

Stores only the last N messages.

**Characteristics:**
- Fixed memory size
- Maintains recent context
- Loses older messages
- **Best for:** Long conversations where recent context matters most

```python
from Codemni.memory import ConversationalWindowMemory

memory = ConversationalWindowMemory(window_size=10)
memory.add_user_message("Message 1")
memory.add_ai_message("Response 1")
# ... after 10 messages, oldest are removed

print(len(memory))  # Always ≤ 10
```

### 3. ConversationalSummaryMemory

Summarizes old messages to save tokens.

**Characteristics:**
- Maintains context with fewer tokens
- Suitable for very long conversations
- Requires LLM for summarization
- **Best for:** Long conversations with token limits

```python
from Codemni.memory import ConversationalSummaryMemory
from Codemni.llm import OpenAILLM

llm = OpenAILLM(model="gpt-3.5-turbo", api_key="key")
memory = ConversationalSummaryMemory(llm=llm, buffer_size=5)

# After buffer_size messages, old messages get summarized
memory.add_user_message("...")
```

### 4. ConversationalTokenBufferMemory

Limits memory based on token count.

**Characteristics:**
- Precise token management
- Prevents API token limit errors
- Uses token estimation
- **Best for:** Managing API costs and limits

```python
from Codemni.memory import ConversationalTokenBufferMemory

memory = ConversationalTokenBufferMemory(max_tokens=2000)
memory.add_user_message("Hello!")

print(memory.get_token_count())  # ~50
print(memory.get_available_tokens())  # ~1950
```

## Common API

All memory classes share a common interface:

### Adding Messages
```python
memory.add_user_message("User's message")
memory.add_ai_message("AI's response")
memory.add_message("system", "System message")
```

### Retrieving History
```python
# As list of dicts
history = memory.get_history()

# As formatted string
history_str = memory.get_history_as_string()

# As context for prompts
context = memory.get_context()
```

### Management
```python
# Get count
count = memory.get_message_count()
# or
count = len(memory)

# Clear memory
memory.clear()
```

### Persistence
```python
# Save to dict
state = memory.save_to_dict()

# Load from dict
memory.load_from_dict(state)
```

## Integration with Agents

### Example: Adding Memory to ToolCalling Agent

```python
from Codemni.llm import GoogleLLM
from Codemni.Agents import Create_ToolCalling_Agent
from Codemni.memory import ConversationalWindowMemory

# Initialize components
llm = GoogleLLM(model="gemini-1.5-pro", api_key="key")
memory = ConversationalWindowMemory(window_size=10)
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Add tools
agent.add_tool("calculator", "Calculate", lambda x: eval(x))

# Use with memory
def chat_with_memory(query: str):
    # Add user message to memory
    memory.add_user_message(query)
    
    # Get conversation context
    context = memory.get_context()
    
    # Create prompt with context
    full_query = f"{context}\n\nNew query: {query}" if context else query
    
    # Get response
    response = agent.invoke(full_query)
    
    # Add response to memory
    memory.add_ai_message(response)
    
    return response

# Use it
response1 = chat_with_memory("My name is John")
response2 = chat_with_memory("What's my name?")  # Has context!
```

## Comparison

| Memory Type | Max Messages | Token Aware | Summarizes | Use Case |
|------------|--------------|-------------|------------|----------|
| **Buffer** | Unlimited | No | No | Short conversations |
| **Window** | Fixed N | No | No | Recent context focus |
| **Summary** | Buffer + Summary | Partial | Yes | Very long conversations |
| **TokenBuffer** | Dynamic | Yes | No | Token budget management |

## Best Practices

### 1. Choose the Right Memory

- Short chats → BufferMemory
- Long chats → WindowMemory or SummaryMemory
- Token limits → TokenBufferMemory

### 2. Consider Costs

- SummaryMemory requires extra LLM calls for summarization
- BufferMemory sends all history (more tokens per request)

### 3. Test Your Limits

- Monitor token usage
- Adjust window/buffer sizes based on your use case

### 4. Save State

- Use save_to_dict/load_from_dict for persistence
- Store to file, database, or session storage

## Advanced Usage

### Custom Token Estimation

```python
class CustomTokenMemory(ConversationalTokenBufferMemory):
    def _estimate_tokens(self, text: str) -> int:
        # Use tiktoken or custom logic
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
```

### Hybrid Memory

```python
# Combine window and summary
from Codemni.memory import ConversationalSummaryMemory

memory = ConversationalSummaryMemory(
    llm=llm,
    buffer_size=5  # Keep last 5 in detail, summarize rest
)
```

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
- Designed for seamless integration with AI agents
- Optimized for production use cases

## Support

- **Documentation**: [GitHub Repository](https://github.com/CodexJitin/Codemni)
- **Issues**: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions)

**Part of the Codemni AI Agent Framework** | Built by [CodexJitin](https://github.com/CodexJitin)
