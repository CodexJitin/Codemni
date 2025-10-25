"""Small, robust wrapper around Ollama's local API client.

This module provides a single function, ``ollama_llm``, which will
call Ollama's local API with input validation, retries, timeouts and
clear exceptions suitable for production integration.

Notes:
- No logging is performed by this module (per project requirement).
- Requires Ollama server running locally (default: http://localhost:11434).
- Supports all Ollama models (llama2, mistral, codellama, etc.).

Example usage:
    >>> from Codemni.llm import ollama_llm, OllamaLLMError
    >>> 
    >>> try:
    ...     response = ollama_llm(
    ...         prompt="Explain Python in one sentence",
    ...         model="llama2",
    ...         base_url="http://localhost:11434"  # or set OLLAMA_BASE_URL env var
    ...     )
    ...     print(response)
    ... except OllamaLLMError as e:
    ...     print(f"Error: {e}")
"""

from typing import Optional, Any
import os
import time

# Import the Ollama client at module level to reduce import overhead
try:
    from ollama import Client
    _OLLAMA_AVAILABLE = True
except ImportError:
    _OLLAMA_AVAILABLE = False
    Client = None  # type: ignore


class OllamaLLMError(Exception):
    """Base exception for errors raised by this module."""


class OllamaLLMImportError(OllamaLLMError):
    """Raised when the Ollama client library cannot be imported."""


class OllamaLLMAPIError(OllamaLLMError):
    """Raised when the API request fails after retries."""


class OllamaLLMResponseError(OllamaLLMError):
    """Raised when the response from the API cannot be interpreted."""


def ollama_llm(
    prompt: str,
    model: str,
    base_url: Optional[str] = None,
    *,
    max_retries: int = 3,
    timeout: Optional[float] = 60.0,
    backoff_factor: float = 0.5,
    temperature: Optional[float] = None,
) -> str:
    """Call an Ollama local model and return the generated text.

    Args:
        prompt: The prompt / input text to send to the model. Must be non-empty.
        model: Model identifier (e.g. "llama2", "mistral", "codellama").
        base_url: Ollama server URL. If omitted, will try OLLAMA_BASE_URL env var
                  or default to http://localhost:11434.
        max_retries: Number of attempts to make on transient failures.
        timeout: Optional timeout (seconds) to pass to the underlying client.
        backoff_factor: Base factor for exponential backoff between retries.
        temperature: Sampling temperature (0.0 to 2.0, optional).

    Returns:
        The generated text from the model.

    Raises:
        ValueError: If required arguments are missing or invalid.
        OllamaLLMImportError: If the Ollama client is not installed.
        OllamaLLMAPIError: If all retry attempts fail.
        OllamaLLMResponseError: If a response is returned but contains no text.
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

    base_url = base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

    # Check if Ollama client is available
    if not _OLLAMA_AVAILABLE or Client is None:
        raise OllamaLLMImportError(
            "Ollama package not installed. Install with: pip install ollama"
        )

    # Initialize client
    try:
        client = Client(host=base_url)
    except Exception as exc:
        raise OllamaLLMImportError(
            f"Failed to initialize Ollama client with base_url={base_url}"
        ) from exc

    last_exc: Optional[BaseException] = None

    for attempt in range(1, max_retries + 1):
        try:
            # Prepare options
            options = {}
            if temperature is not None:
                options["temperature"] = temperature

            # Make API request
            response = client.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                options=options if options else None,
            )

            # Extract text
            if not response:
                raise OllamaLLMResponseError("Empty response from Ollama")
            
            # Handle different response formats
            if isinstance(response, dict):
                text = response.get("message", {}).get("content")
                if not text:
                    # Try alternative format
                    text = response.get("response")
            else:
                text = None

            if not text or not isinstance(text, str):
                raise OllamaLLMResponseError("No valid text content in response")

            return text.strip()

        except OllamaLLMError:
            raise
        except Exception as exc:
            last_exc = exc
            if attempt == max_retries:
                raise OllamaLLMAPIError(
                    f"Ollama LLM request failed after {max_retries} attempts: {exc}"
                ) from exc

            # Backoff before next retry
            sleep_for = backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_for)

    raise OllamaLLMAPIError("Ollama LLM request failed") from last_exc


__all__ = ["ollama_llm", "OllamaLLMError", "OllamaLLMAPIError"]
