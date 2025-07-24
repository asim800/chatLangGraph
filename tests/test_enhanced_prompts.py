#!/usr/bin/env python3
"""
Test script for enhanced tool argument functionality
"""

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from prompts import render_template_with_tools, format_tool_arguments

# Define the financial tools (same as run_finchat_with_tools.py)
@tool  
def calculate_risk(portfolio: str) -> float:
    """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
    if "crypto" in portfolio.lower() or "bitcoin" in portfolio.lower():
        return 0.8
    elif "bonds" in portfolio.lower() or "treasury" in portfolio.lower():
        return 0.2  
    elif "stocks" in portfolio.lower() or "equity" in portfolio.lower():
        return 0.6
    else:
        return 0.4

@tool
def get_stock_info(symbol: str) -> str:
    """Get basic stock information"""
    stock_data = {
        "AAPL": "Apple Inc. - Current: $150, +2.5% today, Strong Buy rating",
        "MSFT": "Microsoft Corp. - Current: $300, +1.2% today, Buy rating", 
        "TSLA": "Tesla Inc. - Current: $200, -3.1% today, Hold rating",
    }
    return stock_data.get(symbol.upper(), f"Stock data for {symbol} not available")

@tool
def portfolio_analyzer(holdings: str) -> str:
    """Analyze portfolio diversification and provide recommendations"""
    return f"""
Portfolio Analysis for: {holdings}
✅ Diversification: Good mix across sectors
📊 Risk Level: Moderate (0.45/1.0)
💰 Expected Return: 8-12% annually
🎯 Recommendation: Consider adding international exposure
"""

def main():
    tools = [calculate_risk, get_stock_info, portfolio_analyzer]
    
    print("🔧 Enhanced Tool Argument System Demo")
    print("=" * 50)
    
    # Test different formatting strategies
    strategies = ["simple", "detailed", "json", "extraction"]
    
    for strategy in strategies:
        print(f"\n🎯 {strategy.upper()} FORMATTER:")
        print("-" * 30)
        args_format = format_tool_arguments(tools, strategy)
        print(args_format)
    
    print("\n" + "=" * 50)
    print("📝 ENHANCED FINCHAT PROMPT PREVIEW:")
    print("=" * 50)
    
    # Show how the enhanced prompt looks
    rendered = render_template_with_tools("finchat_prompt", tools=tools, formatter_strategy="detailed")
    
    # Show just the argument extraction section
    if "ARGUMENT EXTRACTION GUIDE:" in rendered:
        start = rendered.find("ARGUMENT EXTRACTION GUIDE:")
        end = rendered.find("Use the following format:")
        guide_section = rendered[start:end].strip()
        print(guide_section)
    
    print("\n💡 To use different strategies:")
    print("  render_template_with_tools('finchat_prompt', tools=tools, formatter_strategy='simple')")
    print("  render_template_with_tools('finchat_prompt', tools=tools, formatter_strategy='json')")
    print("  render_template_with_tools('finchat_prompt', tools=tools, formatter_strategy='extraction')")

if __name__ == "__main__":
    main()