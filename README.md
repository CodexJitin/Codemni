# Codemni

<div align="center">

<img src="https://raw.githubusercontent.com/CodexJitin/Codemni/main/assets/codemni-logo.jpg" alt="Codemni Logo" width="400"/>

**🚀 The Complete AI Agent Framework for Python**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/CodexJitin/Codemni/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-CodexJitin%2FCodemni-181717?logo=github)](https://github.com/CodexJitin/Codemni)

*The most powerful framework for building autonomous AI agents - featuring intelligent tool execution, multi-LLM orchestration, and advanced conversational memory*

[Features](#-features) • [Installation](#-installation) • [Modules](#-modules) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📖 About

**Codemni** is a powerful Python framework for building production-ready AI agents and LLM applications. Unlike simple wrappers, Codemni provides a complete ecosystem with intelligent tool-calling agents, multi-provider LLM integrations, and sophisticated memory systems. Whether you're building chatbots, automation systems, or complex AI workflows, Codemni gives you the foundation to create robust, scalable solutions.

**Why Choose Codemni?**

- 🤖 **Complete Agent Framework**: Not just an LLM wrapper - build agents that can think, decide, and execute tools
- ✨ **Production-Ready**: Battle-tested with built-in error handling, retries, and intelligent fallbacks
- 🎯 **Multi-Provider Support**: Seamlessly switch between OpenAI, Google, Anthropic, Groq, and Ollama
- 🧠 **Advanced Memory**: 4 memory strategies to maintain context and conversation history
- 🔧 **Developer-Friendly**: Intuitive APIs, comprehensive documentation, and consistent interfaces
- 🚀 **Performance-Optimized**: Designed for speed, efficiency, and reliability at scale
- 🛡️ **Enterprise-Grade**: Robust error handling, logging, and production-ready code

---

## 🧩 Modules

### 🤖 Agent Framework - Intelligent Tool-Calling Agents

Build powerful AI agents with varying levels of reasoning capabilities - from fast production agents to deep reasoning systems.

#### [TOOL_CALLING_AGENT](./TOOL_CALLING_AGENT/) - Basic Tool Execution Agent

Simple and efficient AI agent for standard tool-calling tasks.

**Key Features:**
- 🔧 Dynamic tool execution based on LLM decisions
- 💾 Optional conversation memory (4 different strategies)
- 🎨 Custom agent personality/role support
- 📊 Verbose mode for debugging
- 🔌 Multi-LLM support (OpenAI, Google Gemini, Anthropic, Groq, Ollama)
- ⚠️ Designed for standard models (reasoning models like o1, o3 not supported)

**[📚 Full Documentation →](./TOOL_CALLING_AGENT/README.md)**

#### [REASONING_TOOL_CALLING_AGENT](./REASONING_TOOL_CALLING_AGENT/) - Fast Reasoning Agent ⚡

**Class:** `Create_ToolCalling_Agent`

Production-ready agent with basic reasoning capabilities - perfect for speed and cost efficiency.

**Key Features:**
- ⚡ **Fast**: 2.4x faster than deep reasoning (4.63s avg)
- 💰 **Cost-Efficient**: 50-70% lower token usage
- 🧠 **Thinking Display**: Shows reasoning process
- 🔧 **Tool Execution**: Intelligent tool selection
- 💾 **Memory Support**: Full conversation history
- 🎯 **Production-Ready**: Optimized for high-volume APIs

**Best For:** Production APIs, real-time systems, cost-sensitive applications

**[📚 Full Documentation →](./REASONING_TOOL_CALLING_AGENT/README.md)**

#### [DEEP_REASONING_TOOL_CALLING_AGENT](./DEEP_REASONING_TOOL_CALLING_AGENT/) - Advanced Reasoning Agent 🧠

**Class:** `Create_Deep_Reasoning_Tool_Calling_Agent`

Sophisticated agent with deep chain-of-thought reasoning, problem analysis, and self-reflection.

**Key Features:**
- 🧠 **Deep Reasoning**: Comprehensive problem understanding
- 🔍 **Situation Awareness**: Tracks progress dynamically
- 💭 **Chain-of-Thought**: Multi-layered reasoning process
- 🎯 **Self-Reflection**: Confidence scoring (0.0-1.0)
- 🛡️ **Error Recovery**: Strategic alternative approaches
- 📊 **Full Transparency**: See exactly how AI thinks

**Best For:** Complex problems, research, debugging, educational tools

**[📚 Full Documentation →](./DEEP_REASONING_TOOL_CALLING_AGENT/README.md)**

**Comparison:**

| Feature | TOOL_CALLING | REASONING ⚡ | DEEP_REASONING 🧠 |
|---------|--------------|-------------|------------------|
| Speed | Fast | Fastest (4.63s) | Slower (11.11s) |
| Thinking | None | Basic | Deep |
| Cost | Low | Low | High |
| Use Case | Basic tools | Production | Research |

---

### 💾 [Memory Module](./memory/) - Conversation History Management

Flexible conversation memory system for maintaining context in multi-turn interactions.

**Available Memory Types:**
- 📝 **ConversationalBufferMemory** - Store all messages
- 🪟 **ConversationalWindowMemory** - Keep last N exchanges
- 🎫 **ConversationalTokenBufferMemory** - Limit by token count
- 📋 **ConversationalSummaryMemory** - Summarize old conversations

**Key Features:**
- Common API across all memory types
- Easy serialization (save/load)
- Lightweight and efficient
- Integrates seamlessly with ToolCalling Agent

**[📚 Full Memory Documentation →](./memory/README.md)**

---

### 📡 [LLM Module](./llm/) - Large Language Model Wrappers

Production-ready wrappers for popular LLM providers with unified interface.

**Supported Providers:**
- 🔷 Google Gemini (`gemini-pro`, `gemini-2.0-flash-exp`)
- 🟢 OpenAI (`gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`)
- 🟣 Anthropic Claude (`claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`)
- ⚡ Groq (`llama3-70b`, `mixtral-8x7b`)
- 🦙 Ollama (Local models: `llama2`, `mistral`, `codellama`)

**Key Features:**
- Automatic retries with exponential backoff
- Configurable timeouts
- Consistent API across all providers
- Both function and class-based interfaces
- Silent operation (no logging)
- Minimal dependencies

**[📚 Full LLM Documentation →](./llm/README.md)**

---

## 📦 Installation

### Install from PyPI (Recommended)

```bash
# Install the base package
pip install Codemni

# Install with specific LLM providers
pip install Codemni[openai]        # OpenAI support
pip install Codemni[anthropic]     # Anthropic Claude support
pip install Codemni[groq]          # Groq support
pip install Codemni[google]        # Google Gemini support
pip install Codemni[ollama]        # Ollama (local) support

# Install with all LLM providers
pip install Codemni[all]
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/CodexJitin/Codemni.git
cd Codemni

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e .[all]
```

---

## 🚀 Quick Start

### Installation

```bash
pip install Codemni[all]  # Install with all LLM providers
```

### REASONING Agent - Fast Production Agent (Recommended)

```python
from Codemni.REASONING_TOOL_CALLING_AGENT.agent import Create_ToolCalling_Agent
from Codemni.llm.Google_llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-exp",
    api_key="YOUR_API_KEY"  # or set GOOGLE_API_KEY env var
)

# Create reasoning agent (fast & cost-efficient)
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Define a tool
def calculator(expression):
    return str(eval(expression))

# Add tool to agent
agent.add_tool("calculator", "Evaluate mathematical expressions", calculator)

# Use the agent
response = agent.invoke("What is 125 * 48?")
print(response)  # Agent shows reasoning and uses calculator
```

### DEEP REASONING Agent - Advanced Problem Solving

```python
from Codemni.DEEP_REASONING_TOOL_CALLING_AGENT.agent import Create_Deep_Reasoning_Tool_Calling_Agent
from Codemni.llm.Google_llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-thinking-exp-1219",
    api_key="YOUR_API_KEY"
)

# Create deep reasoning agent (for complex problems)
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,
    show_reasoning=True,  # See full reasoning process
    min_confidence=0.7     # Confidence threshold
)

# Add tools
agent.add_tool("calculator", "Evaluate math expressions", calculator)

# Use for complex reasoning
response = agent.invoke(
    "If I have 100 apples and give away 30%, then buy 25 more, how many do I have?"
)
# Shows: Problem Understanding → Current Situation → Deep Reasoning → Tool Decision → Self-Reflection
```

### Basic ToolCalling Agent

```python
from Codemni.TOOL_CALLING_AGENT.agent import Create_ToolCalling_Agent
from Codemni.llm.Google_llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-exp",
    api_key="YOUR_API_KEY"
)

# Create basic agent (no reasoning display)
agent = Create_ToolCalling_Agent(llm=llm, verbose=True)

# Define a tool
def calculator(expression):
    return str(eval(expression))

# Add tool to agent
agent.add_tool("calculator", "Evaluate mathematical expressions", calculator)

# Use the agent
response = agent.invoke("What is 125 * 48?")
print(response)  # Agent uses the calculator tool
```

### Agent with Memory

```python
from Codemni.REASONING_TOOL_CALLING_AGENT.agent import Create_ToolCalling_Agent
from Codemni.llm.Google_llm import GoogleLLM
from Codemni.memory.conversational_buffer_memory import ConversationalBufferMemory

# Initialize LLM and memory
llm = GoogleLLM(model="gemini-2.0-flash-exp", api_key="YOUR_API_KEY")
memory = ConversationalBufferMemory()

# Create agent with memory
agent = Create_ToolCalling_Agent(llm=llm, memory=memory, verbose=True)
agent.add_tool("calculator", "Evaluate math", calculator)

# Multi-turn conversation with context
response1 = agent.invoke("Calculate 50 + 25")  # Returns: 75
response2 = agent.invoke("Now multiply that by 2")  # Returns: 150 (remembers 75!)
```

### LLM Module - Basic Usage

```python
from Codemni.llm import google_llm, openai_llm, anthropic_llm

# Google Gemini
response = google_llm(
    prompt="Explain quantum computing in simple terms",
    model="gemini-pro",
    api_key="your-api-key"  # or set GOOGLE_API_KEY env var
)
print(response)

# OpenAI GPT
response = openai_llm(
    prompt="Write a Python function to calculate fibonacci",
    model="gpt-4",
    temperature=0.7,
    max_tokens=500
)
print(response)

# Anthropic Claude
response = anthropic_llm(
    prompt="Explain the concept of recursion",
    model="claude-3-sonnet-20240229",
    max_tokens=300
)
print(response)
```

### Error Handling

```python
from Codemni.llm import google_llm, GoogleLLMError, GoogleLLMAPIError

try:
    response = google_llm(
        prompt="Hello, world!",
        model="gemini-pro"
    )
    print(response)
except GoogleLLMAPIError as e:
    print(f"API Error: {e}")
except GoogleLLMError as e:
    print(f"General Error: {e}")
```

---

## 🔐 Configuration

### Environment Variables

Set these to avoid hardcoding API keys:

```bash
# Linux/Mac
export GOOGLE_API_KEY="your-google-key"
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GROQ_API_KEY="your-groq-key"
export OLLAMA_BASE_URL="http://localhost:11434"  # Optional

# Windows PowerShell
$env:GOOGLE_API_KEY="your-google-key"
$env:OPENAI_API_KEY="your-openai-key"
```

### Using .env File

```bash
# Install python-dotenv
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()

# Now your environment variables are loaded
from Codemni.llm import google_llm

response = google_llm(prompt="Hello", model="gemini-pro")
```

---

## 🏗️ Project Structure

```
Codemni/
├── 📄 README.md              # This file - Main documentation
├── 📄 LICENSE                # License information
├── 📄 requirements.txt       # Base dependencies
├── 📄 __init__.py            # Package initialization
│
├── 🤖 TOOL_CALLING_AGENT/    # Basic Tool Calling Agent
│   ├── __init__.py
│   ├── README.md             # Agent documentation
│   ├── agent.py              # Main agent implementation
│   └── prompt.py             # Prompt templates
│
├── ⚡ REASONING_TOOL_CALLING_AGENT/  # Fast Reasoning Agent
│   ├── __init__.py
│   ├── README.md             # Reasoning agent documentation
│   ├── agent.py              # Reasoning agent with thinking
│   └── prompt.py             # Reasoning prompt templates
│
├── 🧠 DEEP_REASONING_TOOL_CALLING_AGENT/  # Deep Reasoning Agent
│   ├── __init__.py
│   ├── README.md             # Deep reasoning documentation
│   ├── agent.py              # Advanced reasoning implementation
│   └── prompt.py             # Deep reasoning prompts
│
├── 💾 memory/                # Memory Module
│   ├── __init__.py
│   ├── README.md             # Memory documentation
│   ├── conversational_buffer_memory.py
│   ├── conversational_window_memory.py
│   ├── conversational_token_buffer_memory.py
│   └── conversational_summary_memory.py
│
├── 📁 llm/                   # LLM Module
│   ├── __init__.py
│   ├── README.md             # LLM module documentation
│   ├── Google_llm.py         # Google Gemini wrapper
│   ├── OpenAI_llm.py         # OpenAI wrapper
│   ├── Anthropic_llm.py      # Anthropic wrapper
│   ├── Groq_llm.py           # Groq wrapper
│   └── Ollama_llm.py         # Ollama wrapper
│
├── 📁 core/                  # Core utilities
│   └── adapter.py            # Tool execution adapter
│
└── 📁 assets/                # Assets and media
    └── codemni-logo.jpg
```

---

## 📚 Documentation

### Module Documentation

- **[TOOL_CALLING_AGENT](./TOOL_CALLING_AGENT/README.md)** - Basic tool calling agent
  - Simple tool execution without reasoning display
  - Memory integration guide
  - Tool definition best practices
  
- **[REASONING_TOOL_CALLING_AGENT](./REASONING_TOOL_CALLING_AGENT/README.md)** - Fast reasoning agent ⚡
  - Complete API reference
  - Basic reasoning with thinking display
  - Production-ready performance
  - Memory integration
  - Troubleshooting and examples

- **[DEEP_REASONING_TOOL_CALLING_AGENT](./DEEP_REASONING_TOOL_CALLING_AGENT/README.md)** - Advanced reasoning agent 🧠
  - Deep chain-of-thought reasoning
  - Problem understanding and situation awareness
  - Self-reflection and confidence scoring
  - Error recovery strategies
  - Complex problem-solving examples
  
- **[Memory Module](./memory/README.md)** - Conversation memory guide
  - Memory type comparison
  - Usage examples for each type
  - Serialization and persistence
  - Integration with agents

- **[LLM Module](./llm/README.md)** - Comprehensive guide to LLM wrappers
  - API reference for all providers
  - Advanced usage examples
  - Exception handling guide
  - Provider-specific notes

---

## ✨ Features by Module

### Agent Framework

| Feature | TOOL_CALLING | REASONING ⚡ | DEEP_REASONING 🧠 |
|---------|--------------|-------------|------------------|
| 🤖 **Multi-LLM Support** | ✅ | ✅ | ✅ |
| 🔧 **Tool Execution** | ✅ | ✅ | ✅ |
| 💾 **Memory Integration** | ✅ | ✅ | ✅ |
| 🧠 **Thinking Display** | ❌ | ✅ Basic | ✅ Deep |
| 📊 **Problem Analysis** | ❌ | ❌ | ✅ Comprehensive |
| 🎯 **Situation Awareness** | ❌ | ❌ | ✅ Dynamic |
| 💭 **Chain-of-Thought** | ❌ | ⚠️ Surface | ✅ Multi-layer |
| 🔍 **Self-Reflection** | ❌ | ❌ | ✅ With confidence |
| 🛡️ **Error Recovery** | ⚠️ Basic | ⚠️ Basic | ✅ Strategic |
| ⚡ **Speed** | Fast | Fastest | Slower |
| 💰 **Cost** | Low | Low | High |
| 🎯 **Best For** | Simple tools | Production | Research |

### ToolCalling Agent Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-LLM Support** | Works with OpenAI, Google Gemini, Anthropic, Groq, Ollama |
| 🔧 **Dynamic Tools** | Automatically selects and executes appropriate tools |
| 💾 **Optional Memory** | 4 memory strategies for conversation context |
| 🎨 **Custom Prompts** | Customize agent personality and role |
| 📊 **Verbose Mode** | Detailed logging for debugging |
| ⚠️ **Standard Models** | Optimized for instruction-following models (not reasoning models) |

### Memory Module

| Feature | Description |
|---------|-------------|
| 📝 **Buffer Memory** | Store all conversation messages |
| 🪟 **Window Memory** | Keep only recent N exchanges |
| 🎫 **Token Buffer** | Limit memory by token count |
| 📋 **Summary Memory** | Summarize old conversations |
| 💾 **Serialization** | Save/load conversation history |
| 🔌 **Easy Integration** | Works seamlessly with agents |

### LLM Module

| Feature | Description |
|---------|-------------|
| 🔄 **Auto Retry** | Exponential backoff for transient failures |
| ⏱️ **Timeouts** | Configurable request timeouts (30-60s) |
| 🛡️ **Error Handling** | Clear exception hierarchy per provider |
| 🔇 **Silent Mode** | No logging - clean operation |
| 📦 **Minimal Deps** | Install only what you need |
| 🎯 **Unified API** | Same interface across all providers |
| ✅ **Validation** | Input validation and defensive coding |
| 🔧 **Dual Interface** | Both function and class-based APIs |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Add tests for new features
- Update documentation
- Keep dependencies minimal
- Maintain backward compatibility

---

## 📋 Requirements

- Python 3.8 or higher
- Optional dependencies (install as needed):
  - `openai>=1.0.0` - For OpenAI support
  - `anthropic>=0.18.0` - For Anthropic support
  - `groq>=0.4.0` - For Groq support
  - `google-generativeai>=0.3.0` - For Google Gemini support
  - `ollama>=0.1.0` - For Ollama support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**CodexJitin**

- GitHub: [@CodexJitin](https://github.com/CodexJitin)
- Repository: [Codemni](https://github.com/CodexJitin/Codemni)

---

## 🔖 Version

**Current Version: 1.2.0**

### Changelog

#### v1.2.0 (2025-10-25)

- 🎉 **NEW**: Added REASONING_TOOL_CALLING_AGENT - Fast reasoning agent with thinking display
- 🧠 **NEW**: Added DEEP_REASONING_TOOL_CALLING_AGENT - Advanced reasoning with deep chain-of-thought
- 📊 **Performance**: Comprehensive agent comparison (Basic vs Reasoning vs Deep Reasoning)
- 🔍 **Features**: Problem understanding, situation awareness, self-reflection, confidence scoring
- 🛡️ **Error Recovery**: Strategic error recovery in deep reasoning agent
- 📚 **Documentation**: Complete README files for all agent types
- ⚡ **Optimization**: gRPC warning suppression in all LLM wrappers

#### v1.1.0 (2025-10-24)

- 🎉 Added ToolCalling Agent module
- 💾 Added Memory module with 4 memory strategies
- 🔧 LLM module now supports both function and class-based interfaces
- 📚 Comprehensive documentation for all modules
- ⚠️ Added warnings about reasoning model compatibility

#### v1.0.0 (2025-10-23)

- 🎉 Initial release
- ✅ LLM module with 5 provider support
- ✅ Production-ready error handling
- ✅ Comprehensive documentation

---

## 🌟 Show Your Support

If you find Codemni useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🔀 Contributing code

---

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/CodexJitin/Codemni/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/CodexJitin/Codemni/discussions)

---

<div align="center">

**Made with ❤️ by CodexJitin**

*Empowering developers to build better AI applications*

</div>
