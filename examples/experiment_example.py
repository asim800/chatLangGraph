"""
Example of running A/B test experiments with different prompts
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_framework import ChatbotAgent, InteractionStore, InteractionScorer, ChatbotConfig
from chatbot_framework.config.settings import ConfigManager, ExperimentConfig


def setup_experiment():
    """Set up an A/B test experiment with different prompts"""
    
    # Create config manager
    config_manager = ConfigManager("./experiment_config")
    
    # Load or create main config
    config = config_manager.load_main_config()
    
    # Create an experiment
    experiment = ExperimentConfig(
        name="engagement_prompts_v1",
        description="Testing different system prompts for user engagement",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        control_prompt="You are a helpful AI assistant.",
        test_prompts={
            "friendly": """You are a friendly and enthusiastic AI assistant! 
            I love chatting with people and learning about their interests. 
            What would you like to talk about today?""",
            
            "professional": """You are a professional AI assistant focused on providing 
            precise, valuable information and insights. I aim to be helpful while 
            maintaining a respectful, business-appropriate tone.""",
            
            "curious": """You are a curious AI assistant who loves asking questions! 
            I'm genuinely interested in learning about you and helping you explore 
            ideas together. Let's dive deep into whatever interests you!"""
        },
        traffic_split={
            "control": 0.25,
            "friendly": 0.25, 
            "professional": 0.25,
            "curious": 0.25
        },
        target_metrics=["user_engagement", "conversation_length", "stickiness"],
        success_threshold=0.05
    )
    
    # Save experiment
    config_manager.create_experiment(experiment)
    print(f"✅ Created experiment: {experiment.name}")
    
    return config_manager, config


def run_experiment_simulation():
    """Simulate multiple users interacting with different prompt variants"""
    
    config_manager, base_config = setup_experiment()
    
    # Create storage and scorer
    interaction_store = InteractionStore("./experiment_interactions")
    scorer = InteractionScorer()
    
    # Simulate different users
    test_users = [
        ("user_001", ["Hello!", "That's interesting, tell me more", "Thanks!"]),
        ("user_002", ["Hi there", "What can you help me with?", "That's helpful", "Goodbye"]),
        ("user_003", ["Hey", "I'm looking for advice", "Can you elaborate?", "Perfect, thanks!"]),
        ("user_004", ["Hello", "I have a question", "That makes sense"]),
    ]
    
    print("\n🧪 Running Experiment Simulation...")
    print("=" * 40)
    
    for user_id, messages in test_users:
        print(f"\nUser: {user_id}")
        
        # Get prompt variant for this user
        prompt = config_manager.get_prompt_for_user(user_id, base_config)
        
        # Create config with the assigned prompt
        user_config = ChatbotConfig(
            model_name=base_config.model_name,
            temperature=base_config.temperature,
            system_prompt=prompt,
            storage_path=base_config.storage_path
        )
        
        # Create chatbot for this user
        chatbot = ChatbotAgent(user_config, interaction_store)
        
        session_id = None
        for message in messages:
            try:
                response = chatbot.chat(message, user_id, session_id)
                if not session_id:
                    session_id = response["session_id"]
                
                print(f"  User: {message}")
                print(f"  Bot: {response['response'][:100]}...")
                print(f"  Engagement: {response['engagement_score']:.2f}")
            
            except Exception as e:
                print(f"  Error: {e}")
                break
    
    return interaction_store, scorer


def analyze_experiment_results(interaction_store: InteractionStore, scorer: InteractionScorer):
    """Analyze results of the experiment"""
    
    print("\n📊 Experiment Results Analysis")
    print("=" * 35)
    
    # Get all interactions
    interactions = interaction_store.get_interactions_for_evaluation()
    
    if not interactions:
        print("No interactions found.")
        return
    
    # Group interactions by user to determine their prompt variant
    config_manager = ConfigManager("./experiment_config")
    base_config = config_manager.load_main_config()
    
    variant_interactions = {
        "control": [],
        "friendly": [],
        "professional": [], 
        "curious": []
    }
    
    for interaction in interactions:
        user_id = interaction["user_id"]
        user_prompt = config_manager.get_prompt_for_user(user_id, base_config)
        
        # Determine variant based on prompt content
        if "helpful AI assistant" in user_prompt and len(user_prompt) < 50:
            variant = "control"
        elif "friendly and enthusiastic" in user_prompt:
            variant = "friendly"
        elif "professional AI assistant" in user_prompt:
            variant = "professional"
        elif "curious AI assistant" in user_prompt:
            variant = "curious"
        else:
            variant = "unknown"
        
        if variant in variant_interactions:
            variant_interactions[variant].append(interaction)
    
    # Analyze each variant
    print("\nResults by Variant:")
    
    for variant_name, variant_interactions_list in variant_interactions.items():
        if not variant_interactions_list:
            continue
            
        print(f"\n{variant_name.upper()} ({len(variant_interactions_list)} interactions):")
        
        results = scorer.evaluate_interactions(variant_interactions_list)
        
        if "metric_statistics" in results:
            for metric, stats in results["metric_statistics"].items():
                print(f"  {metric}: {stats['mean']:.3f}")
    
    # Overall experiment metrics
    print(f"\n📈 Overall Metrics:")
    engagement_metrics = interaction_store.get_engagement_metrics()
    for key, value in engagement_metrics.items():
        print(f"  {key}: {value}")


def main():
    print("🧪 LangGraph Chatbot Framework - A/B Testing Example")
    print("=" * 55)
    
    # Run experiment simulation
    interaction_store, scorer = run_experiment_simulation()
    
    # Analyze results
    analyze_experiment_results(interaction_store, scorer)
    
    print("\n✅ Experiment completed! Check ./experiment_interactions for stored data.")


if __name__ == "__main__":
    main()