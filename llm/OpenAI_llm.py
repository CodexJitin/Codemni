"""Small, robust wrapper around OpenAI's API client.

This module provides a single function, ``openai_llm``, which will
call OpenAI's API with input validation, retries, timeouts and
clear exceptions suitable for production integration.

Notes:
- No logging is performed by this module (per project requirement).
- Handles both chat models (gpt-4, gpt-3.5-turbo) and legacy completion models.

Example usage:
    >>> from Codemni.llm import openai_llm, OpenAILLMError
    >>> 
    >>> try:
    ...     response = openai_llm(
    ...         prompt="Explain Python in one sentence",
    ...         model="gpt-4",
    ...         api_key="your-api-key-here"  # or set OPENAI_API_KEY env var
    ...     )
    ...     print(response)
    ... except OpenAILLMError as e:
    ...     print(f"Error: {e}")
"""

from typing import Optional, Any
import os
import time
import warnings
import sys
from contextlib import contextmanager

# Suppress gRPC and other warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress Python warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

@contextmanager
def suppress_stderr():
    """Temporarily suppress stderr output using low-level file descriptor redirection."""
    import io
    
    # Save original stderr
    original_stderr = sys.stderr
    original_stderr_fd = None
    
    try:
        # Save the original file descriptor
        try:
            original_stderr_fd = os.dup(2)
        except:
            pass
        
        # Redirect stderr to devnull
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, 2)
            os.close(devnull)
        except:
            pass
        
        # Also redirect Python's sys.stderr
        sys.stderr = io.StringIO()
        
        yield
        
    finally:
        # Restore stderr
        try:
            if original_stderr_fd is not None:
                os.dup2(original_stderr_fd, 2)
                os.close(original_stderr_fd)
        except:
            pass
        
        sys.stderr = original_stderr

# Import the OpenAI client at module level to reduce import overhead
try:
    with suppress_stderr():
        from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    OpenAI = None  # type: ignore


class OpenAILLMError(Exception):
    """Base exception for errors raised by this module."""


class OpenAILLMImportError(OpenAILLMError):
    """Raised when the OpenAI client library cannot be imported."""


class OpenAILLMAPIError(OpenAILLMError):
    """Raised when the API request fails after retries."""


class OpenAILLMResponseError(OpenAILLMError):
    """Raised when the response from the API cannot be interpreted."""


def openai_llm(
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
    """Call an OpenAI model and return the generated text.

    Args:
        prompt: The prompt / input text to send to the model. Must be non-empty.
        model: Model identifier (e.g. "gpt-4", "gpt-3.5-turbo").
        api_key: API key to use. If omitted, will try OPENAI_API_KEY env var.
        max_retries: Number of attempts to make on transient failures.
        timeout: Optional timeout (seconds) to pass to the underlying client.
        backoff_factor: Base factor for exponential backoff between retries.
        temperature: Sampling temperature (0.0 to 2.0, optional).
        max_tokens: Maximum tokens in response (optional).

    Returns:
        The generated text from the model.

    Raises:
        ValueError: If required arguments are missing or invalid.
        OpenAILLMImportError: If the OpenAI client is not installed.
        OpenAILLMAPIError: If all retry attempts fail.
        OpenAILLMResponseError: If a response is returned but contains no text.
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

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OpenAILLMImportError(
            "No API key provided and environment variable OPENAI_API_KEY is not set"
        )

    # Check if OpenAI client is available
    if not _OPENAI_AVAILABLE or OpenAI is None:
        raise OpenAILLMImportError(
            "OpenAI package not installed. Install with: pip install openai"
        )

    # Initialize client
    try:
        client = OpenAI(api_key=api_key, timeout=timeout)
    except Exception as exc:
        raise OpenAILLMImportError(
            "Failed to initialize OpenAI client"
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
                raise OpenAILLMResponseError("No choices in response")
            
            text = response.choices[0].message.content
            if not text or not isinstance(text, str):
                raise OpenAILLMResponseError("No valid text content in response")

            return text.strip()

        except OpenAILLMError:
            raise
        except Exception as exc:
            last_exc = exc
            if attempt == max_retries:
                raise OpenAILLMAPIError(
                    f"OpenAI LLM request failed after {max_retries} attempts: {exc}"
                ) from exc

            # Backoff before next retry
            sleep_for = backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_for)

    raise OpenAILLMAPIError("OpenAI LLM request failed") from last_exc


class OpenAILLM:
    """
    Class-based wrapper for OpenAI LLM with generate_response method.
    
    This class wraps the openai_llm function to provide a stateful interface
    suitable for use with agents and other systems that expect an object
    with a generate_response(prompt) method.
    
    Example:
        >>> llm = OpenAILLM(model="gpt-4", api_key="your-key", temperature=0.7)
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
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize OpenAI LLM wrapper.
        
        Args:
            model: Model identifier (e.g. "gpt-4", "gpt-3.5-turbo")
            api_key: API key (optional if OPENAI_API_KEY env var is set)
            max_retries: Number of retry attempts on failure
            timeout: Request timeout in seconds
            backoff_factor: Exponential backoff factor for retries
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
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
        Generate a response from the OpenAI model.
        
        Args:
            prompt: The input prompt text
            
        Returns:
            Generated response text
            
        Raises:
            ValueError: If prompt is invalid
            OpenAILLMImportError: If OpenAI client not available
            OpenAILLMAPIError: If API request fails
            OpenAILLMResponseError: If response is invalid
        """
        return openai_llm(
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
    "openai_llm",
    "OpenAILLM",
    "OpenAILLMError",
    "OpenAILLMAPIError",
    "OpenAILLMImportError",
    "OpenAILLMResponseError",
]
