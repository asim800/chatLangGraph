#!/usr/bin/env python3
"""
Ready-to-run example: React Chat with Tools and ArgumentFormatters
Run this script to test the react_prompt with enhanced argument formatting
"""

import sys
import os
import readline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from langchain_core.tools import tool
from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from prompts import render_template_with_tools

# Define financial tools (same as original)
@tool  
def calculate_risk(portfolio: str) -> float:
    """Calculate portfolio risk score (0-1, where 1 is highest risk)"""
    # Simple risk calculation
    if "crypto" in portfolio.lower() or "bitcoin" in portfolio.lower():
        return 0.8
    elif "bonds" in portfolio.lower() or "treasury" in portfolio.lower():
        return 0.2  
    elif "stocks" in portfolio.lower() or "equity" in portfolio.lower():
        return 0.6
    else:
        return 0.4  # Default moderate risk


@tool
def get_stock_info(symbol: str) -> str:
    """Get basic stock information"""
    stock_data = {
        "AAPL": "Apple Inc. - Current: $150, +2.5% today, Strong Buy rating",
        "MSFT": "Microsoft Corp. - Current: $300, +1.2% today, Buy rating", 
        "TSLA": "Tesla Inc. - Current: $200, -3.1% today, Hold rating",
        "SPY": "S&P 500 ETF - Current: $400, +0.8% today, Diversified index fund"
    }
    return stock_data.get(symbol.upper(), f"Stock data for {symbol} not available")


@tool
def portfolio_analyzer(holdings: str) -> str:
    """Analyze portfolio diversification and provide recommendations"""
    analysis = f"""
Portfolio Analysis for: {holdings}

✅ Diversification: Good mix across sectors
📊 Risk Level: Moderate (0.45/1.0)
💰 Expected Return: 8-12% annually
🎯 Recommendation: Consider adding international exposure

Key Insights:
- Well balanced between growth and value
- Good sector diversification
- Consider adding 10-15% international stocks
- Emergency fund should be 6 months expenses
"""
    return analysis.strip()


def main():
    print("🔬 React Agent with Enhanced Tools")
    print("=" * 40)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("💡 Create a .env file with: OPENAI_API_KEY=your-key-here")
        return
    
    # Our financial tools
    tools = [calculate_risk, get_stock_info, portfolio_analyzer]
    
    try:
        # Test different ArgumentFormatter strategies
        formatter_strategies = ["simple", "detailed", "json", "extraction"]
        
        print("🧪 Testing ArgumentFormatter strategies:")
        for strategy in formatter_strategies:
            print(f"\n--- {strategy.upper()} Strategy ---")
            try:
                rendered_prompt = render_template_with_tools("react_prompt", tools=tools, formatter_strategy=strategy, input="{input}")
                print(f"✅ {strategy} strategy rendered successfully!")
                if strategy == "detailed":  # Show one example
                    print("📝 Sample output (first 300 chars):")
                    print(rendered_prompt[:300] + "..." if len(rendered_prompt) > 300 else rendered_prompt)
            except Exception as e:
                print(f"❌ {strategy} strategy failed: {e}")
        
        # Use detailed strategy for the actual chatbot
        print(f"\n📝 Rendering react_prompt with detailed ArgumentFormatter...")
        rendered_prompt = render_template_with_tools("react_prompt", tools=tools, formatter_strategy="detailed", input="{input}")
        print("✅ Template rendered successfully!")
        
        # Create configuration with tools
        config = ChatbotConfig(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            system_prompt=rendered_prompt,
            tools=tools,
            storage_path="./demo_interactions"
        )
        
        # Create chatbot
        interaction_store = InteractionStore(config.storage_path)
        chatbot = ChatbotAgent(config, interaction_store)
        
        print("\n🤖 React Agent Ready!")
        print(f"🔧 Available tools: {[tool.name for tool in tools]}")
        print("\n💡 Try asking:")
        print("  • What's the risk of my crypto portfolio?")
        print("  • Get info on AAPL stock")
        print("  • Analyze my portfolio with AAPL, MSFT, and bonds")
        print("  • Compare risk between crypto and bonds")
        print("\n💬 Type 'quit' to exit")
        print("🔄 Use ↑/↓ arrow keys to navigate chat history")
        print()
        
        # Enable readline history
        readline.set_history_length(1000)
        
        user_id = "react_user"
        session_id = None
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
            
            # Add to readline history for arrow key navigation
            readline.add_history(user_input)
            
            try:
                # Format the input for the react template
                formatted_prompt = rendered_prompt.format(input=user_input)
                
                # Create a temporary config with the formatted prompt
                temp_config = ChatbotConfig(
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                    system_prompt="",  # We'll pass the full prompt as user message
                    tools=tools,
                    storage_path="./demo_interactions"
                )
                
                temp_chatbot = ChatbotAgent(temp_config, interaction_store)
                # Use invoke() method following LangGraph conventions
                response = temp_chatbot.invoke({
                    "message": formatted_prompt,
                    "user_id": user_id,
                    "session_id": session_id
                })
                
                if not session_id:
                    session_id = response["session_id"]
                
                print(f"\n🤖 React Agent: {response['response']}")
                print(f"📊 Engagement: {response['engagement_score']:.2f}")
                print()
                
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Make sure your OpenAI API key is valid")
                print("🔍 Debug info: Check if the react template formatting is correct")
                break
                
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("💡 Check your configuration and API key")


if __name__ == "__main__":
    main()