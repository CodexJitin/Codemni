from TOOL_CALLING_AGENT.agent import Create_ToolCalling_Agent
from llm.Google_llm import GoogleLLM
import datetime
import random

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash",
    api_key="AIzaSyBsL27HZNz7yhDahKfLxAwuftXc480275o"  # or set GOOGLE_API_KEY env var
)

# Create agent
agent = Create_ToolCalling_Agent(llm=llm)

# Define multiple tools
def calculator(expression):
    """Evaluate mathematical expressions"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_time():
    """Get the current date and time"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_day_of_week(date_string):
    """Get the day of the week for a given date (format: YYYY-MM-DD)"""
    try:
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.strftime("%A")
    except Exception as e:
        return f"Error: {str(e)}. Please use YYYY-MM-DD format."

def generate_random_number(min_val, max_val):
    """Generate a random number between min and max (inclusive)"""
    try:
        min_int = int(min_val)
        max_int = int(max_val)
        return str(random.randint(min_int, max_int))
    except Exception as e:
        return f"Error: {str(e)}"

def string_length(text):
    """Calculate the length of a string"""
    return str(len(text))

def reverse_string(text):
    """Reverse a string"""
    return text[::-1]

def word_count(text):
    """Count the number of words in a text"""
    return str(len(text.split()))

def to_uppercase(text):
    """Convert text to uppercase"""
    return text.upper()

def temperature_converter(temperature, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    try:
        temp = float(temperature)
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        # Convert to Celsius first
        if from_unit == 'F':
            celsius = (temp - 32) * 5/9
        elif from_unit == 'K':
            celsius = temp - 273.15
        else:
            celsius = temp
        
        # Convert from Celsius to target
        if to_unit == 'F':
            result = (celsius * 9/5) + 32
        elif to_unit == 'K':
            result = celsius + 273.15
        else:
            result = celsius
        
        return f"{result:.2f} {to_unit}"
    except Exception as e:
        return f"Error: {str(e)}"

# Add tools to agent
agent.add_tool("calculator", "Evaluate mathematical expressions like addition, subtraction, multiplication, division, etc.", calculator)
agent.add_tool("get_current_time", "Get the current date and time", get_current_time)
agent.add_tool("get_day_of_week", "Get the day of the week for a given date in YYYY-MM-DD format", get_day_of_week)
agent.add_tool("generate_random_number", "Generate a random number between a minimum and maximum value", generate_random_number)
agent.add_tool("string_length", "Calculate the length of a string", string_length)
agent.add_tool("reverse_string", "Reverse a string", reverse_string)
agent.add_tool("word_count", "Count the number of words in a text", word_count)
agent.add_tool("to_uppercase", "Convert text to uppercase", to_uppercase)
agent.add_tool("temperature_converter", "Convert temperature between Celsius (C), Fahrenheit (F), and Kelvin (K)", temperature_converter)

# Test with complex queries that require multiple tool calls
print("\n" + "="*70)
print("Test 1: Simple Calculation")
print("="*70)
response = agent.invoke("What is 125 * 48?")
print(response)

print("\n" + "="*70)
print("Test 2: Multiple Operations")
print("="*70)
response = agent.invoke("Calculate (100 + 50) * 2, then tell me if the result is greater than 250")
print(response)

print("\n" + "="*70)
print("Test 3: String Operations")
print("="*70)
response = agent.invoke("Reverse the string 'Hello World', then count how many characters are in the reversed string, and convert it to uppercase")
print(response)

print("\n" + "="*70)
print("Test 4: Date and Random")
print("="*70)
response = agent.invoke("What day of the week was 2025-01-01? Also generate a random number between 1 and 100")
print(response)

print("\n" + "="*70)
print("Test 5: Temperature Conversion Chain")
print("="*70)
response = agent.invoke("Convert 100 degrees Fahrenheit to Celsius, then convert that result to Kelvin")
print(response)

print("\n" + "="*70)
print("Test 6: Complex Multi-Tool Query")
print("="*70)
response = agent.invoke("What is the current time? Then calculate 15 * 23, and tell me how many words are in the sentence 'Artificial Intelligence is transforming the world'")
print(response)