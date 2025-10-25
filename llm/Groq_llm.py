"""Small, robust wrapper around Groq's API client.

This module provides a single function, ``groq_llm``, which will
call Groq's API with input validation, retries, timeouts and
clear exceptions suitable for production integration.

Notes:
- No logging is performed by this module (per project requirement).
- Supports Groq's fast inference models (llama3, mixtral, gemma, etc.).

Example usage:
    >>> from Codemni.llm import groq_llm, GroqLLMError
    >>> 
    >>> try:
    ...     response = groq_llm(
    ...         prompt="Explain Python in one sentence",
    ...         model="llama3-70b-8192",
    ...         api_key="your-api-key-here"  # or set GROQ_API_KEY env var
    ...     )
    ...     print(response)
    ... except GroqLLMError as e:
    ...     print(f"Error: {e}")
"""

from typing import Optional, Any
import os
import time

# Import the Groq client at module level to reduce import overhead
try:
    from groq import Groq
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False
    Groq = None  # type: ignore


class GroqLLMError(Exception):
    """Base exception for errors raised by this module."""


class GroqLLMImportError(GroqLLMError):
    """Raised when the Groq client library cannot be imported."""


class GroqLLMAPIError(GroqLLMError):
    """Raised when the API request fails after retries."""


class GroqLLMResponseError(GroqLLMError):
    """Raised when the response from the API cannot be interpreted."""


def groq_llm(
    prompt: str,
    model: str,
    api_key: Optional[str] = None,
    *,
    max_retries: int = 3,
    timeout: Optional[float] = 30.0,
    backoff_factor: float = 0.5,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    """Call a Groq model and return the generated text.

    Args:
        prompt: The prompt / input text to send to the model. Must be non-empty.
        model: Model identifier (e.g. "llama3-70b-8192", "mixtral-8x7b-32768").
        api_key: API key to use. If omitted, will try GROQ_API_KEY env var.
        max_retries: Number of attempts to make on transient failures.
        timeout: Optional timeout (seconds) to pass to the underlying client.
        backoff_factor: Base factor for exponential backoff between retries.
        temperature: Sampling temperature (0.0 to 2.0, optional).
        max_tokens: Maximum tokens in response (optional).

    Returns:
        The generated text from the model.

    Raises:
        ValueError: If required arguments are missing or invalid.
        GroqLLMImportError: If the Groq client is not installed.
        GroqLLMAPIError: If all retry attempts fail.
        GroqLLMResponseError: If a response is returned but contains no text.
    """

    # Basic validation
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")
    if not isinstance(max_retries, int) or max_retries < 1:
        raise ValueError("max_retries must be an integer >= 1")
    if temperature is not None and not (0.0 <= temperature <= 2.0):
        raise ValueError("temperature must be between 0.0 and 2.0")
    if max_tokens is not None and max_tokens <= 0:
        raise ValueError("max_tokens must be positive")

    api_key = api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise GroqLLMImportError(
            "No API key provided and environment variable GROQ_API_KEY is not set"
        )

    # Check if Groq client is available
    if not _GROQ_AVAILABLE or Groq is None:
        raise GroqLLMImportError(
            "Groq package not installed. Install with: pip install groq"
        )

    # Initialize client
    try:
        client = Groq(api_key=api_key, timeout=timeout)
    except Exception as exc:
        raise GroqLLMImportError(
            "Failed to initialize Groq client"
        ) from exc

    last_exc: Optional[BaseException] = None

    for attempt in range(1, max_retries + 1):
        try:
            # Prepare kwargs
            kwargs: dict = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            if temperature is not None:
                kwargs["temperature"] = temperature
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens

            # Make API request
            response = client.chat.completions.create(**kwargs)

            # Extract text
            if not response.choices:
                raise GroqLLMResponseError("No choices in response")
            
            text = response.choices[0].message.content
            if not text or not isinstance(text, str):
                raise GroqLLMResponseError("No valid text content in response")

            return text.strip()

        except GroqLLMError:
            raise
        except Exception as exc:
            last_exc = exc
            if attempt == max_retries:
                raise GroqLLMAPIError(
                    f"Groq LLM request failed after {max_retries} attempts: {exc}"
                ) from exc

            # Backoff before next retry
            sleep_for = backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_for)

    raise GroqLLMAPIError("Groq LLM request failed") from last_exc


__all__ = ["groq_llm", "GroqLLMError", "GroqLLMAPIError"]
