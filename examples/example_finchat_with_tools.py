#!/usr/bin/env python3
"""
Example: Financial Chat with Tools
Demonstrates how to use the enhanced prompt template system with actual financial tools
"""

import sys
import os
from typing import List, Dict
import random

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from prompts import render_template_with_tools


# Define financial analysis tools
@tool
def calculate_portfolio_risk(portfolio_data: str) -> float:
    """
    Calculate portfolio risk metrics including volatility and VaR
    
    Args:
        portfolio_data: JSON string containing portfolio holdings and weights
    
    Returns:
        Risk score between 0 (low risk) and 1 (high risk)
    """
    # Simulate risk calculation
    import json
    try:
        portfolio = json.loads(portfolio_data)
        # Simple risk calculation based on number of holdings and diversification
        num_holdings = len(portfolio.get('holdings', []))
        risk_score = max(0.1, min(0.9, 1.0 / max(1, num_holdings) + random.uniform(0.1, 0.3)))
        return round(risk_score, 3)
    except:
        return 0.5  # Default moderate risk


@tool
def get_sharpe_ratio(returns_data: str) -> float:
    """
    Calculate Sharpe ratio for risk-adjusted returns
    
    Args:
        returns_data: JSON string with historical returns data
    
    Returns:
        Sharpe ratio (higher is better, >1.0 is good)
    """
    # Simulate Sharpe ratio calculation
    import json
    try:
        data = json.loads(returns_data)
        returns = data.get('returns', [0.08])  # Default 8% return
        avg_return = sum(returns) / len(returns) if returns else 0.08
        risk_free_rate = 0.02  # 2% risk-free rate
        volatility = 0.15 + random.uniform(-0.05, 0.05)  # Simulate volatility
        sharpe = (avg_return - risk_free_rate) / volatility
        return round(sharpe, 3)
    except:
        return 1.2  # Default good Sharpe ratio


@tool
def fetch_market_data(symbol: str) -> Dict:
    """
    Fetch current market data for a given symbol
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary with current price, change, and volume data
    """
    # Simulate market data
    base_prices = {
        'AAPL': 150.0,
        'MSFT': 300.0,
        'GOOGL': 2500.0,
        'TSLA': 200.0,
        'SPY': 400.0
    }
    
    base_price = base_prices.get(symbol.upper(), 100.0)
    change_pct = random.uniform(-5.0, 5.0)
    current_price = base_price * (1 + change_pct / 100)
    
    return {
        'symbol': symbol.upper(),
        'current_price': round(current_price, 2),
        'change_percent': round(change_pct, 2),
        'volume': random.randint(1000000, 10000000),
        'last_updated': '2024-07-22T10:30:00Z'
    }


def demo_tool_enabled_finchat():
    """Demonstrate financial chat with tools"""
    
    print("🏦 Financial Chat with Tools Demo")
    print("=" * 40)
    
    # Define our financial tools
    financial_tools = [
        calculate_portfolio_risk,
        get_sharpe_ratio,
        fetch_market_data
    ]
    
    # Show the rendered prompt with tools
    print("\n📝 Rendering finchat_prompt with tools...")
    rendered_prompt = render_template_with_tools(
        "finchat_prompt", 
        tools=financial_tools
    )
    
    print("✅ Template rendered successfully!")
    print(f"📏 Prompt length: {len(rendered_prompt)} characters")
    print("\n📋 Prompt preview:")
    print("=" * 50)
    print(rendered_prompt[:300] + "..." if len(rendered_prompt) > 300 else rendered_prompt)
    print("=" * 50)
    
    # Create tool-enabled configuration
    config = ChatbotConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        system_prompt=rendered_prompt,  # Use the rendered prompt
        tools=financial_tools,  # Add the actual tool objects
        storage_path="./finchat_interactions"
    )
    
    print(f"\n🔧 Tools configured: {[tool.name for tool in financial_tools]}")
    
    # Create components
    interaction_store = InteractionStore(config.storage_path)
    chatbot = ChatbotAgent(config, interaction_store)
    
    print("\n🤖 Financial Advisor Chatbot Ready!")
    print("💡 Try asking about:")
    print("  - Portfolio risk analysis")
    print("  - Sharpe ratio calculations") 
    print("  - Market data for stocks")
    print("  - Investment advice")
    print("\n💬 Commands: 'quit' to exit, 'new' for new session")
    print()
    
    user_id = "demo_user"
    session_id = None
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'new':
            session_id = None
            print("🆕 Started new session")
            continue
        
        if not user_input:
            continue
        
        try:
            # Get chatbot response (tools will be called automatically if needed)
            response = chatbot.chat(user_input, user_id, session_id)
            
            if not session_id:
                session_id = response["session_id"]
            
            print(f"\n🤖 Financial Advisor: {response['response']}")
            print(f"💯 Engagement Score: {response['engagement_score']:.2f}")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print()


def demo_different_tool_patterns():
    """Show different tool injection patterns"""
    
    print("\n🔧 Tool Injection Patterns Demo")
    print("=" * 40)
    
    tools = [calculate_portfolio_risk, get_sharpe_ratio, fetch_market_data]
    
    # Test different patterns by creating custom templates
    test_templates = {
        "tool_names_template": "You have access to: {tool_names}",
        "tool_list_template": "Available tools:\n{tool_list}",
        "tools_template": "Your tools:\n{tools}",
        "tool_schemas_template": "Tool schemas:\n{tool_schemas}"
    }
    
    for template_name, template_content in test_templates.items():
        print(f"\n📝 {template_name}:")
        print("-" * 30)
        
        # Temporarily add template to prompts
        from prompts import SYSTEM_PROMPTS
        SYSTEM_PROMPTS[template_name] = template_content
        
        try:
            rendered = render_template_with_tools(template_name, tools=tools)
            print(rendered[:200] + "..." if len(rendered) > 200 else rendered)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Clean up
            if template_name in SYSTEM_PROMPTS:
                del SYSTEM_PROMPTS[template_name]


if __name__ == "__main__":
    print("🎯 Financial Chat Tools Integration Example")
    print("=" * 50)
    
    try:
        demo_different_tool_patterns()
        print("\n" + "=" * 50)
        demo_tool_enabled_finchat()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\n💡 Make sure you have:")
        print("  - OpenAI API key in .env file")
        print("  - All required dependencies installed")