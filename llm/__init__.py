"""
Initialize Codemni LLM package

Production-ready LLM wrappers with robust error handling, retries, and no logging.
Supports: Google Gemini, OpenAI, Anthropic Claude, Groq, and Ollama.

Each LLM module provides two interfaces:
1. Function-based: For one-off calls with all parameters
   Example: openai_llm(prompt="Hello", model="gpt-4", api_key="key")

2. Class-based: For stateful usage with agents (NEW!)
   Example: 
   llm = OpenAILLM(model="gpt-4", api_key="key")
   response = llm.generate_response("Hello")

Available Classes:
- OpenAILLM: For GPT-4, GPT-3.5-turbo, etc.
- GoogleLLM: For Gemini models (gemini-1.5-pro, gemini-pro)
- AnthropicLLM: For Claude models (claude-3-opus, claude-3-sonnet)
- GroqLLM: For Groq models (llama3-70b-8192, mixtral-8x7b-32768)
- OllamaLLM: For local Ollama models (llama2, mistral, codellama)

Available Functions:
- openai_llm(): Call OpenAI models
- google_llm(): Call Google Gemini models
- anthropic_llm(): Call Anthropic Claude models
- groq_llm(): Call Groq models
- ollama_llm(): Call local Ollama models
"""

from .Google_llm import (
    google_llm,
    GoogleLLM,
    GoogleLLMError,
    GoogleLLMAPIError,
    GoogleLLMImportError,
    GoogleLLMResponseError,
)

from .OpenAI_llm import (
    openai_llm,
    OpenAILLM,
    OpenAILLMError,
    OpenAILLMAPIError,
    OpenAILLMImportError,
    OpenAILLMResponseError,
)

from .Anthropic_llm import (
    anthropic_llm,
    AnthropicLLM,
    AnthropicLLMError,
    AnthropicLLMAPIError,
    AnthropicLLMImportError,
    AnthropicLLMResponseError,
)

from .Groq_llm import (
    groq_llm,
    GroqLLM,
    GroqLLMError,
    GroqLLMAPIError,
    GroqLLMImportError,
    GroqLLMResponseError,
)

from .Ollama_llm import (
    ollama_llm,
    OllamaLLM,
    OllamaLLMError,
    OllamaLLMAPIError,
    OllamaLLMImportError,
    OllamaLLMResponseError,
)

__version__ = "1.2.2"
__author__ = "CodexJitin"
__all__ = [
    # Google Gemini
    "google_llm",
    "GoogleLLM",
    "GoogleLLMError",
    "GoogleLLMAPIError",
    "GoogleLLMImportError",
    "GoogleLLMResponseError",
    # OpenAI
    "openai_llm",
    "OpenAILLM",
    "OpenAILLMError",
    "OpenAILLMAPIError",
    "OpenAILLMImportError",
    "OpenAILLMResponseError",
    # Anthropic Claude
    "anthropic_llm",
    "AnthropicLLM",
    "AnthropicLLMError",
    "AnthropicLLMAPIError",
    "AnthropicLLMImportError",
    "AnthropicLLMResponseError",
    # Groq
    "groq_llm",
    "GroqLLM",
    "GroqLLMError",
    "GroqLLMAPIError",
    "GroqLLMImportError",
    "GroqLLMResponseError",
    # Ollama
    "ollama_llm",
    "OllamaLLM",
    "OllamaLLMError",
    "OllamaLLMAPIError",
    "OllamaLLMImportError",
    "OllamaLLMResponseError",
]
