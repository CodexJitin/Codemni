import json

def Tool_Executor(tool_name, tool_parameters, available_tools):
    """
    Execute a tool function with the provided parameters.
    
    Args:
        tool_name: Name of the tool to execute
        tool_parameters: Parameters in format {"value1,value2,..."} or {"key": "value"} or "None"
        available_tools: Dictionary of available tools with their functions
        
    Returns:
        Result from tool execution or error message
    """
    if tool_name not in available_tools:
        return f"Error: Tool '{tool_name}' not found"
    
    tool_function = available_tools[tool_name]["function"]
    
    # Handle no parameters case
    if not tool_parameters or tool_parameters == "None":
        return tool_function()
    
    # Parse parameters if string
    if isinstance(tool_parameters, str):
        try:
            tool_parameters = json.loads(tool_parameters)
        except json.JSONDecodeError:
            return f"Error: Invalid parameter format"
    
    # Extract and handle parameters
    try:
        if isinstance(tool_parameters, dict):
            # Check if it's a key-value dict (like {"expression": "125 * 48"})
            if len(tool_parameters) > 0:
                first_key = list(tool_parameters.keys())[0]
                first_value = tool_parameters[first_key]
                
                # If the key looks like a parameter name (contains letters), treat as kwargs
                if first_key and any(c.isalpha() for c in first_key):
                    # Key-value parameters like {"expression": "125 * 48"}
                    return tool_function(**tool_parameters)
                else:
                    # Comma-separated parameters like {"125 * 48"} or {"value1,value2"}
                    param_string = first_value if first_value else first_key
                    params = [p.strip() for p in str(param_string).split(',')]
                    return tool_function(*params)
            else:
                return tool_function()
        elif isinstance(tool_parameters, set):
            param_string = list(tool_parameters)[0]
            params = [p.strip() for p in str(param_string).split(',')]
            return tool_function(*params)
        else:
            return f"Error: Unexpected parameter type"
            
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"