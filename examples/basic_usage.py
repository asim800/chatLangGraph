"""
Basic usage example for the LangGraph chatbot framework
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import our framework
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_framework import ChatbotAgent, InteractionStore, InteractionScorer, ChatbotConfig


def main():
    # Initialize configuration
    config = ChatbotConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        system_prompt="""You are a friendly and engaging AI assistant. Your goal is to create 
        sticky conversations that keep users coming back. Ask thoughtful follow-up questions, 
        show genuine interest, and provide valuable insights. Be conversational and slightly playful.""",
        storage_path="./example_interactions"
    )
    
    # Initialize components
    interaction_store = InteractionStore(config.storage_path)
    chatbot = ChatbotAgent(config, interaction_store)
    scorer = InteractionScorer()
    
    print("🤖 LangGraph Chatbot Framework - Basic Example")
    print("=" * 50)
    print("Type 'quit' to exit, 'evaluate' to see scores")
    print()
    
    user_id = "demo_user"
    session_id = None
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'evaluate':
            evaluate_interactions(interaction_store, scorer)
            continue
        
        if not user_input:
            continue
        
        try:
            # Get chatbot response
            response = chatbot.chat(user_input, user_id, session_id)
            
            # Update session ID for continuation
            if not session_id:
                session_id = response["session_id"]
            
            print(f"Bot: {response['response']}")
            print(f"Engagement Score: {response['engagement_score']:.2f}")
            print()
            
        except Exception as e:
            print(f"Error: {e}")


def evaluate_interactions(interaction_store: InteractionStore, scorer: InteractionScorer):
    """Evaluate stored interactions and display results"""
    print("\n📊 Evaluating Interactions...")
    print("=" * 30)
    
    # Get all interactions
    interactions = interaction_store.get_interactions_for_evaluation()
    
    if not interactions:
        print("No interactions found to evaluate.")
        return
    
    # Evaluate interactions
    results = scorer.evaluate_interactions(interactions)
    
    # Display summary statistics
    print(f"Total Interactions: {results['total_interactions']}")
    print("\nMetric Statistics:")
    
    for metric_name, stats in results["metric_statistics"].items():
        print(f"  {metric_name.title().replace('_', ' ')}:")
        print(f"    Mean: {stats['mean']:.3f}")
        print(f"    Range: {stats['min']:.3f} - {stats['max']:.3f}")
    
    # Get improvement suggestions
    suggestions = scorer.get_improvement_suggestions(results)
    if suggestions:
        print("\n💡 Improvement Suggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
    
    # Display engagement metrics
    engagement_metrics = interaction_store.get_engagement_metrics()
    print(f"\n📈 Engagement Metrics:")
    print(f"  Unique Users: {engagement_metrics['unique_users']}")
    print(f"  Unique Sessions: {engagement_metrics['unique_sessions']}")
    print(f"  Avg Messages/Session: {engagement_metrics['avg_messages_per_session']:.1f}")
    print(f"  Avg Engagement Score: {engagement_metrics['avg_engagement_score']:.3f}")
    print()


if __name__ == "__main__":
    main()