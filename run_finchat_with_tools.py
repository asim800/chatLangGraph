#!/usr/bin/env python3
"""
Ready-to-run example: Financial Chat with Tools
Run this script to test the complete tool-enabled chatbot system
"""

import sys
import os
import readline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from prompts import render_template_with_tools
from tools.financial_tools import get_financial_tools


def main():
    print("🏦 Financial Portfolio Chatbot with Tools")
    print("=" * 45)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("💡 Create a .env file with: OPENAI_API_KEY=your-key-here")
        return
    
    # Our financial tools from centralized module
    tools = get_financial_tools()
    
    try:
        # Render the prompt with tools
        print("📝 Rendering finchat_prompt with tools...")
        rendered_prompt = render_template_with_tools("finchat_prompt", tools=tools)
        print('*'*80)
        print(rendered_prompt)
        print('*'*80)
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
        
        print("\n🤖 Financial Assitant Ready!")
        print(f"🔧 Available tools: {[tool.name for tool in tools]}")
        print("\n💡 Try asking:")
        print("  • What's the risk of a crypto portfolio?")
        print("  • Get info on AAPL stock")
        print("  • Analyze my portfolio: AAPL, MSFT, bonds")
        print("  • General financial advice")
        print("\n💬 Type 'quit' to exit")
        print("🔄 Use ↑/↓ arrow keys to navigate chat history")
        print()
        
        # Enable readline history
        readline.set_history_length(1000)
        
        user_id = "demo_user"
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
                # Use invoke() method following LangGraph conventions
                response = chatbot.invoke({
                    "message": user_input,
                    "user_id": user_id,
                    "session_id": session_id
                })
                
                if not session_id:
                    session_id = response["session_id"]
                
                print(f"\n🤖 Financial Advisor: {response['response']}")
                print(f"📊 Engagement: {response['engagement_score']:.2f}")
                print()
                
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Make sure your OpenAI API key is valid")
                break
                
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("💡 Check your configuration and API key")


if __name__ == "__main__":
    main()