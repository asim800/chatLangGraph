#!/usr/bin/env python3
"""
Simple example showing tool-enabled prompt templates
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from prompts import render_template_with_tools, get_template_variables


# Define simple financial tools
@tool  
def triple(num: float) -> float:
    """
    Triple the input number
    
    Args:
        num: input number
    
    Returns:
        the triple of the input
    """
    return float(num) * 3


@tool
def portfolio_risk_calculator(portfolio: str) -> str:
    """
    Calculate portfolio risk metrics
    
    Args:
        portfolio: Portfolio description
        
    Returns:
        Risk assessment string
    """
    return f"Portfolio '{portfolio}' has moderate risk (0.35) with good diversification."


@tool
def market_sentiment_analyzer(symbol: str) -> str:
    """
    Analyze market sentiment for a stock symbol
    
    Args:
        symbol: Stock symbol (e.g., AAPL)
        
    Returns:
        Sentiment analysis result
    """
    return f"Market sentiment for {symbol}: Bullish (75% positive sentiment based on recent news)"


def main():
    print("🧪 Tool-Enabled Prompt Template Example")
    print("=" * 45)
    
    # Our tools
    tools = [triple, portfolio_risk_calculator, market_sentiment_analyzer]
    
    print(f"\n🔧 Available tools: {[tool.name for tool in tools]}")
    
    # Show what variables the finchat_prompt needs
    print(f"\n📝 finchat_prompt variables: {get_template_variables('finchat_prompt')}")
    
    # Render the template with tools
    print("\n🎯 Rendering finchat_prompt with tools...")
    try:
        rendered_prompt = render_template_with_tools(
            "finchat_prompt",
            tools=tools
        )
        
        print("✅ Success!")
        print(f"\n📏 Rendered prompt length: {len(rendered_prompt)} characters")
        print(f"📊 Word count: {len(rendered_prompt.split())} words")
        
        print("\n📋 Rendered Prompt Preview:")
        print("=" * 50)
        # Show first 500 characters
        preview = rendered_prompt[:500] + "..." if len(rendered_prompt) > 500 else rendered_prompt
        print(preview)
        print("=" * 50)
        
        # Show how tools were injected
        tool_names_section = "You have access to the following tools:\ntriple, portfolio_risk_calculator, market_sentiment_analyzer"
        if "triple" in rendered_prompt:
            print("\n✅ Tools successfully injected into prompt!")
            print("🔍 Found tool names in the template")
        
        # Save to file for inspection
        with open("rendered_finchat_prompt.txt", "w") as f:
            f.write(rendered_prompt)
        print(f"\n💾 Full rendered prompt saved to: rendered_finchat_prompt.txt")
        
    except Exception as e:
        print(f"❌ Error rendering template: {e}")
    
    # Show different tool formatting patterns
    print("\n🎨 Different Tool Formatting Examples:")
    print("-" * 40)
    
    from prompts import format_tools_for_template
    
    patterns = ["tool_names", "tool_list", "tools", "tool_schemas"]
    
    for pattern in patterns:
        print(f"\n📌 Pattern: {pattern}")
        formatted = format_tools_for_template(tools, pattern)
        preview = formatted[:150] + "..." if len(formatted) > 150 else formatted
        print(preview)


if __name__ == "__main__":
    main()