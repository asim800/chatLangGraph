#!/usr/bin/env python3
"""
React Pattern Demo - Properly formatted Thought/Action/Action Input/Observation/Final Answer
Uses LangGraph recommended patterns with @tool decorators and invoke methods
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from prompts import render_template_with_tools

# Define tools using @tool decorator (LangGraph recommended pattern)
@tool
def calculate_risk(portfolio: str) -> str:
    """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
    if "crypto" in portfolio.lower() or "bitcoin" in portfolio.lower():
        return "0.8 (HIGH risk) - Cryptocurrency investments are highly volatile"
    elif "bonds" in portfolio.lower() or "treasury" in portfolio.lower():
        return "0.2 (LOW risk) - Government bonds are stable investments"
    elif "stocks" in portfolio.lower() or "equity" in portfolio.lower():
        return "0.6 (MODERATE risk) - Stock investments have moderate volatility"
    else:
        return "0.4 (MODERATE risk) - Mixed portfolio with balanced risk"

@tool
def get_stock_info(symbol: str) -> str:
    """Get basic stock information"""
    stock_data = {
        "AAPL": "Apple Inc. - Current: $150.25, +2.5% today, Strong Buy rating",
        "MSFT": "Microsoft Corp. - Current: $300.75, +1.2% today, Buy rating", 
        "TSLA": "Tesla Inc. - Current: $200.50, -3.1% today, Hold rating",
        "SPY": "S&P 500 ETF - Current: $400.80, +0.8% today"
    }
    return stock_data.get(symbol.upper(), f"Stock data for {symbol} not available")

@tool
def portfolio_analyzer(holdings: str) -> str:
    """Analyze portfolio diversification and provide recommendations"""
    return f"""Portfolio Analysis: {holdings}
- Diversification: Good sector mix
- Risk Level: Moderate (0.45/1.0)  
- Expected Return: 8-12% annually
- Recommendation: Add international exposure"""

def demonstrate_react_pattern():
    """Demonstrate the complete React pattern with proper formatting"""
    
    print("🔬 React Pattern Demonstration")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    # Initialize LLM with tools
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [calculate_risk, get_stock_info, portfolio_analyzer]
    
    # Create React prompt
    react_prompt = render_template_with_tools(
        "react_prompt",
        tools=tools,
        formatter_strategy="detailed",
        input="What's the risk of my crypto portfolio with Bitcoin and Ethereum?"
    )
    
    print("📝 Using React Prompt Template:")
    print("-" * 30)
    print(react_prompt)
    print("-" * 30)
    
    try:
        # Use invoke method (LangGraph recommended pattern)
        print("\n🤖 INVOKING LLM...")
        response = llm.invoke([HumanMessage(content=react_prompt)])
        
        print("\n📋 LLM RESPONSE (React Pattern):")
        print("=" * 50)
        print(response.content)
        print("=" * 50)
        
        # Parse and demonstrate each component
        lines = response.content.split('\n')
        
        print("\n🔍 PARSED REACT COMPONENTS:")
        print("-" * 40)
        
        for line in lines:
            line = line.strip()
            if line.startswith("Question:"):
                print(f"❓ {line}")
            elif line.startswith("Thought:"):
                print(f"💭 {line}")
            elif line.startswith("Action:"):
                print(f"⚡ {line}")
            elif line.startswith("Action Input:"):
                print(f"📥 {line}")
            elif line.startswith("Observation:"):
                print(f"👀 {line}")
            elif line.startswith("Final Answer:"):
                print(f"🎯 {line}")
        
        # Now let's manually execute the tools to show the complete loop
        print("\n" + "=" * 50)
        print("🔧 MANUAL TOOL EXECUTION DEMO:")
        print("=" * 50)
        
        print("💭 Thought: I need to calculate the risk of a crypto portfolio containing Bitcoin and Ethereum.")
        print("⚡ Action: calculate_risk")
        print("📥 Action Input: portfolio=\"crypto portfolio with Bitcoin and Ethereum\"")
        
        # Use invoke method on the tool (LangGraph recommended pattern)
        risk_result = calculate_risk.invoke({"portfolio": "crypto portfolio with Bitcoin and Ethereum"})
        print(f"👀 Observation: {risk_result}")
        
        print("💭 Thought: I now know the final answer about the crypto portfolio risk.")
        print("🎯 Final Answer: Your crypto portfolio containing Bitcoin and Ethereum has a high risk score of 0.8. Cryptocurrency investments are highly volatile and should be considered high-risk investments. This means there's significant potential for both gains and losses.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your OpenAI API key is valid")

def show_all_tools_demo():
    """Demonstrate all tools using the invoke method"""
    print("\n" + "=" * 60)
    print("🛠️  ALL TOOLS DEMONSTRATION (using invoke method)")
    print("=" * 60)
    
    tools = [calculate_risk, get_stock_info, portfolio_analyzer]
    
    # Demo 1: Calculate Risk Tool
    print("\n1️⃣  CALCULATE_RISK TOOL:")
    print("💭 Thought: User wants to know portfolio risk")
    print("⚡ Action: calculate_risk")
    print("📥 Action Input: {\"portfolio\": \"mixed portfolio with stocks and bonds\"}")
    result1 = calculate_risk.invoke({"portfolio": "mixed portfolio with stocks and bonds"})
    print(f"👀 Observation: Risk assessment shows {result1}")
    
    # Demo 2: Stock Info Tool  
    print("\n2️⃣  GET_STOCK_INFO TOOL:")
    print("💭 Thought: User needs current stock information")
    print("⚡ Action: get_stock_info")
    print("📥 Action Input: {\"symbol\": \"AAPL\"}")
    result2 = get_stock_info.invoke({"symbol": "AAPL"})
    print(f"👀 Observation: {result2}")
    
    # Demo 3: Portfolio Analyzer Tool
    print("\n3️⃣  PORTFOLIO_ANALYZER TOOL:")
    print("💭 Thought: User wants comprehensive portfolio analysis")
    print("⚡ Action: portfolio_analyzer") 
    print("📥 Action Input: {\"holdings\": \"AAPL, MSFT, Treasury bonds\"}")
    result3 = portfolio_analyzer.invoke({"holdings": "AAPL, MSFT, Treasury bonds"})
    print(f"👀 Observation: {result3}")
    
    print("\n💭 Thought: I have analyzed all the requested portfolio components")
    print("🎯 Final Answer: Complete portfolio analysis has been provided with risk assessments, stock information, and diversification recommendations.")

def main():
    """Main demonstration function"""
    print("🎯 REACT PATTERN WITH LANGGRAPH BEST PRACTICES")
    print("=" * 60)
    print("This demo shows:")
    print("• Complete Thought/Action/Action Input/Observation/Final Answer loop")
    print("• @tool decorator usage (LangGraph recommended)")
    print("• invoke() method for all tool calls (LangGraph recommended)")
    print("• Proper React prompt template integration")
    print("=" * 60)
    
    # Main demonstration
    demonstrate_react_pattern()
    
    # Show all tools
    show_all_tools_demo()
    
    print("\n" + "=" * 60)
    print("✅ REACT PATTERN DEMONSTRATION COMPLETE!")
    print("💡 Key LangGraph patterns used:")
    print("   • @tool decorators for all tools")
    print("   • tool.invoke(args) method for execution")
    print("   • Structured React prompt template")
    print("   • Clear Thought → Action → Observation → Final Answer flow")

if __name__ == "__main__":
    main()