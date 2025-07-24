#!/usr/bin/env python3
"""
Test React pattern with web chat
"""

import os
from dotenv import load_dotenv
load_dotenv()

from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig
from tools.financial_tools import get_financial_tools
from prompts import render_template_with_tools

def test_react_pattern():
    """Test React pattern response parsing"""
    
    # Create config with react_prompt using the web chat approach
    from web_chat import get_or_create_chatbot
    
    # This will use the special react_prompt handling from web_chat
    chatbot = get_or_create_chatbot('react_prompt')
    
    print('🧪 Testing React Pattern...')
    print('=' * 50)
    
    # Test with a complex financial question that should trigger multiple tools
    result = chatbot.invoke({
        'message': 'What is the risk assessment for a portfolio containing SPY, AAPL, and MSFT? I need to understand each stock first.',
        'user_id': 'test_user',
        'session_id': None
    })
    
    print('✅ React Pattern Test Result:')
    print('=' * 50)
    print(result['response'])
    print('=' * 50)
    print(f'Engagement Score: {result["engagement_score"]}')
    
    # Check if it contains React pattern keywords
    response = result['response']
    react_keywords = ['Question:', 'Thought:', 'Action:', 'Action Input:', 'Observation:', 'Final Answer:']
    found_keywords = [kw for kw in react_keywords if kw in response]
    
    print(f'\n🔍 React Pattern Keywords Found: {found_keywords}')
    
    if len(found_keywords) >= 4:
        print('✅ React pattern is working correctly!')
    else:
        print('❌ React pattern may not be working as expected.')
        print('Expected keywords: Question, Thought, Action, Action Input, Observation, Final Answer')

if __name__ == "__main__":
    test_react_pattern()