"""
Conversational Buffer Memory

Stores all conversation history in a simple buffer without any limitations.
Best for: Short conversations or when full context is important.
"""

from typing import List, Dict, Optional


class ConversationalBufferMemory:
    """
    Simple memory buffer that stores all conversation history.
    
    This memory stores every user input and AI response without any limit.
    It provides complete conversation context but can grow very large.
    
    Example:
        >>> memory = ConversationalBufferMemory()
        >>> memory.add_user_message("Hello!")
        >>> memory.add_ai_message("Hi there! How can I help you?")
        >>> print(memory.get_history())
        [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there! How can I help you?"}
        ]
    """
    
    def __init__(self, return_messages: bool = True):
        """
        Initialize ConversationalBufferMemory.
        
        Args:
            return_messages: If True, returns list of message dicts.
                           If False, returns formatted string.
        """
        self.messages: List[Dict[str, str]] = []
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
        Get the complete conversation history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return self.messages.copy()
    
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
        
        context = "Previous conversation:\n"
        context += self.get_history_as_string()
        return context
    
    def clear(self) -> None:
        """Clear all memory."""
        self.messages.clear()
    
    def get_message_count(self) -> int:
        """
        Get the number of messages in memory.
        
        Returns:
            Number of messages stored
        """
        return len(self.messages)
    
    def save_to_dict(self) -> Dict:
        """
        Save memory state to a dictionary.
        
        Returns:
            Dictionary containing memory state
        """
        return {
            "messages": self.messages.copy(),
            "return_messages": self.return_messages
        }
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load memory state from a dictionary.
        
        Args:
            data: Dictionary containing memory state
        """
        self.messages = data.get("messages", [])
        self.return_messages = data.get("return_messages", True)
    
    def __len__(self) -> int:
        """Return the number of messages."""
        return len(self.messages)
    
    def __str__(self) -> str:
        """String representation of the memory."""
        return f"ConversationalBufferMemory(messages={len(self.messages)})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ConversationalBufferMemory(messages={len(self.messages)}, return_messages={self.return_messages})"
