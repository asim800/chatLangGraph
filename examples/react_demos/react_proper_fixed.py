#!/usr/bin/env python3
"""
React Pattern with Full LangGraph Conventions - Fixed Version
Demonstrates proper Thought/Action/Action Input/Observation/Final Answer loop
"""

import sys
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from tools.financial_tools import get_financial_tools

# Demo wrapper functions that add print statements for demonstration
def create_demo_tools():
    """Create demo versions of tools with enhanced logging"""
    from langchain_core.tools import tool
    
    @tool
    def calculate_risk(portfolio: str) -> str:
        """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
        print(f"🔧 EXECUTING: calculate_risk.invoke({{'portfolio': '{portfolio}'}})")
        
        # Use the centralized tool logic
        from tools.financial_tools import calculate_risk as base_calculate_risk
        result = base_calculate_risk.invoke({"portfolio": portfolio})
        
        print(f"📊 RESULT: {result}")
        return result

    @tool
    def get_stock_info(symbol: str) -> str:
        """Get basic stock information"""
        print(f"🔧 EXECUTING: get_stock_info.invoke({{'symbol': '{symbol}'}})")
        
        # Use the centralized tool logic
        from tools.financial_tools import get_stock_info as base_get_stock_info
        result = base_get_stock_info.invoke({"symbol": symbol})
        
        print(f"📊 RESULT: {result}")
        return result

    @tool
    def portfolio_analyzer(holdings: str) -> str:
        """Analyze portfolio diversification and provide recommendations"""
        print(f"🔧 EXECUTING: portfolio_analyzer.invoke({{'holdings': '{holdings}'}})")
        
        # Use the centralized tool logic
        from tools.financial_tools import portfolio_analyzer as base_portfolio_analyzer
        result = base_portfolio_analyzer.invoke({"holdings": holdings})
        
        print(f"📊 RESULT: Analysis completed")
        return result
    
    return [calculate_risk, get_stock_info, portfolio_analyzer]

def demonstrate_react_pattern():
    """Demonstrate the complete React pattern with LangGraph conventions"""
    
    print("🎯 REACT PATTERN WITH FULL LANGGRAPH CONVENTIONS")
    print("=" * 60)
    print("Using invoke() consistently for all components:")
    print("• PromptTemplate.invoke() - Prompt formatting")
    print("• ChatOpenAI.invoke() - LLM calls") 
    print("• Tool.invoke() - Tool execution")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    # Initialize components using LangGraph conventions
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = create_demo_tools()  # Use demo tools with enhanced logging
    tool_map = {tool.name: tool for tool in tools}
    
    # Create React prompt template using PromptTemplate (LangGraph convention)
    react_template = PromptTemplate(
        input_variables=["question", "tools", "tool_names"],
        template="""Answer the following question step by step using the React pattern.

Available tools:
{tools}

Tool names: {tool_names}

Use this exact format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the chosen action (just the parameter value)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {question}
"""
    )
    
    # Test question
    question = "What's the risk of my crypto portfolio with Bitcoin and Ethereum?"
    
    print(f"\n📝 Question: {question}")
    print("-" * 50)
    
    # Prepare tools description
    tool_descriptions = []
    for tool in tools:
        tool_descriptions.append(f"- {tool.name}: {tool.description}")
    tools_text = "\n".join(tool_descriptions)
    tool_names = [tool.name for tool in tools]
    
    # Use PromptTemplate.invoke() (LangGraph convention)
    prompt_input = {
        "question": question,
        "tools": tools_text,
        "tool_names": tool_names
    }
    
    print("🔧 USING: PromptTemplate.invoke()")
    formatted_prompt = react_template.invoke(prompt_input)
    
    print("📋 Generated prompt:")
    print("-" * 30)
    print(formatted_prompt.text)
    print("-" * 30)
    
    # Use ChatOpenAI.invoke() (LangGraph convention)
    print("\n🔧 USING: ChatOpenAI.invoke()")
    response = llm.invoke([HumanMessage(content=formatted_prompt.text)])
    
    print("🤖 LLM Response:")
    print("-" * 30)
    print(response.content)
    print("-" * 30)
    
    # Parse and execute the React pattern manually to show proper flow
    print("\n" + "=" * 60)
    print("🔍 MANUAL REACT PATTERN EXECUTION")
    print("=" * 60)
    
    # Step 1: Question
    print(f"❓ Question: {question}")
    
    # Step 2: Thought
    print("💭 Thought: I need to calculate the risk of a crypto portfolio containing Bitcoin and Ethereum")
    
    # Step 3: Action
    action = "calculate_risk"
    print(f"⚡ Action: {action}")
    
    # Step 4: Action Input
    action_input = "crypto portfolio with Bitcoin and Ethereum"
    print(f"📥 Action Input: {action_input}")
    
    # Step 5: Observation (using tool.invoke())
    print("🔧 USING: Tool.invoke()")
    if action in tool_map:
        tool = tool_map[action]
        observation = tool.invoke({"portfolio": action_input})
        print(f"👀 Observation: {observation}")
    
    # Step 6: Final Thought
    print("💭 Thought: I now know the final answer")
    
    # Step 7: Final Answer
    final_answer = f"Your crypto portfolio containing Bitcoin and Ethereum has a risk score of 0.8, which is considered HIGH risk. Cryptocurrency investments are highly volatile and can experience significant price swings."
    print(f"🎯 Final Answer: {final_answer}")

def demonstrate_all_tools():
    """Demonstrate all tools using invoke() method"""
    
    print("\n" + "=" * 60)
    print("🛠️  ALL TOOLS DEMONSTRATION")
    print("=" * 60)
    print("Each tool executed using tool.invoke() method")
    print()
    
    tools = create_demo_tools()  # Use demo tools with enhanced logging
    
    # Test cases for each tool
    test_cases = [
        {
            "tool_name": "calculate_risk",
            "input": {"portfolio": "crypto portfolio with Bitcoin and Ethereum"},
            "description": "Calculate risk for crypto portfolio"
        },
        {
            "tool_name": "get_stock_info", 
            "input": {"symbol": "AAPL"},
            "description": "Get Apple stock information"
        },
        {
            "tool_name": "portfolio_analyzer",
            "input": {"holdings": "AAPL, MSFT, Treasury bonds"},
            "description": "Analyze diversified portfolio"
        }
    ]
    
    tool_map = {tool.name: tool for tool in tools}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣  {test_case['description'].upper()}")
        print("-" * 40)
        
        print("💭 Thought: User wants " + test_case['description'].lower())
        print(f"⚡ Action: {test_case['tool_name']}")
        print(f"📥 Action Input: {test_case['input']}")
        
        # Use tool.invoke() (LangGraph convention)
        tool = tool_map[test_case['tool_name']]
        result = tool.invoke(test_case['input'])
        print(f"👀 Observation: {result}")
        
        if i < len(test_cases):
            print()

def show_complete_react_loop():
    """Show complete React loop with multiple steps"""
    
    print("\n" + "=" * 60)
    print("🔄 COMPLETE REACT LOOP WITH MULTIPLE STEPS")
    print("=" * 60)
    
    question = "Get AAPL stock info and calculate the risk if I put it in my portfolio"
    
    print(f"❓ Question: {question}")
    print()
    
    # Get demo tools for this demonstration
    demo_tools = create_demo_tools()
    tool_map = {tool.name: tool for tool in demo_tools}
    
    # Step 1: Get stock info
    print("💭 Thought: I need to first get information about AAPL stock")
    print("⚡ Action: get_stock_info")
    print("📥 Action Input: AAPL")
    
    stock_result = tool_map["get_stock_info"].invoke({"symbol": "AAPL"})
    print(f"👀 Observation: {stock_result}")
    print()
    
    # Step 2: Calculate risk
    print("💭 Thought: Now I need to calculate the risk of having AAPL in my portfolio")
    print("⚡ Action: calculate_risk")
    print("📥 Action Input: stock portfolio with AAPL")
    
    risk_result = tool_map["calculate_risk"].invoke({"portfolio": "stock portfolio with AAPL"})
    print(f"👀 Observation: {risk_result}")
    print()
    
    # Step 3: Final answer
    print("💭 Thought: I now know the final answer")
    print("🎯 Final Answer: Based on my analysis, AAPL (Apple Inc.) is currently trading at $150.25 with a +2.5% gain today and has a Strong Buy rating. If you add AAPL to your portfolio, it would have a moderate risk score of 0.6, as stock investments typically have moderate volatility. This makes AAPL a relatively solid choice for a balanced portfolio.")

def main():
    """Main demonstration function"""
    
    print("🚀 REACT PATTERN WITH LANGGRAPH CONVENTIONS")
    print("="*80)
    print("This demonstration shows:")
    print("• Complete Thought/Action/Action Input/Observation/Final Answer loop")
    print("• Consistent use of invoke() method for ALL components")
    print("• @tool decorator usage (LangGraph recommended)")
    print("• PromptTemplate.invoke() for prompt formatting")
    print("• ChatOpenAI.invoke() for LLM calls")
    print("• Tool.invoke() for tool execution")
    print("="*80)
    
    # Main demonstrations
    demonstrate_react_pattern()
    demonstrate_all_tools()
    show_complete_react_loop()
    
    print("\n" + "="*80)
    print("✅ REACT PATTERN DEMONSTRATION COMPLETE!")
    print("\n🔧 LangGraph Conventions Used:")
    print("   • @tool decorators for all tools")
    print("   • PromptTemplate.invoke() for prompt formatting")
    print("   • ChatOpenAI.invoke() for LLM execution")
    print("   • Tool.invoke() for tool calls")
    print("   • Consistent invoke() pattern throughout")
    print("\n💡 React Pattern Components Shown:")
    print("   • Question: Input question")
    print("   • Thought: Reasoning step")
    print("   • Action: Tool to execute")
    print("   • Action Input: Tool parameters")
    print("   • Observation: Tool results")
    print("   • Final Answer: Complete response")
    print("="*80)

if __name__ == "__main__":
    main()