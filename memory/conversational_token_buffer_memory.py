"""
Conversational Token Buffer Memory

Limits memory based on token count rather than message count.
Best for: Managing memory within specific token budgets for API calls.
"""

from typing import List, Dict, Optional


class ConversationalTokenBufferMemory:
    """
    Memory that maintains conversation history within a token limit.
    
    This memory keeps messages that fit within a maximum token count,
    removing oldest messages when the limit would be exceeded.
    
    Example:
        >>> memory = ConversationalTokenBufferMemory(max_tokens=1000)
        >>> memory.add_user_message("Hello!")
        >>> memory.add_ai_message("Hi there!")
        >>> print(memory.get_token_count())
        ~50  # Approximate token count
    """
    
    def __init__(
        self, 
        max_tokens: int = 2000,
        tokens_per_message: int = 4,  # Overhead per message
        return_messages: bool = True
    ):
        """
        Initialize ConversationalTokenBufferMemory.
        
        Args:
            max_tokens: Maximum number of tokens to keep in memory
            tokens_per_message: Estimated overhead tokens per message
            return_messages: If True, returns list of message dicts
        """
        if max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        
        self.max_tokens = max_tokens
        self.tokens_per_message = tokens_per_message
        self.return_messages = return_messages
        self.messages: List[Dict[str, str]] = []
        self.current_tokens = 0
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Simple estimation: ~4 characters per token on average.
        For accurate counting, integrate with tiktoken library.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        return len(text) // 4 + self.tokens_per_message
    
    def _calculate_message_tokens(self, message: Dict[str, str]) -> int:
        """Calculate tokens for a single message."""
        return self._estimate_tokens(message["content"])
    
    def _prune_old_messages(self) -> None:
        """Remove oldest messages to fit within token limit."""
        while self.messages and self.current_tokens > self.max_tokens:
            removed_message = self.messages.pop(0)
            removed_tokens = self._calculate_message_tokens(removed_message)
            self.current_tokens -= removed_tokens
    
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to memory.
        
        Args:
            message: The user's message content
        """
        msg = {"role": "user", "content": message}
        tokens = self._calculate_message_tokens(msg)
        
        self.messages.append(msg)
        self.current_tokens += tokens
        self._prune_old_messages()
    
    def add_ai_message(self, message: str) -> None:
        """
        Add an AI response to memory.
        
        Args:
            message: The AI's response content
        """
        msg = {"role": "assistant", "content": message}
        tokens = self._calculate_message_tokens(msg)
        
        self.messages.append(msg)
        self.current_tokens += tokens
        self._prune_old_messages()
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message with custom role.
        
        Args:
            role: Message role (user, assistant, system, etc.)
            content: Message content
        """
        msg = {"role": role, "content": content}
        tokens = self._calculate_message_tokens(msg)
        
        self.messages.append(msg)
        self.current_tokens += tokens
        self._prune_old_messages()
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history within token limit.
        
        Returns:
            List of message dictionaries
        """
        return self.messages.copy()
    
    def get_history_as_string(self) -> str:
        """
        Get conversation history as a formatted string.
        
        Returns:
            Formatted string representation
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
            Formatted context string
        """
        if not self.messages:
            return ""
        
        context = f"Conversation history ({self.current_tokens}/{self.max_tokens} tokens):\n"
        context += self.get_history_as_string()
        return context
    
    def clear(self) -> None:
        """Clear all memory."""
        self.messages.clear()
        self.current_tokens = 0
    
    def get_message_count(self) -> int:
        """
        Get the number of messages in memory.
        
        Returns:
            Number of messages stored
        """
        return len(self.messages)
    
    def get_token_count(self) -> int:
        """
        Get the current estimated token count.
        
        Returns:
            Current token count
        """
        return self.current_tokens
    
    def get_available_tokens(self) -> int:
        """
        Get the number of tokens still available.
        
        Returns:
            Remaining token capacity
        """
        return max(0, self.max_tokens - self.current_tokens)
    
    def is_token_limit_reached(self) -> bool:
        """
        Check if token limit is reached or exceeded.
        
        Returns:
            True if at or over limit
        """
        return self.current_tokens >= self.max_tokens
    
    def set_max_tokens(self, new_max: int) -> None:
        """
        Change the maximum token limit. May prune messages.
        
        Args:
            new_max: New maximum token count
        """
        if new_max < 1:
            raise ValueError("max_tokens must be at least 1")
        
        self.max_tokens = new_max
        self._prune_old_messages()
    
    def save_to_dict(self) -> Dict:
        """
        Save memory state to a dictionary.
        
        Returns:
            Dictionary containing memory state
        """
        return {
            "messages": self.messages.copy(),
            "max_tokens": self.max_tokens,
            "current_tokens": self.current_tokens,
            "tokens_per_message": self.tokens_per_message,
            "return_messages": self.return_messages
        }
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load memory state from a dictionary.
        
        Args:
            data: Dictionary containing memory state
        """
        self.messages = data.get("messages", [])
        self.max_tokens = data.get("max_tokens", 2000)
        self.current_tokens = data.get("current_tokens", 0)
        self.tokens_per_message = data.get("tokens_per_message", 4)
        self.return_messages = data.get("return_messages", True)
    
    def __len__(self) -> int:
        """Return the number of messages."""
        return len(self.messages)
    
    def __str__(self) -> str:
        """String representation."""
        return f"ConversationalTokenBufferMemory(messages={len(self.messages)}, tokens={self.current_tokens}/{self.max_tokens})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ConversationalTokenBufferMemory(max_tokens={self.max_tokens}, current_tokens={self.current_tokens}, messages={len(self.messages)})"
