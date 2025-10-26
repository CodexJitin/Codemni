"""
Codemni - Production-Ready Python Toolkit for AI Development

A modular collection of production-ready tools for building AI agents,
managing LLM interactions, and maintaining conversation context.

Modules:
- TOOL_CALLING_AGENT: Advanced AI agent with tool execution capabilities
- llm: Multi-provider LLM wrapper (OpenAI, Google, Anthropic, Groq, Ollama)
- memory: Conversation memory management for agents

Example:
    >>> from Codemni.llm import openai_llm
    >>> from Codemni.TOOL_CALLING_AGENT import Create_ToolCalling_Agent
    >>> from Codemni.memory import ConversationalBufferMemory

For detailed documentation, see: https://github.com/CodexJitin/Codemni
"""

__version__ = "1.2.3"
__author__ = "CodexJitin"
__license__ = "Proprietary"

# Note: Submodules are imported when accessed directly
# e.g., from Codemni.llm import openai_llm
