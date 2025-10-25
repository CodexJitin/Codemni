import re
import json
from typing import Optional
from .prompt import PREFIX_PROMPT, LOGIC_PROMPT, SUFFIX_PROMPT
from core.adapter import Tool_Executor


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

class Create_ToolCalling_Agent:
    """
    Agent that can call tools based on LLM decisions.
    
    The agent accepts an LLM object that must have a generate_response(prompt) method.
    Initialize your LLM from the llm folder before passing it to this agent.
    """
    
    def __init__(
        self, 
        llm,
        verbose: bool = False,
        prompt: Optional[str] = None,
        memory = None,
    ) -> None:
        """
        Initialize ToolCallAgent with an LLM object.
        
        Args:
            llm: LLM object with a generate_response(prompt) method.
                 Use llm from the llm folder (google_llm, openai_llm, anthropic_llm, groq_llm, ollama_llm)
            verbose: Enable verbose logging
            prompt: Custom agent introduction (optional). Should ONLY contain agent personality/role description.
                   ⚠️ WARNING: The custom prompt should ONLY be the agent introduction (e.g., "You are a helpful 
                   math tutor"). Do NOT include tool instructions or response format - these are added automatically.
                   If not provided, uses default agent introduction.
            memory: Optional memory object (ConversationalBufferMemory, ConversationalWindowMemory, etc.)
                   from the memory module. If provided, conversation history will be maintained.
        
        Example:
            # Without custom prompt (uses default)
            agent = Create_ToolCalling_Agent(llm=my_llm, verbose=True)
            
            # With custom agent introduction
            custom_intro = "You are a friendly financial advisor assistant."
            agent = Create_ToolCalling_Agent(llm=my_llm, prompt=custom_intro, verbose=True)
            
            # With memory
            from memory import ConversationalWindowMemory
            memory = ConversationalWindowMemory(window_size=10)
            agent = Create_ToolCalling_Agent(llm=my_llm, memory=memory, verbose=True)
        """
        self.tools = {}
        self.llm = llm
        self.verbose = verbose
        self.memory = memory
        
        # If user provides custom prompt (agent introduction), use it instead of PREFIX
        # Otherwise use default PREFIX_PROMPT
        # LOGIC_PROMPT and SUFFIX_PROMPT are always added automatically
        if prompt is not None:
            if verbose:
                print(f"{Colors.YELLOW}⚠{Colors.ENDC} Using custom agent introduction. "
                      f"Only provide agent personality/role - tool instructions are added automatically.")
            self.prompt_template = prompt + "\n\n" + LOGIC_PROMPT + SUFFIX_PROMPT
            self.custom_prompt = True
        else:
            self.prompt_template = PREFIX_PROMPT + LOGIC_PROMPT + SUFFIX_PROMPT
            self.custom_prompt = False
        
    def _parser(self, response):
        """
        Parse the LLM response to extract tool call, parameters, and final response.
        
        Args:
            response: Raw response string from LLM containing JSON block
            
        Returns:
            tuple: (tool_call_dict, tool_parameters_dict, final_response_dict)
        """
        # Extract JSON block with ```json or '''json markers
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
        if not json_match:
            json_match = re.search(r"'''json\s*(\{.*?\})\s*'''", response, re.DOTALL)
        
        if not json_match:
            raise ValueError(f"Invalid response format: No JSON block found in response: {response[:200]}")
        
        # Parse the single JSON object containing all three keys
        parsed_json = json.loads(json_match.group(1))
        
        # Create separate dicts for each component
        tool_call = {"Tool call": parsed_json.get("Tool call", "None")}
        tool_parameters = {"Tool Parameters": parsed_json.get("Tool Parameters", "None")}
        final_response = {"Final Response": parsed_json.get("Final Response", "None")}
        
        return tool_call, tool_parameters, final_response
        
    
    def add_llm(self, llm):
        """
        Set or update the LLM instance.
        
        Args:
            llm: LLM object with a generate_response(prompt) method
        """
        self.llm = llm
    
    def add_memory(self, memory):
        """
        Set or update the memory instance.
        
        Args:
            memory: Memory object from memory module (ConversationalBufferMemory, etc.)
        """
        self.memory = memory
    
    def clear_memory(self):
        """Clear the conversation memory if it exists."""
        if self.memory is not None:
            self.memory.clear()
            self._log("Memory cleared", "success")
    
    def get_memory_history(self):
        """
        Get the conversation history from memory.
        
        Returns:
            List of message dicts if memory exists, empty list otherwise
        """
        if self.memory is not None:
            return self.memory.get_history()
        return []
    
    def add_tool(self, name, description, function):
        """
        Add a tool that the agent can use.
        
        Args:
            name: Tool name
            description: Description of what the tool does
            function: Callable function to execute
        """
        self.tools[name] = {
            "description": description,
            "function": function
        }
    
    def _log(self, message, level="info"):
        """Print message if verbose mode is enabled with colors."""
        if self.verbose:
            if level == "info":
                print(f"{Colors.BLUE}ℹ{Colors.ENDC} {message}")
            elif level == "success":
                print(f"{Colors.GREEN}✓{Colors.ENDC} {message}")
            elif level == "error":
                print(f"{Colors.RED}✗{Colors.ENDC} {message}")
            elif level == "warning":
                print(f"{Colors.YELLOW}⚠{Colors.ENDC} {message}")
    
    def invoke(self, query):
        """
        Execute the agent with a user query.
        
        Args:
            query: User's question or request
            
        Returns:
            Final response from the agent
        """
        if self.llm is None:
            raise ValueError("LLM not set. Call add_llm() first")
        
        if not self.tools:
            raise ValueError("No tools added. Call add_tool() at least once")
        
        # Add user query to memory if available
        if self.memory is not None:
            self.memory.add_user_message(query)
            self._log("Added user message to memory", "info")
        
        # Compile prompt inline
        tool_list = "\n".join(
            [f"        - {name}: {info['description']}" 
             for name, info in self.tools.items()]
        )
        compiled_prompt = self.prompt_template.replace("{tool_list}", tool_list)
        
        # Add memory context if available
        memory_context = ""
        if self.memory is not None:
            context = self.memory.get_context()
            if context:
                memory_context = f"\n\n--- Conversation History ---\n{context}\n--- End History ---\n"
                self._log("Including conversation history", "info")
        
        if self.verbose:
            print(f"\n{Colors.CYAN}{'─' * 70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.CYAN}Starting ToolCalling Agent{Colors.ENDC}")
            print(f"{Colors.CYAN}{'─' * 70}{Colors.ENDC}\n")
        
        prompt = compiled_prompt.format(user_input=query) + memory_context
        scratchpad = ""
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Get LLM response
            full_prompt = f"{prompt}\n{scratchpad}" if scratchpad else prompt
            response = self.llm.generate_response(full_prompt)
            
            try:
                tool_call, tool_params, final_response = self._parser(response)
            except Exception as e:
                error_msg = f"Error parsing response: {str(e)}"
                self._log(error_msg, "error")
                return error_msg
            
            # Check if agent wants to provide final response
            tool_name = tool_call.get("Tool call")
            
            if tool_name == "None" or not tool_name:
                final_answer = final_response.get("Final Response", "No response provided")
                
                # Add AI response to memory if available
                if self.memory is not None:
                    self.memory.add_ai_message(final_answer)
                    self._log("Added AI response to memory", "info")
                
                if self.verbose:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Final Response:{Colors.ENDC}")
                    print(f"{Colors.GREEN}▸{Colors.ENDC} {final_answer}\n")
                
                return final_answer
            
            # Execute tool
            params = tool_params.get("Tool Parameters")
            
            if self.verbose:
                print(f"{Colors.YELLOW}🔧 Tool:{Colors.ENDC} {Colors.BOLD}{tool_name}{Colors.ENDC}")
                print(f"{Colors.YELLOW}📝 Params:{Colors.ENDC} {params}")
            
            tool_result = Tool_Executor(tool_name, params, self.tools)
            
            if self.verbose:
                print(f"{Colors.GREEN}📤 Result:{Colors.ENDC} {tool_result}\n")
            
            # Update scratchpad with tool result for next iteration
            scratchpad += f"\n\n--- Previous Tool Call ---\nTool Used: {tool_name}\nResult: {tool_result}\n\nNow provide the final response to the user based on this result."
        
        error_msg = "Error: Maximum iterations reached"
        self._log(error_msg, "error")
        return error_msg