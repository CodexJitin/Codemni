"""
Initialize codemni_LLM package

Production-ready LLM wrappers with robust error handling, retries, and no logging.
Supports: Google Gemini, OpenAI, Anthropic Claude, Groq, and Ollama.
"""

from .Google_llm import (
    google_llm,
    GoogleLLMError,
    GoogleLLMAPIError,
    GoogleLLMImportError,
    GoogleLLMResponseError,
)

from .OpenAI_llm import (
    openai_llm,
    OpenAILLMError,
    OpenAILLMAPIError,
    OpenAILLMImportError,
    OpenAILLMResponseError,
)

from .Anthropic_llm import (
    anthropic_llm,
    AnthropicLLMError,
    AnthropicLLMAPIError,
    AnthropicLLMImportError,
    AnthropicLLMResponseError,
)

from .Groq_llm import (
    groq_llm,
    GroqLLMError,
    GroqLLMAPIError,
    GroqLLMImportError,
    GroqLLMResponseError,
)

from .Ollama_llm import (
    ollama_llm,
    OllamaLLMError,
    OllamaLLMAPIError,
    OllamaLLMImportError,
    OllamaLLMResponseError,
)

__version__ = "1.0.0"
__author__ = "codexJitin"
__all__ = [
    # Google Gemini
    "google_llm",
    "GoogleLLMError",
    "GoogleLLMAPIError",
    "GoogleLLMImportError",
    "GoogleLLMResponseError",
    # OpenAI
    "openai_llm",
    "OpenAILLMError",
    "OpenAILLMAPIError",
    "OpenAILLMImportError",
    "OpenAILLMResponseError",
    # Anthropic Claude
    "anthropic_llm",
    "AnthropicLLMError",
    "AnthropicLLMAPIError",
    "AnthropicLLMImportError",
    "AnthropicLLMResponseError",
    # Groq
    "groq_llm",
    "GroqLLMError",
    "GroqLLMAPIError",
    "GroqLLMImportError",
    "GroqLLMResponseError",
    # Ollama
    "ollama_llm",
    "OllamaLLMError",
    "OllamaLLMAPIError",
    "OllamaLLMImportError",
    "OllamaLLMResponseError",
]
