"""
Agents Module - Advanced AI Agents with Tool Calling Capabilities

This module provides three types of agents:
1. TOOL_CALLING_AGENT: Standard tool-calling agent for most use cases
2. REASONING_TOOL_CALLING_AGENT: Agent with reasoning capabilities
3. DEEP_REASONING_TOOL_CALLING_AGENT: Advanced agent with chain-of-thought reasoning

Example:
    >>> from Codemni.Agents import Create_ToolCalling_Agent
    >>> from Codemni.Agents import Create_Deep_Reasoning_Tool_Calling_Agent
"""

from .TOOL_CALLING_AGENT import Create_ToolCalling_Agent
from .REASONING_TOOL_CALLING_AGENT import Create_ToolCalling_Agent as Create_Reasoning_ToolCalling_Agent
from .DEEP_REASONING_TOOL_CALLING_AGENT import Create_Deep_Reasoning_Tool_Calling_Agent

__all__ = [
    "Create_ToolCalling_Agent",
    "Create_Reasoning_ToolCalling_Agent",
    "Create_Deep_Reasoning_Tool_Calling_Agent",
]

__version__ = "1.2.2"