#!/usr/bin/env python3
"""
Demo script to show react_prompt with ArgumentFormatters working
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prompts import render_template_with_tools, format_tool_arguments
from tools.financial_tools import get_financial_tools

def main():
    print("🔬 React Prompt + ArgumentFormatters Demo")
    print("=" * 45)
    
    tools = get_financial_tools()[:2]  # Use first 2 tools for demo
    
    # Test all ArgumentFormatter strategies
    strategies = ["simple", "detailed", "json", "extraction"]
    
    for strategy in strategies:
        print(f"\n--- {strategy.upper()} ArgumentFormatter ---")
        tool_args = format_tool_arguments(tools, strategy)
        print(tool_args)
        print("-" * 40)
    
    # Show the complete rendered react_prompt
    print("\n--- COMPLETE REACT PROMPT (detailed strategy) ---")
    rendered = render_template_with_tools(
        "react_prompt", 
        tools=tools, 
        formatter_strategy="detailed",
        input="What's the risk of my crypto portfolio?"
    )
    print(rendered)
    
    print("\n✅ All formatters working correctly!")
    print("💡 The script can now be used with a real chatbot agent")

if __name__ == "__main__":
    main()