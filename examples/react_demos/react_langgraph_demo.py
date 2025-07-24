#!/usr/bin/env python3
"""
React Pattern Demo with LangGraph Recommended Patterns
Demonstrates proper Thought/Action/Action Input/Observation/Final Answer loop
"""

import sys
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from prompts import render_template_with_tools

# Define tools using @tool decorator (LangGraph recommended pattern)
@tool
def calculate_risk(portfolio: str) -> str:
    """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
    print(f"🔧 TOOL EXECUTION: calculate_risk(portfolio='{portfolio}')")
    
    if "crypto" in portfolio.lower() or "bitcoin" in portfolio.lower():
        risk_score = 0.8
        risk_level = "HIGH"
    elif "bonds" in portfolio.lower() or "treasury" in portfolio.lower():
        risk_score = 0.2
        risk_level = "LOW"
    elif "stocks" in portfolio.lower() or "equity" in portfolio.lower():
        risk_score = 0.6
        risk_level = "MODERATE"
    else:
        risk_score = 0.4
        risk_level = "MODERATE"
    
    result = f"Risk Score: {risk_score} ({risk_level} risk)"
    print(f"📊 TOOL RESULT: {result}")
    return result

@tool
def get_stock_info(symbol: str) -> str:
    """Get basic stock information"""
    print(f"🔧 TOOL EXECUTION: get_stock_info(symbol='{symbol}')")
    
    stock_data = {
        "AAPL": "Apple Inc. - Current: $150.25, +2.5% today, Strong Buy rating",
        "MSFT": "Microsoft Corp. - Current: $300.75, +1.2% today, Buy rating", 
        "TSLA": "Tesla Inc. - Current: $200.50, -3.1% today, Hold rating",
        "SPY": "S&P 500 ETF - Current: $400.80, +0.8% today, Diversified index fund"
    }
    
    result = stock_data.get(symbol.upper(), f"Stock data for {symbol} not available in demo database")
    print(f"📊 TOOL RESULT: {result}")
    return result

@tool
def portfolio_analyzer(holdings: str) -> str:
    """Analyze portfolio diversification and provide recommendations"""
    print(f"🔧 TOOL EXECUTION: portfolio_analyzer(holdings='{holdings}')")
    
    analysis = f"""Portfolio Analysis for: {holdings}

✅ Diversification: Good mix across sectors
📊 Risk Level: Moderate (0.45/1.0)  
💰 Expected Return: 8-12% annually
🎯 Recommendation: Consider adding international exposure

Key Insights:
- Well balanced between growth and value
- Good sector diversification  
- Consider adding 10-15% international stocks
- Emergency fund should be 6 months expenses"""
    
    print(f"📊 TOOL RESULT: Analysis completed")
    return analysis.strip()

# State definition for LangGraph
class AgentState(TypedDict):
    messages: list
    question: str
    thoughts: list
    actions: list
    observations: list
    final_answer: str

def create_react_agent():
    """Create a React agent using LangGraph recommended patterns"""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Get all tools
    tools = [calculate_risk, get_stock_info, portfolio_analyzer]
    
    # Bind tools to LLM (LangGraph recommended pattern)
    llm_with_tools = llm.bind_tools(tools)
    
    # Create the system prompt using react_prompt template
    system_prompt = render_template_with_tools(
        "react_prompt", 
        tools=tools, 
        formatter_strategy="detailed",
        input="{input}"
    )
    
    def agent_node(state: AgentState) -> AgentState:
        """Main agent reasoning node"""
        question = state["question"]
        
        # Format the prompt with the actual question
        formatted_prompt = system_prompt.format(input=question)
        
        print("🤖 AGENT THINKING...")
        print("=" * 60)
        
        # Use invoke method (LangGraph recommended pattern)
        response = llm_with_tools.invoke([HumanMessage(content=formatted_prompt)])
        
        # Parse and display the React pattern steps
        content = response.content
        print("📝 AGENT RESPONSE:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        # Extract React pattern components (simple parsing)
        lines = content.split('\n')
        thoughts = []
        actions = []
        observations = []
        final_answer = ""
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                current_section = "thought"
                thoughts.append(line[8:].strip())
                print(f"💭 {line}")
            elif line.startswith("Action:"):
                current_section = "action"
                actions.append(line[7:].strip())
                print(f"⚡ {line}")
            elif line.startswith("Action Input:"):
                current_section = "action_input"
                print(f"📥 {line}")
            elif line.startswith("Observation:"):
                current_section = "observation"
                observations.append(line[12:].strip())
                print(f"👀 {line}")
            elif line.startswith("Final Answer:"):
                final_answer = line[13:].strip()
                print(f"🎯 {line}")
            elif current_section and line:
                if current_section == "thought":
                    thoughts[-1] += " " + line
                elif current_section == "observation":
                    observations[-1] += " " + line
                elif current_section == "final_answer":
                    final_answer += " " + line
        
        # Handle tool calls if present
        if response.tool_calls:
            print("\n🔧 EXECUTING TOOLS:")
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                print(f"   Calling {tool_name} with args: {tool_args}")
                
                # Find and invoke the tool (LangGraph recommended pattern)
                for tool in tools:
                    if tool.name == tool_name:
                        try:
                            result = tool.invoke(tool_args)
                            print(f"   ✅ Result: {result}")
                            observations.append(f"Tool {tool_name} returned: {result}")
                        except Exception as e:
                            print(f"   ❌ Error: {e}")
                            observations.append(f"Tool {tool_name} failed: {e}")
                        break
        
        return {
            **state,
            "messages": state["messages"] + [response],
            "thoughts": thoughts,
            "actions": actions,
            "observations": observations,
            "final_answer": final_answer
        }
    
    # Create the graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    return workflow.compile()

def demonstrate_react_pattern(question: str):
    """Demonstrate the React pattern with proper output formatting"""
    print("🔬 React Pattern Demo with LangGraph")
    print("=" * 50)
    print(f"📝 Question: {question}")
    print("=" * 50)
    
    # Create the React agent
    agent = create_react_agent()
    
    # Initial state
    initial_state = {
        "messages": [],
        "question": question,
        "thoughts": [],
        "actions": [],
        "observations": [],
        "final_answer": ""
    }
    
    try:
        # Use invoke method (LangGraph recommended pattern)
        result = agent.invoke(initial_state)
        
        print("\n" + "=" * 50)
        print("📋 REACT PATTERN SUMMARY:")
        print("=" * 50)
        
        # Display the structured React components
        if result["thoughts"]:
            print("💭 THOUGHTS:")
            for i, thought in enumerate(result["thoughts"], 1):
                print(f"   {i}. {thought}")
        
        if result["actions"]:
            print("\n⚡ ACTIONS:")
            for i, action in enumerate(result["actions"], 1):
                print(f"   {i}. {action}")
        
        if result["observations"]:
            print("\n👀 OBSERVATIONS:")
            for i, obs in enumerate(result["observations"], 1):
                print(f"   {i}. {obs}")
        
        if result["final_answer"]:
            print(f"\n🎯 FINAL ANSWER:")
            print(f"   {result['final_answer']}")
        
        print("\n✅ React pattern demonstration completed!")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("💡 Make sure your OpenAI API key is valid")

def main():
    """Main function to run the React pattern demo"""
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("💡 Create a .env file with: OPENAI_API_KEY=your-key-here")
        return
    
    # Demo questions showcasing the React pattern
    demo_questions = [
        "What's the risk of my crypto portfolio with Bitcoin and Ethereum?",
        "Get me information about AAPL stock",
        "Analyze my portfolio with AAPL, MSFT, and Treasury bonds"
    ]
    
    print("🎯 Available demo questions:")
    for i, q in enumerate(demo_questions, 1):
        print(f"   {i}. {q}")
    
    print("\n" + "="*60)
    
    # Run demonstration with the first question
    demonstrate_react_pattern(demo_questions[0])
    
    print("\n" + "="*60)
    print("💡 This demo shows the proper React pattern:")
    print("   • Thought: Agent reasoning")
    print("   • Action: Tool to use") 
    print("   • Action Input: Tool parameters")
    print("   • Observation: Tool results")
    print("   • Final Answer: Conclusion")
    print("\n🔧 Uses LangGraph recommended patterns:")
    print("   • @tool decorator for tools")
    print("   • invoke() method for execution")
    print("   • Proper state management")
    print("   • Tool binding with llm.bind_tools()")

if __name__ == "__main__":
    main()