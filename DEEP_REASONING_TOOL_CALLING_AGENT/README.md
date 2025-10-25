# 🧠 Deep Reasoning Tool Calling Agent

An advanced AI agent with **deep chain-of-thought reasoning**, dynamic problem analysis, self-reflection, and error recovery capabilities.

## 📋 Overview

The `Create_Deep_Reasoning_Tool_Calling_Agent` provides sophisticated reasoning capabilities that go far beyond simple tool execution. Unlike basic agents that simply call tools, this agent:

- **Understands** the problem deeply before acting
- **Analyzes** the current situation dynamically at each step
- **Reasons** through complex multi-step problems
- **Reflects** on its decisions with confidence scoring
- **Recovers** from errors with alternative approaches

**⚡ Performance Note:** This agent is ~2.4x slower than the basic reasoning agent but provides significantly deeper transparency and reasoning capabilities. Use it when you need to understand *how* the AI is thinking, not just *what* it's doing.

## ✨ Key Features

### 1. **Problem Understanding**
- Deeply analyzes the user's query
- Identifies key requirements and constraints
- Breaks down complex questions into components
- Understands the real intent behind questions

### 2. **Current Situation Awareness**
- Tracks what information has been gathered
- Identifies what's still missing
- Shows progress toward the goal
- Adapts reasoning based on context

### 3. **Deep Reasoning Process**
- **What I Need Now:** Identifies immediate requirements
- **Why I Need It:** Explains the reasoning behind each action
- **Thought Process:** Shows step-by-step logical thinking
- **Expected Outcome:** Predicts what will happen

### 4. **Tool Decision Logic**
- Explains why a specific tool is chosen
- Details what parameters to use and why
- Shows how the tool output will be used

### 5. **Self-Reflection & Verification**
- Provides confidence scoring (0.0-1.0)
- Plans for error recovery ("If This Fails")
- Questions if its approach makes sense
- Transparent about uncertainty

### 6. **Error Recovery**
- Doesn't give up on first failure
- Analyzes errors and adjusts parameters
- Tries alternative tools if needed
- Maintains reasoning even when tools fail

## 🆚 Comparison: Reasoning vs Deep Reasoning Agent

| Feature | REASONING Agent | DEEP_REASONING Agent |
|---------|-----------------|----------------------|
| **Speed** | ⚡ Fast (4.63s avg) | 🐢 Slower (11.11s avg) |
| **Token Usage** | 💰 Low (600-900) | 💸 High (1500-2800) |
| **Thinking Display** | ✅ Basic | ✅ Deep chain-of-thought |
| **Problem Analysis** | ❌ None | ✅ Comprehensive breakdown |
| **Situation Awareness** | ❌ None | ✅ Dynamic context tracking |
| **Reasoning Depth** | ⚠️ Surface-level | ✅ Multi-layered reasoning |
| **Self-Reflection** | ❌ None | ✅ Confidence + alternatives |
| **Error Recovery** | ⚠️ Basic retry | ✅ Strategic alternatives |
| **Best For** | Production APIs | Research & Debugging |
| Verification | ❌ None | ✅ Checks results make sense |
| Ambiguity Handling | ❌ Limited | ✅ Identifies unclear aspects |

## 📖 Usage

```python
from DEEP_REASONING_TOOL_CALLING_AGENT.agent import Create_Deep_Reasoning_Tool_Calling_Agent
from llm.Google_llm import GoogleLLM

# Initialize LLM
llm = GoogleLLM(
    model="gemini-2.0-flash-thinking-exp-1219",
    api_key="your-api-key"
)

# Create deep reasoning agent
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    verbose=True,              # Show detailed output
    show_reasoning=True,       # Display reasoning process
    min_confidence=0.7         # Minimum confidence threshold
)

# Add tools
def calculator(expression):
    return str(eval(expression))

agent.add_tool(
    "calculator",
    "Evaluate mathematical expressions",
    calculator
)

# Use the agent
response = agent.invoke(
    "If I have 100 apples and give away 23%, "
    "then buy 50 more, how many do I have?"
)
```

## 🎯 Best Use Cases

1. **Complex Multi-Step Problems**
   - Math word problems
   - Multi-stage calculations
   - Problems requiring verification

2. **Ambiguous Queries**
   - Questions with unclear requirements
   - Situations needing clarification
   - Edge case handling

3. **High-Stakes Decisions**
   - When accuracy is critical
   - When you need to see the reasoning
   - When transparency matters

4. **Learning & Education**
   - Show step-by-step working
   - Explain mathematical processes
   - Demonstrate problem-solving approaches

## 🔧 Configuration Options

```python
Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,                   # Required: LLM instance
    verbose=True,              # Show detailed logs
    show_reasoning=True,       # Display reasoning (recommended!)
    prompt=None,               # Custom agent introduction
    memory=None,               # Memory instance for history
    min_confidence=0.7         # Confidence threshold (0.0-1.0)
)
```

## 📊 Output Structure

The agent provides rich, structured reasoning:

```
🧠 Reasoning Iteration 1
═══════════════════════════════════════════════════════════════════════

📊 Problem Analysis:
  Understanding: Calculate percentage decrease, then addition
  Complexity: moderate
  Key Components:
    • Percentage calculation
    • Subtraction
    • Addition

📋 Execution Plan:
  ▸ Step 1: Calculate 23% of 100 apples
  ▸ Step 2: Subtract from original amount
  ▸ Step 3: Add 50 more apples
  ▸ Step 4: Verify result is reasonable

💭 Deep Reasoning:
  Current Step: Step 1
  Thought Process: Need to find 23% of 100. That's 0.23 × 100 = 23 apples
  Why This Approach: Percentage calculations require decimal conversion
  Expected Outcome: Should get 23 apples to subtract

🔍 Self-Reflection:
  Makes Sense? Yes, percentage logic is sound
  Confidence: 0.95
  🔄 Alternatives:
    • Could break into multiple calculator calls
    • Could calculate mentally and verify with tool
```

## ⚡ Performance Notes

- **More tokens**: Deep reasoning uses more LLM tokens
- **Slower**: Thoroughness takes time
- **More accurate**: Catches errors early
- **Better for complex tasks**: Overkill for simple queries

## 🎓 When to Use Each Agent

**Use REASONING_TOOL_CALLING_AGENT for:**
- Simple tool calls
- Fast responses needed
- Straightforward queries
- Cost-sensitive applications
- Production APIs with latency requirements

**Use DEEP_REASONING_TOOL_CALLING_AGENT for:**
- Complex multi-step problems
- When you need to see reasoning
- High-accuracy requirements
- Learning and education
- Debugging and verification
- Research and analysis

## 🚀 Advanced Features

### Memory Integration

```python
from memory import ConversationalWindowMemory

memory = ConversationalWindowMemory(window_size=10)
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, memory=memory)
```

### Custom Prompts

```python
custom_prompt = "You are a mathematics tutor who explains step-by-step."
agent = Create_Deep_Reasoning_Tool_Calling_Agent(llm=llm, prompt=custom_prompt)
```

### Confidence Monitoring

```python
# Set high confidence threshold for critical tasks
agent = Create_Deep_Reasoning_Tool_Calling_Agent(
    llm=llm,
    min_confidence=0.9  # Warn if confidence < 90%
)
```

## 📝 Example Queries

### Simple (but with full reasoning)
```python
agent.invoke("What is 144 divided by 12?")
```

### Complex
```python
agent.invoke(
    "If a train travels at 80 km/h for 2.5 hours, "
    "then increases speed by 20% for another 1.5 hours, "
    "what's the total distance? Show your calculations."
)
```

### Ambiguous
```python
agent.invoke(
    "Compare the length of 'Hello World' with the number "
    "of words in 'Artificial Intelligence is Amazing'"
)
```

## 🎯 Design Philosophy

This agent embodies:
- **Transparency**: Shows all reasoning
- **Thoroughness**: Doesn't skip steps
- **Self-awareness**: Questions its own logic
- **Reliability**: Verifies before answering
- **Adaptability**: Recovers from errors

---

**Built by codexjitin** | Part of the Codemni AI Agent Framework
