import re
import json
from typing import Optional, Dict, Any
from .prompt import PREFIX_PROMPT, LOGIC_PROMPT, SUFFIX_PROMPT
from core.adapter import Tool_Executor


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


class Create_Deep_Reasoning_Tool_Calling_Agent:
    """
    Advanced AI Agent with deep reasoning, planning, and self-reflection capabilities.
    
    Features:
    - Deep Chain-of-Thought reasoning
    - Step-by-step planning before execution
    - Self-reflection and verification
    - Error recovery with alternative approaches
    - Confidence scoring
    - Detailed problem analysis
    """
    
    def __init__(
        self, 
        llm,
        verbose: bool = True,
        show_reasoning: bool = True,
        prompt: Optional[str] = None,
        memory = None,
        min_confidence: float = 0.7
    ) -> None:
        """
        Initialize Advanced Reasoning Agent.
        
        Args:
            llm: LLM object with generate_response(prompt) method
            verbose: Enable detailed output
            show_reasoning: Display reasoning process (highly recommended)
            prompt: Custom agent introduction (optional)
            memory: Optional memory object for conversation history
            min_confidence: Minimum confidence threshold (0.0-1.0) to accept results
        """
        self.tools = {}
        self.llm = llm
        self.verbose = verbose
        self.show_reasoning = show_reasoning
        self.memory = memory
        self.min_confidence = min_confidence
        
        if prompt is not None:
            self.prompt_template = prompt + "\n\n" + LOGIC_PROMPT + SUFFIX_PROMPT
        else:
            self.prompt_template = PREFIX_PROMPT + LOGIC_PROMPT + SUFFIX_PROMPT
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the advanced reasoning response into structured components.
        
        Returns:
            Dictionary with all reasoning components
        """
        # Extract JSON block
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
        if not json_match:
            json_match = re.search(r"'''json\s*(\{.*?\})\s*'''", response, re.DOTALL)
        
        if not json_match:
            raise ValueError(f"Invalid response format: No JSON block found")
        
        # Parse the comprehensive JSON structure
        parsed = json.loads(json_match.group(1))
        
        return {
            "problem_understanding": parsed.get("Problem Understanding", ""),
            "current_situation": parsed.get("Current Situation", ""),
            "deep_reasoning": parsed.get("Deep Reasoning", {}),
            "tool_decision": parsed.get("Tool Decision", {}),
            "tool_call": parsed.get("Tool call", "None"),
            "tool_parameters": parsed.get("Tool Parameters", {}),
            "self_reflection": parsed.get("Self-Reflection", {}),
            "final_response": parsed.get("Final Response", "None")
        }
    
    def _display_reasoning(self, components: Dict[str, Any], iteration: int):
        """Display the reasoning process in a beautiful, structured format."""
        if not self.show_reasoning:
            return
        
        print(f"\n{Colors.CYAN}{'═' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}🧠 Reasoning Iteration {iteration}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'═' * 70}{Colors.ENDC}\n")
        
        # Problem Understanding
        understanding = components.get("problem_understanding", "")
        if understanding:
            print(f"{Colors.MAGENTA}{Colors.BOLD}� Problem Understanding:{Colors.ENDC}")
            print(f"  {understanding}\n")
        
        # Current Situation
        situation = components.get("current_situation", "")
        if situation:
            print(f"{Colors.BLUE}{Colors.BOLD}📍 Current Situation:{Colors.ENDC}")
            print(f"  {situation}\n")
        
        # Deep Reasoning
        deep_reasoning = components.get("deep_reasoning", {})
        if deep_reasoning:
            print(f"{Colors.MAGENTA}{Colors.BOLD}💭 Deep Reasoning:{Colors.ENDC}")
            
            what_need = deep_reasoning.get("What I Need Now", "")
            if what_need:
                print(f"  {Colors.CYAN}What I Need Now:{Colors.ENDC}\n    {what_need}")
            
            why_need = deep_reasoning.get("Why I Need It", "")
            if why_need:
                print(f"  {Colors.CYAN}Why I Need It:{Colors.ENDC}\n    {why_need}")
            
            thought = deep_reasoning.get("Thought Process", "")
            if thought:
                print(f"  {Colors.CYAN}Thought Process:{Colors.ENDC}\n    {thought}")
            
            expected = deep_reasoning.get("Expected Outcome", "")
            if expected:
                print(f"  {Colors.CYAN}Expected Outcome:{Colors.ENDC}\n    {expected}")
            print()
        
        # Tool Decision
        tool_decision = components.get("tool_decision", {})
        if tool_decision:
            should_use = tool_decision.get("Should I Use A Tool", "")
            which_tool = tool_decision.get("Which Tool", "")
            why_tool = tool_decision.get("Why This Tool", "")
            what_next = tool_decision.get("What Happens Next", "")
            
            if should_use or which_tool:
                print(f"{Colors.YELLOW}{Colors.BOLD}� Tool Decision:{Colors.ENDC}")
                if should_use:
                    print(f"  {Colors.BLUE}Use Tool?{Colors.ENDC} {should_use}")
                if which_tool:
                    print(f"  {Colors.BLUE}Which Tool:{Colors.ENDC} {which_tool}")
                if why_tool:
                    print(f"  {Colors.BLUE}Why:{Colors.ENDC}\n    {why_tool}")
                if what_next:
                    print(f"  {Colors.BLUE}Next:{Colors.ENDC}\n    {what_next}")
                print()
        
        # Self-Reflection
        reflection = components.get("self_reflection", {})
        if reflection:
            confidence = reflection.get('Confidence', 'N/A')
            confidence_val = float(confidence) if isinstance(confidence, (int, float, str)) and str(confidence).replace('.', '').isdigit() else 0.0
            
            confidence_color = Colors.GREEN if confidence_val >= 0.8 else Colors.YELLOW if confidence_val >= 0.6 else Colors.RED
            
            print(f"{Colors.MAGENTA}{Colors.BOLD}🔍 Self-Reflection:{Colors.ENDC}")
            
            makes_sense = reflection.get('Does This Make Sense', '')
            if makes_sense:
                print(f"  {Colors.BLUE}Makes Sense?{Colors.ENDC} {makes_sense}")
            
            print(f"  {confidence_color}Confidence:{Colors.ENDC} {confidence}")
            
            issues = reflection.get('Potential Issues', [])
            if issues:
                print(f"  {Colors.YELLOW}⚠ Potential Issues:{Colors.ENDC}")
                for issue in issues:
                    print(f"    • {issue}")
            
            if_fails = reflection.get('If This Fails', '')
            if if_fails:
                print(f"  {Colors.CYAN}Backup Plan:{Colors.ENDC}\n    {if_fails}")
            print()
    
    def _display_tool_execution(self, tool_name: str, params: Dict, result: str):
        """Display tool execution information."""
        if self.verbose:
            print(f"{Colors.YELLOW}{Colors.BOLD}🔧 Tool Execution:{Colors.ENDC}")
            print(f"  {Colors.BLUE}Tool:{Colors.ENDC} {tool_name}")
            print(f"  {Colors.BLUE}Parameters:{Colors.ENDC} {params}")
            print(f"  {Colors.GREEN}Result:{Colors.ENDC} {result}")
            print()
    
    def add_tool(self, name: str, description: str, function):
        """Add a tool that the agent can use."""
        self.tools[name] = {
            "description": description,
            "function": function
        }
    
    def add_llm(self, llm):
        """Set or update the LLM instance."""
        self.llm = llm
    
    def add_memory(self, memory):
        """Set or update the memory instance."""
        self.memory = memory
    
    def clear_memory(self):
        """Clear conversation memory."""
        if self.memory is not None:
            self.memory.clear()
    
    def get_memory_history(self):
        """Get conversation history."""
        if self.memory is not None:
            return self.memory.get_history()
        return []
    
    def invoke(self, query: str) -> str:
        """
        Execute the agent with deep reasoning.
        
        Args:
            query: User's question or request
            
        Returns:
            Final response after reasoning and tool execution
        """
        if self.llm is None:
            raise ValueError("LLM not set. Call add_llm() first")
        
        if not self.tools:
            raise ValueError("No tools added. Call add_tool() at least once")
        
        # Add user query to memory
        if self.memory is not None:
            self.memory.add_user_message(query)
        
        # Compile prompt
        tool_list = "\n".join(
            [f"        - {name}: {info['description']}" 
             for name, info in self.tools.items()]
        )
        compiled_prompt = self.prompt_template.replace("{tool_list}", tool_list)
        
        # Add memory context
        memory_context = ""
        if self.memory is not None:
            context = self.memory.get_context()
            if context:
                memory_context = f"\n\n--- Previous Conversation ---\n{context}\n--- End History ---\n"
        
        if self.verbose:
            print(f"\n{Colors.GREEN}{'═' * 70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.GREEN}🚀 Advanced Reasoning Agent Activated{Colors.ENDC}")
            print(f"{Colors.GREEN}{'═' * 70}{Colors.ENDC}")
        
        scratchpad = ""
        max_iterations = 15  # More iterations for complex reasoning
        iteration = 0
        last_confidence = 1.0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Build context for this iteration
            context = memory_context + scratchpad
            prompt = compiled_prompt.format(user_input=query, context=context if context else "")
            
            # Get LLM response
            try:
                response = self.llm.generate_response(prompt)
                components = self._parse_response(response)
            except Exception as e:
                if self.verbose:
                    print(f"{Colors.RED}✗ Error parsing response: {str(e)}{Colors.ENDC}")
                return f"Error in reasoning process: {str(e)}"
            
            # Display reasoning
            self._display_reasoning(components, iteration)
            
            # Extract confidence
            reflection = components.get("self_reflection", {})
            confidence_str = reflection.get("Confidence", "1.0")
            try:
                confidence = float(confidence_str) if isinstance(confidence_str, (int, float, str)) and str(confidence_str).replace('.', '').isdigit() else 1.0
                last_confidence = confidence
            except:
                confidence = 1.0
            
            # Check if we have final response
            tool_name = components.get("tool_call")
            final_response = components.get("final_response")
            
            if tool_name == "None" or not tool_name:
                if final_response and final_response != "None":
                    # Add to memory
                    if self.memory is not None:
                        self.memory.add_ai_message(final_response)
                    
                    # Check confidence and warn if verbose
                    if confidence < self.min_confidence and self.verbose:
                        print(f"\n{Colors.YELLOW}⚠ Warning: Low confidence ({confidence}). "
                              f"Consider alternative approaches.{Colors.ENDC}\n")
                    
                    # Display final answer if verbose
                    if self.verbose:
                        print(f"{Colors.GREEN}{'═' * 70}{Colors.ENDC}")
                        print(f"{Colors.BOLD}{Colors.GREEN}✓ Final Answer (Confidence: {confidence}):{Colors.ENDC}")
                        print(f"{Colors.GREEN}{'═' * 70}{Colors.ENDC}")
                        print(f"\n{final_response}\n")
                    
                    return final_response
            
            # Execute tool
            params = components.get("tool_parameters", {})
            
            if tool_name and tool_name != "None":
                tool_result = Tool_Executor(tool_name, params, self.tools)
                self._display_tool_execution(tool_name, params, tool_result)
            else:
                tool_result = "No tool called"
            
            # Update scratchpad with detailed result
            scratchpad += f"\n\n{'─' * 70}\n"
            scratchpad += f"PREVIOUS ACTION (Iteration {iteration}):\n"
            if tool_name and tool_name != "None":
                scratchpad += f"Tool Used: {tool_name}\n"
                scratchpad += f"Parameters: {params}\n"
                scratchpad += f"Result: {tool_result}\n"
            scratchpad += f"{'─' * 70}\n\n"
            scratchpad += "Based on the above result, reason about your NEXT action:\n"
            scratchpad += "- What did you learn from this result?\n"
            scratchpad += "- Does it match your expectation?\n"
            scratchpad += "- What do you need to do NOW?\n"
            scratchpad += "- Can you provide the final answer, or do you need more information?\n\n"
        
        error_msg = f"Reasoning exceeded maximum iterations ({max_iterations}). Last confidence: {last_confidence}"
        if self.verbose:
            print(f"{Colors.RED}✗ {error_msg}{Colors.ENDC}")
        return error_msg
