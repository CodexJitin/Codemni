"""
Tool Calling Agent Module

Provides an advanced AI agent framework with tool execution capabilities,
memory integration, and verbose debugging support.

Main Components:
- Create_ToolCalling_Agent: The main agent class with tool registration and execution
- Memory integration support (optional)
- Custom prompt support for agent introduction
- Verbose mode with colored terminal output

Note: This agent does NOT support reasoning models (o1, o3 series).

Example:
    >>> from Codemni.TOOL_CALLING_AGENT import Create_ToolCalling_Agent
    >>> from Codemni.llm import openai_llm
    >>> 
    >>> llm = openai_llm(model="gpt-4", api_key="your-key")
    >>> agent = Create_ToolCalling_Agent(llm=llm, verbose=True)
    >>> 
    >>> def calculator(a: int, b: int) -> int:
    ...     return a + b
    >>> 
    >>> agent.register_tool(calculator)
    >>> result = agent.invoke("What is 5 + 3?")
"""

from .agent import Create_ToolCalling_Agent

__all__ = ["Create_ToolCalling_Agent"]

__version__ = "1.1.0"
