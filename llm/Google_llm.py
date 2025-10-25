"""Small, robust wrapper around Google's Generative AI client.

This module provides a single function, ``google_llm``, which will
call Google's generative APIs with input validation, retries, timeouts and
clear exceptions suitable for production integration.

Notes:
- No logging is performed by this module (per project requirement).
- The function prefers the official ``google.generativeai`` package when
  available but has defensive code to handle different shapes of response
  objects used across minor client versions.

Example usage:
    >>> from Codemni.llm import google_llm, GoogleLLMError
    >>> 
    >>> try:
    ...     response = google_llm(
    ...         prompt="Explain Python in one sentence",
    ...         model="gemini-pro",
    ...         api_key="your-api-key-here"  # or set GOOGLE_API_KEY env var
    ...     )
    ...     print(response)
    ... except GoogleLLMError as e:
    ...     print(f"Error: {e}")
"""

from typing import Optional, Any
import os
import time
import warnings
import sys
from contextlib import contextmanager

# Suppress gRPC ALTS warnings at environment level
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Suppress Python warnings from gRPC
warnings.filterwarnings('ignore', category=UserWarning, module='.*grpc.*')

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

# Import the Google generativeai client at module level to reduce import overhead
_GOOGLE_GENAI_AVAILABLE = False
genai_module = None
try:
    with suppress_stderr():
        try:
            import google.generativeai as genai_module  # type: ignore
            _GOOGLE_GENAI_AVAILABLE = True
        except Exception:
            # older or alternate packaging
            from google import genai as genai_module  # type: ignore
            _GOOGLE_GENAI_AVAILABLE = True
except Exception:
    _GOOGLE_GENAI_AVAILABLE = False
    genai_module = None


class GoogleLLMError(Exception):
    """Base exception for errors raised by this module."""


class GoogleLLMImportError(GoogleLLMError):
    """Raised when the Google generative client library cannot be imported."""


class GoogleLLMAPIError(GoogleLLMError):
    """Raised when the API request fails after retries."""


class GoogleLLMResponseError(GoogleLLMError):
    """Raised when the response from the API cannot be interpreted."""


def _extract_text_from_response(resp: Any) -> Optional[str]:
    """Try several patterns to extract the generated text from a response.

    The Google client has evolved and different helper wrappers return
    different shapes (objects with a ``text`` attribute, dicts with
    ``candidates``, etc.). This function centralizes tolerant extraction
    logic.
    """
    if resp is None:
        return None

    # Try 1: Object-like responses with .text attribute or property
    try:
        text = getattr(resp, "text", None)
        if text is not None:
            # Handle both property and attribute
            if callable(text):
                text = text()
            if isinstance(text, str) and text.strip():
                return text
    except Exception:
        pass

    # Try 2: Check for candidates attribute (common in newer APIs)
    candidates = getattr(resp, "candidates", None)
    if candidates and isinstance(candidates, (list, tuple)) and len(candidates) > 0:
        first_candidate = candidates[0]
        
        # Try to get content from the candidate
        content = getattr(first_candidate, "content", None)
        if content:
            # Check for parts in content
            parts = getattr(content, "parts", None)
            if parts and isinstance(parts, (list, tuple)) and len(parts) > 0:
                first_part = parts[0]
                # Try to get text from the part
                part_text = getattr(first_part, "text", None)
                if isinstance(part_text, str) and part_text.strip():
                    return part_text
            
            # Try direct text in content
            content_text = getattr(content, "text", None)
            if isinstance(content_text, str) and content_text.strip():
                return content_text
        
        # Try direct text in candidate
        candidate_text = getattr(first_candidate, "text", None)
        if isinstance(candidate_text, str) and candidate_text.strip():
            return candidate_text

    # Try 3: Dict-like responses
    try:
        if isinstance(resp, dict):
            # Pattern: {'candidates': [{'content': {'parts': [{'text': '...'}]}}]}
            candidates = resp.get("candidates")
            if candidates and isinstance(candidates, (list, tuple)) and len(candidates) > 0:
                first = candidates[0]
                if isinstance(first, dict):
                    # Try nested content.parts[0].text
                    content = first.get("content")
                    if isinstance(content, dict):
                        parts = content.get("parts")
                        if isinstance(parts, (list, tuple)) and len(parts) > 0:
                            part = parts[0]
                            if isinstance(part, dict):
                                text = part.get("text")
                                if isinstance(text, str) and text.strip():
                                    return text
                    
                    # Try direct content or text
                    cont = first.get("content") or first.get("text")
                    if isinstance(cont, str) and cont.strip():
                        return cont
            
            # Sometimes response may have top-level 'text'
            cont = resp.get("text")
            if isinstance(cont, str) and cont.strip():
                return cont
    except Exception:
        # Be tolerant: fall through to return None
        pass

    return None


def google_llm(
    prompt: str,
    model: str,
    api_key: Optional[str] = None,
    *,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    max_tokens: Optional[int] = None,
    max_retries: int = 3,
    timeout: Optional[float] = 30.0,
    backoff_factor: float = 0.5,
) -> str:
    """Call a Google generative model and return the generated text.

    Args:
        prompt: The prompt / input text to send to the model. Must be non-empty.
        model: Model identifier (e.g. "gemini-pro" or other supported model name).
        api_key: API key to use. If omitted, the function will try the
            environment variable ``GOOGLE_API_KEY``.
        temperature: Controls randomness (0.0-2.0). Higher = more random.
        top_p: Nucleus sampling threshold (0.0-1.0). Alternative to temperature.
        top_k: Top-k sampling. Limits to k most likely tokens.
        max_tokens: Maximum tokens to generate (max_output_tokens).
        max_retries: Number of attempts to make on transient failures.
        timeout: Optional timeout (seconds) to pass to the underlying client.
        backoff_factor: Base factor for exponential backoff between retries.

    Returns:
        The generated text from the model.

    Raises:
        ValueError: If required arguments are missing or invalid.
        GoogleLLMImportError: If the Google client is not installed.
        GoogleLLMAPIError: If all retry attempts fail.
        GoogleLLMResponseError: If a response is returned but contains no text.
    """

    # Basic validation
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a non-empty string")
    if not isinstance(max_retries, int) or max_retries < 1:
        raise ValueError("max_retries must be an integer >= 1")
    
    # Validate generation parameters
    if temperature is not None and not (0.0 <= temperature <= 2.0):
        raise ValueError("temperature must be between 0.0 and 2.0")
    if top_p is not None and not (0.0 <= top_p <= 1.0):
        raise ValueError("top_p must be between 0.0 and 1.0")
    if top_k is not None and top_k < 1:
        raise ValueError("top_k must be >= 1")
    if max_tokens is not None and max_tokens < 1:
        raise ValueError("max_tokens must be >= 1")

    # Build generation config
    generation_config = {}
    if temperature is not None:
        generation_config["temperature"] = temperature
    if top_p is not None:
        generation_config["top_p"] = top_p
    if top_k is not None:
        generation_config["top_k"] = top_k
    if max_tokens is not None:
        generation_config["max_output_tokens"] = max_tokens

    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise GoogleLLMImportError(
            "No API key provided and environment variable GOOGLE_API_KEY is not set"
        )

    # Check if Google generativeai client is available
    if not _GOOGLE_GENAI_AVAILABLE or genai_module is None:
        raise GoogleLLMImportError(
            "Failed to import or initialize google.generativeai client"
        )

    # Use the module-level imported genai
    genai = genai_module
    client = None
    
    # Try to configure or create a client where appropriate. The package
    # has a couple of helper patterns (configure + GenerativeModel) and a
    # client wrapper with .models.generate_content. Be tolerant and keep
    # the object shapes available for later.
    try:
        with suppress_stderr():
            # Prefer configure() if provided (no return value)
            cfg = getattr(genai, "configure", None)
            if callable(cfg):
                cfg(api_key=api_key)
    except Exception:
        # Non-fatal: some wrappers don't require configure
        pass

    # Instantiate client if a Client class exists
    try:
        with suppress_stderr():
            ClientCls = getattr(genai, "Client", None)
            if callable(ClientCls):
                try:
                    client = ClientCls(api_key=api_key)
                except TypeError:
                    # Some Client constructors use different signatures
                    client = ClientCls()
    except Exception:
        # Non-fatal: client may not be needed
        pass

    last_exc: Optional[BaseException] = None

    for attempt in range(1, max_retries + 1):
        try:
            # Try several calling patterns in order of preference
            # Wrap API calls in stderr suppression to hide gRPC warnings
            with suppress_stderr():
                # 1) If the client has models.generate_content (client.models.generate_content)
                if client is not None:
                    models_attr = getattr(client, "models", None)
                    gen_fn = getattr(models_attr, "generate_content", None) if models_attr else None
                    if callable(gen_fn):
                        resp = gen_fn(model=model, contents=prompt, timeout=timeout)
                        text = _extract_text_from_response(resp)
                        if text:
                            return text

                # 2) If package exposes GenerativeModel and it has generate_content
                GenerativeModel = getattr(genai, "GenerativeModel", None)
                if callable(GenerativeModel):
                    try:
                        # Create model with generation config if provided
                        if generation_config:
                            model_obj = GenerativeModel(model, generation_config=generation_config)
                        else:
                            model_obj = GenerativeModel(model)
                        gen_fn = getattr(model_obj, "generate_content", None)
                        if callable(gen_fn):
                            resp = gen_fn(prompt)  # GenerativeModel doesn't support timeout parameter
                            text = _extract_text_from_response(resp)
                            if text:
                                return text
                    except Exception:
                        # Be tolerant: fall through to other options
                        pass

                # 3) Top-level convenience helpers (generate_text / generate)
                for helper_name in ("generate_text", "generate", "model_generate"):
                    helper = getattr(genai, helper_name, None)
                    if callable(helper):
                        try:
                            resp = helper(model=model, prompt=prompt, timeout=timeout)
                            text = _extract_text_from_response(resp)
                            if text:
                                return text
                        except Exception:
                            pass

            # If none of the above returned text, raise a response error to
            # trigger retry / final failure handling.
            raise GoogleLLMResponseError("No text could be extracted from the API response")

        except Exception as exc:  # catch network/errors from client
            last_exc = exc
            if attempt == max_retries:
                # Exhausted retries; surface a clear error to the caller.
                raise GoogleLLMAPIError(
                    f"Google LLM request failed after {max_retries} attempts: {exc}"
                ) from exc

            # Backoff before the next retry (no logging per user request)
            sleep_for = backoff_factor * (2 ** (attempt - 1))
            # Ensure minimum sleep to avoid tight loop
            time.sleep(sleep_for)

    # If the loop exits without returning, raise the last observed exception
    raise GoogleLLMAPIError("Google LLM request failed") from last_exc


class GoogleLLM:
    """
    Class-based wrapper for Google Gemini LLM with generate_response method.
    
    This class wraps the google_llm function to provide a stateful interface
    suitable for use with agents and other systems that expect an object
    with a generate_response(prompt) method.
    
    Example:
        >>> llm = GoogleLLM(model="gemini-1.5-pro", api_key="your-key")
        >>> response = llm.generate_response("What is Python?")
        >>> print(response)
    """
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        *,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        timeout: Optional[float] = 30.0,
        backoff_factor: float = 0.5,
    ):
        """
        Initialize Google Gemini LLM wrapper.
        
        Args:
            model: Model identifier (e.g. "gemini-1.5-pro", "gemini-pro")
            api_key: API key (optional if GOOGLE_API_KEY env var is set)
            temperature: Controls randomness (0.0-2.0)
            top_p: Nucleus sampling threshold (0.0-1.0)
            top_k: Top-k sampling
            max_tokens: Maximum tokens to generate
            max_retries: Number of retry attempts on failure
            timeout: Request timeout in seconds
            backoff_factor: Exponential backoff factor for retries
        """
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the Google Gemini model.
        
        Args:
            prompt: The input prompt text
            
        Returns:
            Generated response text
            
        Raises:
            ValueError: If prompt is invalid
            GoogleLLMImportError: If Google client not available
            GoogleLLMAPIError: If API request fails
            GoogleLLMResponseError: If response is invalid
        """
        return google_llm(
            prompt=prompt,
            model=self.model,
            api_key=self.api_key,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            max_tokens=self.max_tokens,
            max_retries=self.max_retries,
            timeout=self.timeout,
            backoff_factor=self.backoff_factor,
        )


__all__ = [
    "google_llm",
    "GoogleLLM",
    "GoogleLLMError",
    "GoogleLLMAPIError",
    "GoogleLLMImportError",
    "GoogleLLMResponseError",
]