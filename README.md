# Codemni

<div align="center">

<img src="./assets/codemni-logo.png" alt="Codemni Logo" width="400"/>

**🚀 Production-Ready Python Toolkit for AI Development**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-CodexJitin%2FCodemni-181717?logo=github)](https://github.com/CodexJitin/Codemni)

*A modular collection of production-ready tools and utilities for modern AI-powered Python applications*

[Features](#-features) • [Installation](#-installation) • [Modules](#-modules) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📖 About

**Codemni** is a comprehensive Python toolkit designed to accelerate AI development with robust, production-ready components. Built with a focus on:

- ✨ **Production-Ready**: Battle-tested with built-in error handling, retries, and timeouts
- 🎯 **Modular Design**: Use only what you need, keep dependencies minimal
- 🔧 **Developer-Friendly**: Consistent APIs, clear documentation, and intuitive interfaces
- 🚀 **Performance**: Optimized for speed and reliability
- 🛡️ **Robust**: Comprehensive exception handling and defensive coding

---

## 🧩 Modules

### 📡 [LLM Module](./llm/) - Large Language Model Wrappers

Production-ready wrappers for popular LLM providers with unified interface.

**Supported Providers:**
- 🔷 Google Gemini (`gemini-pro`, `gemini-1.5-pro`)
- 🟢 OpenAI (`gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`)
- 🟣 Anthropic Claude (`claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`)
- ⚡ Groq (`llama3-70b`, `mixtral-8x7b`)
- 🦙 Ollama (Local models: `llama2`, `mistral`, `codellama`)

**Key Features:**
- Automatic retries with exponential backoff
- Configurable timeouts
- Consistent API across all providers
- Silent operation (no logging)
- Minimal dependencies

**[📚 Full LLM Documentation →](./llm/README.md)**

---

## 📦 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/CodexJitin/Codemni.git
cd Codemni

# Install the package
pip install -e .
```

### Direct from GitHub

```bash
pip install git+https://github.com/CodexJitin/Codemni.git
```

### Install with Optional Dependencies

```bash
# Install with specific LLM providers
pip install -e .[openai]        # OpenAI support
pip install -e .[anthropic]     # Anthropic Claude support
pip install -e .[groq]          # Groq support
pip install -e .[google]        # Google Gemini support
pip install -e .[ollama]        # Ollama (local) support

# Install with all LLM providers
pip install -e .[all]
```

---

## 🚀 Quick Start

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
├── 📄 setup.py               # Package configuration
├── 📄 requirements.txt       # Base dependencies
├── 📄 __init__.py            # Package initialization
├── 📄 example_usage.py       # Quick examples
│
├── 📁 llm/                   # LLM Module
│   ├── __init__.py
│   ├── README.md             # LLM module documentation
│   ├── Google_llm.py         # Google Gemini wrapper
│   ├── OpenAI_llm.py         # OpenAI wrapper
│   ├── Anthropic_llm.py      # Anthropic wrapper
│   ├── Groq_llm.py           # Groq wrapper
│   ├── Ollama_llm.py         # Ollama wrapper
│   └── examples.py           # Usage examples
│
└── 📁 [Future Modules]       # Coming soon...
    └── ...
```

---

## 📚 Documentation

### Module Documentation

- **[LLM Module](./llm/README.md)** - Comprehensive guide to LLM wrappers
  - API reference for all providers
  - Advanced usage examples
  - Exception handling guide
  - Provider-specific notes

### Examples

- `example_usage.py` - Quick start examples for all modules
- `llm/examples.py` - Detailed LLM provider examples

---

## ✨ Features by Module

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

**Current Version: 1.0.0**

### Changelog

#### v1.0.0 (2025-10-24)
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
