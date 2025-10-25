"""Small, robust wrapper around Anthropic's Claude API client.

This module provides a single function, ``anthropic_llm``, which will
call Anthropic's Claude API with input validation, retries, timeouts and
clear exceptions suitable for production integration.

Notes:
- No logging is performed by this module (per project requirement).
- Supports Claude 3 models (opus, sonnet, haiku) and legacy models.

Example usage:
    >>> from Codemni.llm import anthropic_llm, AnthropicLLMError
    >>> 
    >>> try:
    ...     response = anthropic_llm(
    ...         prompt="Explain Python in one sentence",
    ...         model="claude-3-opus-20240229",
    ...         api_key="your-api-key-here"  # or set ANTHROPIC_API_KEY env var
    ...     )
    ...     print(response)
    ... except AnthropicLLMError as e:
    ...     print(f"Error: {e}")
"""

from typing import Optional, Any
import os
import time

# Import the Anthropic client at module level to reduce import overhead
try:
    from anthropic import Anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False
    Anthropic = None  # type: ignore


class AnthropicLLMError(Exception):
    """Base exception for errors raised by this module."""


class AnthropicLLMImportError(AnthropicLLMError):
    """Raised when the Anthropic client library cannot be imported."""


class AnthropicLLMAPIError(AnthropicLLMError):
    """Raised when the API request fails after retries."""


class AnthropicLLMResponseError(AnthropicLLMError):
    """Raised when the response from the API cannot be interpreted."""


def anthropic_llm(
    prompt: str,
    model: str,
    api_key: Optional[str] = None,
    *,
    max_retries: int = 3,
    timeout: Optional[float] = 30.0,
    backoff_factor: float = 0.5,
    temperature: Optional[float] = None,
    max_tokens: int = 4096,
) -> str:
    """Call an Anthropic Claude model and return the generated text.

    Args:
        prompt: The prompt / input text to send to the model. Must be non-empty.
        model: Model identifier (e.g. "claude-3-opus-20240229", "claude-3-sonnet-20240229").
        api_key: API key to use. If omitted, will try ANTHROPIC_API_KEY env var.
        max_retries: Number of attempts to make on transient failures.
        timeout: Optional timeout (seconds) to pass to the underlying client.
        backoff_factor: Base factor for exponential backoff between retries.
        temperature: Sampling temperature (0.0 to 1.0, optional).
        max_tokens: Maximum tokens in response (default: 4096, required by Anthropic).

    Returns:
        The generated text from the model.

    Raises:
        ValueError: If required arguments are missing or invalid.
        AnthropicLLMImportError: If the Anthropic client is not installed.
        AnthropicLLMAPIError: If all retry attempts fail.
        AnthropicLLMResponseError: If a response is returned but contains no text.
    """

    # Basic validation
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")
    if not isinstance(max_retries, int) or max_retries < 1:
        raise ValueError("max_retries must be an integer >= 1")
    if temperature is not None and not (0.0 <= temperature <= 1.0):
        raise ValueError("temperature must be between 0.0 and 1.0")
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise AnthropicLLMImportError(
            "No API key provided and environment variable ANTHROPIC_API_KEY is not set"
        )

    # Check if Anthropic client is available
    if not _ANTHROPIC_AVAILABLE or Anthropic is None:
        raise AnthropicLLMImportError(
            "Anthropic package not installed. Install with: pip install anthropic"
        )

    # Initialize client
    try:
        client = Anthropic(api_key=api_key, timeout=timeout)
    except Exception as exc:
        raise AnthropicLLMImportError(
            "Failed to initialize Anthropic client"
        ) from exc

    last_exc: Optional[BaseException] = None

    for attempt in range(1, max_retries + 1):
        try:
            # Prepare kwargs
            kwargs: dict = {
                "model": model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            }
            if temperature is not None:
                kwargs["temperature"] = temperature

            # Make API request
            response = client.messages.create(**kwargs)

            # Extract text
            if not response.content:
                raise AnthropicLLMResponseError("No content in response")
            
            # Concatenate all text blocks
            text_parts = []
            for block in response.content:
                if hasattr(block, 'text'):
                    text_parts.append(block.text)
            
            if not text_parts:
                raise AnthropicLLMResponseError("No text content in response")

            return "".join(text_parts).strip()

        except AnthropicLLMError:
            raise
        except Exception as exc:
            last_exc = exc
            if attempt == max_retries:
                raise AnthropicLLMAPIError(
                    f"Anthropic LLM request failed after {max_retries} attempts: {exc}"
                ) from exc

            # Backoff before next retry
            sleep_for = backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_for)

    raise AnthropicLLMAPIError("Anthropic LLM request failed") from last_exc


class AnthropicLLM:
    """
    Class-based wrapper for Anthropic Claude LLM with generate_response method.
    
    This class wraps the anthropic_llm function to provide a stateful interface
    suitable for use with agents and other systems that expect an object
    with a generate_response(prompt) method.
    
    Example:
        >>> llm = AnthropicLLM(model="claude-3-sonnet-20240229", api_key="your-key")
        >>> response = llm.generate_response("What is Python?")
        >>> print(response)
    """
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        *,
        max_retries: int = 3,
        timeout: Optional[float] = 30.0,
        backoff_factor: float = 0.5,
        temperature: Optional[float] = None,
        max_tokens: int = 4096,
    ):
        """
        Initialize Anthropic Claude LLM wrapper.
        
        Args:
            model: Model identifier (e.g. "claude-3-opus-20240229", "claude-3-sonnet-20240229")
            api_key: API key (optional if ANTHROPIC_API_KEY env var is set)
            max_retries: Number of retry attempts on failure
            timeout: Request timeout in seconds
            backoff_factor: Exponential backoff factor for retries
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response (required by Anthropic)
        """
        self.model = model
        self.api_key = api_key
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the Anthropic Claude model.
        
        Args:
            prompt: The input prompt text
            
        Returns:
            Generated response text
            
        Raises:
            ValueError: If prompt is invalid
            AnthropicLLMImportError: If Anthropic client not available
            AnthropicLLMAPIError: If API request fails
            AnthropicLLMResponseError: If response is invalid
        """
        return anthropic_llm(
            prompt=prompt,
            model=self.model,
            api_key=self.api_key,
            max_retries=self.max_retries,
            timeout=self.timeout,
            backoff_factor=self.backoff_factor,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )


__all__ = [
    "anthropic_llm",
    "AnthropicLLM",
    "AnthropicLLMError",
    "AnthropicLLMAPIError",
    "AnthropicLLMImportError",
    "AnthropicLLMResponseError",
]
