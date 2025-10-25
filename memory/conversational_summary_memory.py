"""
Conversational Summary Memory

Automatically summarizes old messages to save tokens while preserving context.
Best for: Very long conversations where full history would exceed token limits.
"""

from typing import List, Dict, Optional


class ConversationalSummaryMemory:
    """
    Memory that summarizes old conversation to maintain context with fewer tokens.
    
    This memory keeps recent messages in full detail but summarizes older messages
    to reduce token count while preserving important context.
    
    Example:
        >>> from llm import OpenAILLM
        >>> llm = OpenAILLM(model="gpt-3.5-turbo", api_key="key")
        >>> memory = ConversationalSummaryMemory(llm=llm, buffer_size=4)
        >>> # After 4 messages, old messages get summarized
    """
    
    def __init__(
        self, 
        llm=None,
        buffer_size: int = 5,
        return_messages: bool = True
    ):
        """
        Initialize ConversationalSummaryMemory.
        
        Args:
            llm: LLM instance with generate_response() method for summarization
            buffer_size: Number of recent messages to keep in full detail
            return_messages: If True, returns list of message dicts
        """
        self.llm = llm
        self.buffer_size = buffer_size
        self.return_messages = return_messages
        
        self.summary: str = ""
        self.buffer: List[Dict[str, str]] = []
    
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to memory.
        
        Args:
            message: The user's message content
        """
        self.buffer.append({
            "role": "user",
            "content": message
        })
        self._maybe_summarize()
    
    def add_ai_message(self, message: str) -> None:
        """
        Add an AI response to memory.
        
        Args:
            message: The AI's response content
        """
        self.buffer.append({
            "role": "assistant",
            "content": message
        })
        self._maybe_summarize()
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message with custom role.
        
        Args:
            role: Message role (user, assistant, system, etc.)
            content: Message content
        """
        self.buffer.append({
            "role": role,
            "content": content
        })
        self._maybe_summarize()
    
    def _maybe_summarize(self) -> None:
        """Summarize old messages if buffer exceeds size."""
        if len(self.buffer) > self.buffer_size and self.llm is not None:
            # Take first half of buffer to summarize
            to_summarize = self.buffer[:len(self.buffer) // 2]
            
            # Create summary prompt
            conversation = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in to_summarize
            ])
            
            prompt = f"""Summarize the following conversation concisely, preserving key information:

{conversation}

Summary:"""
            
            try:
                new_summary = self.llm.generate_response(prompt)
                
                # Update summary
                if self.summary:
                    self.summary += f"\n{new_summary}"
                else:
                    self.summary = new_summary
                
                # Remove summarized messages from buffer
                self.buffer = self.buffer[len(to_summarize):]
            except Exception as e:
                # If summarization fails, just continue without summarizing
                pass
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history (summary + recent messages).
        
        Returns:
            List of message dictionaries
        """
        messages = []
        
        if self.summary:
            messages.append({
                "role": "system",
                "content": f"Previous conversation summary: {self.summary}"
            })
        
        messages.extend(self.buffer)
        return messages
    
    def get_history_as_string(self) -> str:
        """
        Get conversation history as a formatted string.
        
        Returns:
            Formatted string representation
        """
        result = ""
        
        if self.summary:
            result += f"Summary: {self.summary}\n\n"
        
        if self.buffer:
            result += "Recent messages:\n"
            for msg in self.buffer:
                role = msg["role"].capitalize()
                content = msg["content"]
                result += f"{role}: {content}\n"
        
        return result.strip()
    
    def get_context(self) -> str:
        """
        Get conversation context for prompt injection.
        
        Returns:
            Formatted context string
        """
        if not self.summary and not self.buffer:
            return ""
        
        context = "Conversation context:\n"
        context += self.get_history_as_string()
        return context
    
    def clear(self) -> None:
        """Clear all memory including summary."""
        self.summary = ""
        self.buffer.clear()
    
    def get_summary(self) -> str:
        """
        Get the current summary.
        
        Returns:
            Summary text
        """
        return self.summary
    
    def get_message_count(self) -> int:
        """
        Get the number of messages in buffer.
        
        Returns:
            Number of messages in buffer
        """
        return len(self.buffer)
    
    def set_llm(self, llm) -> None:
        """
        Set or update the LLM for summarization.
        
        Args:
            llm: LLM instance with generate_response() method
        """
        self.llm = llm
    
    def save_to_dict(self) -> Dict:
        """
        Save memory state to a dictionary.
        
        Returns:
            Dictionary containing memory state
        """
        return {
            "summary": self.summary,
            "buffer": self.buffer.copy(),
            "buffer_size": self.buffer_size,
            "return_messages": self.return_messages
        }
    
    def load_from_dict(self, data: Dict) -> None:
        """
        Load memory state from a dictionary.
        
        Args:
            data: Dictionary containing memory state
        """
        self.summary = data.get("summary", "")
        self.buffer = data.get("buffer", [])
        self.buffer_size = data.get("buffer_size", 5)
        self.return_messages = data.get("return_messages", True)
    
    def __len__(self) -> int:
        """Return the number of messages in buffer."""
        return len(self.buffer)
    
    def __str__(self) -> str:
        """String representation."""
        has_summary = "with summary" if self.summary else "no summary"
        return f"ConversationalSummaryMemory(buffer={len(self.buffer)}/{self.buffer_size}, {has_summary})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ConversationalSummaryMemory(buffer_size={self.buffer_size}, buffer={len(self.buffer)}, has_summary={bool(self.summary)})"
