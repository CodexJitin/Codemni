"""
Example usage of codemni_LLM package
Demonstrates all supported LLM providers
"""

import os

# Example 1: Google Gemini
def example_google():
    from codemni_LLM import google_llm, GoogleLLMError
    
    try:
        response = google_llm(
            prompt="What is Python? Answer in one sentence.",
            model="gemini-pro",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        print("Google Gemini Response:")
        print(response)
        print()
    except GoogleLLMError as e:
        print(f"Google Error: {e}")
        print()


# Example 2: OpenAI
def example_openai():
    from codemni_LLM import openai_llm, OpenAILLMError
    
    try:
        response = openai_llm(
            prompt="Write a haiku about programming",
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=50
        )
        print("OpenAI Response:")
        print(response)
        print()
    except OpenAILLMError as e:
        print(f"OpenAI Error: {e}")
        print()


# Example 3: Anthropic Claude
def example_anthropic():
    from codemni_LLM import anthropic_llm, AnthropicLLMError
    
    try:
        response = anthropic_llm(
            prompt="Explain machine learning in simple terms",
            model="claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.5,
            max_tokens=150
        )
        print("Anthropic Claude Response:")
        print(response)
        print()
    except AnthropicLLMError as e:
        print(f"Anthropic Error: {e}")
        print()


# Example 4: Groq
def example_groq():
    from codemni_LLM import groq_llm, GroqLLMError
    
    try:
        response = groq_llm(
            prompt="What is artificial intelligence?",
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.3
        )
        print("Groq Response:")
        print(response)
        print()
    except GroqLLMError as e:
        print(f"Groq Error: {e}")
        print()


# Example 5: Ollama (Local)
def example_ollama():
    from codemni_LLM import ollama_llm, OllamaLLMError
    
    try:
        response = ollama_llm(
            prompt="Explain Docker in one sentence",
            model="llama2",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.8
        )
        print("Ollama Response:")
        print(response)
        print()
    except OllamaLLMError as e:
        print(f"Ollama Error: {e}")
        print()


# Example 6: Error handling
def example_error_handling():
    from codemni_LLM import google_llm, GoogleLLMError, GoogleLLMAPIError, GoogleLLMImportError
    
    try:
        # This will fail if API key is not set
        response = google_llm(
            prompt="Test prompt",
            model="gemini-pro"
        )
        print(response)
    except GoogleLLMImportError as e:
        print(f"Import/Config Error: {e}")
    except GoogleLLMAPIError as e:
        print(f"API Error: {e}")
    except GoogleLLMError as e:
        print(f"General Error: {e}")
    except ValueError as e:
        print(f"Invalid parameters: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("codemni_LLM Examples")
    print("=" * 60)
    print()
    
    # Uncomment the examples you want to test
    # Make sure to set the corresponding environment variables
    
    # example_google()
    # example_openai()
    # example_anthropic()
    # example_groq()
    # example_ollama()
    example_error_handling()
