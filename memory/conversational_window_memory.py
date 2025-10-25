"""
Conversational Window Memory

Stores only the last N messages to maintain a sliding window of conversation history.
Best for: Long conversations where recent context is most important.
"""

from typing import List, Dict, Optional
from collections import deque


class ConversationalWindowMemory:
    """
    Memory that keeps only the last N messages in a sliding window.
    
    This memory maintains a fixed-size window of recent conversation history.
    Older messages are automatically removed when the window size is exceeded.
    
    Example:
        >>> memory = ConversationalWindowMemory(window_size=4)
        >>> memory.add_user_message("Message 1")
        >>> memory.add_ai_message("Response 1")
        >>> memory.add_user_message("Message 2")
        >>> memory.add_ai_message("Response 2")
        >>> memory.add_user_message("Message 3")  # This pushes out "Message 1"
        >>> len(memory)
        4  # Only keeps last 4 messages
    """
    
    def __init__(self, window_size: int = 10, return_messages: bool = True):
        """
        Initialize ConversationalWindowMemory.
        
        Args:
            window_size: Maximum number of messages to keep (default: 10)
            return_messages: If True, returns list of message dicts.
                           If False, returns formatted string.
        """
        if window_size < 1:
            raise ValueError("window_size must be at least 1")
        
        self.window_size = window_size
        self.messages: deque = deque(maxlen=window_size)
        self.return_messages = return_messages
    
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to memory.
        
        Args:
            message: The user's message content
        """
        self.messages.append({
            "role": "user",
            "content": message
        })
    
    def add_ai_message(self, message: str) -> None:
        """
        Add an AI response to memory.
        
        Args:
            message: The AI's response content
        """
        self.messages.append({
            "role": "assistant",
            "content": message
        })
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message with custom role.
        
        Args:
            role: Message role (user, assistant, system, etc.)
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history within the window.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return list(self.messages)
    
    def get_history_as_string(self) -> str:
        """
        Get conversation history as a formatted string.
        
        Returns:
            Formatted string representation of the conversation
        """
        if not self.messages:
            return ""
        
        history_str = ""
        for msg in self.messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            history_str += f"{role}: {content}\n"
        
        return history_str.strip()
    
    def get_context(self) -> str:
        """
        Get conversation context for prompt injection.
        
        Returns:
            Formatted context string to include in prompts
        """
        if not self.messages:
            return ""
        
        context = f"Recent conversation (last {len(self.messages)} messages):\n"
        context += self.get_history_as_string()
        return context
    
    def clear(self) -> None:
        """Clear all memory."""
        self.messages.clear()
    
    def get_message_count(self) -> int:
        """
        Get the number of messages currently in memory.
        
        Returns:
            Number of messages stored
        """
        return len(self.messages)
    
    def is_full(self) -> bool:
        """
        Check if the memory window is full.
        
        Returns:
            True if window is at maximum capacity
        """
        return len(self.messages) == self.window_size
    
    def set_window_size(self, new_size: int) -> None:
        """
        Change the window size. May truncate existing messages.
        
        Args:
            new_size: New window size (must be >= 1)
        """
        if new_size < 1:
            raise ValueError("window_size must be at least 1")
        
        # Create new deque with new size and existing messages
        old_messages = list(self.messages)
        self.window_size = new_size
        self.messages = deque(old_messages[-new_size:], maxlen=new_size)
    
    def save_to_dict(self) -> Dict:
        """
        Save memory state to a dictionary.
        
        Returns:
            Dictionary containing memory state
        """
        return {
            "messages": list(self.messages),
            "window_size": self.window_size,
            "return_messages": self.return_messages
        }
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load memory state from a dictionary.
        
        Args:
            data: Dictionary containing memory state
        """
        window_size = data.get("window_size", 10)
        self.window_size = window_size
        self.messages = deque(data.get("messages", []), maxlen=window_size)
        self.return_messages = data.get("return_messages", True)
    
    def __len__(self) -> int:
        """Return the number of messages."""
        return len(self.messages)
    
    def __str__(self) -> str:
        """String representation of the memory."""
        return f"ConversationalWindowMemory(messages={len(self.messages)}/{self.window_size})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ConversationalWindowMemory(window_size={self.window_size}, messages={len(self.messages)}, return_messages={self.return_messages})"
