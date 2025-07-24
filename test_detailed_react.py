#!/usr/bin/env python3
"""
Test detailed React pattern with multiple sequential tool calls
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_detailed_react():
    """Test detailed React pattern"""
    
    from web_chat import get_or_create_chatbot
    
    # This will use the enhanced react_prompt handling
    chatbot = get_or_create_chatbot('react_prompt')
    
    print('🧪 Testing Detailed React Pattern...')
    print('=' * 60)
    
    # Test with a question that should require multiple sequential tool calls
    result = chatbot.invoke({
        'message': 'I want to analyze the risk of a portfolio with SPY, AAPL, and MSFT. Please get information about each stock first, then calculate the overall portfolio risk.',
        'user_id': 'test_user',
        'session_id': None
    })
    
    print('✅ Detailed React Pattern Result:')
    print('=' * 60)
    print(result['response'])
    print('=' * 60)
    print(f'Engagement Score: {result["engagement_score"]}')
    
    # Check for expected detailed pattern
    response = result['response']
    
    # Count occurrences of each step type
    thought_count = response.count('Thought:')
    action_count = response.count('Action:')
    observation_count = response.count('Observation:')
    
    print(f'\n📊 Pattern Analysis:')
    print(f'  - Thought sections: {thought_count}')
    print(f'  - Action sections: {action_count}')
    print(f'  - Observation sections: {observation_count}')
    
    if thought_count >= 3 and action_count >= 2 and observation_count >= 2:
        print('✅ Detailed multi-step React pattern detected!')
    else:
        print('⚠️  Pattern may need more detail - try asking for more complex analysis')

if __name__ == "__main__":
    test_detailed_react()