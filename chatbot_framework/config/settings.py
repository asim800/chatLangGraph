"""
Configuration management for the chatbot framework
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
import os
import json
from pathlib import Path


@dataclass
class ChatbotConfig:
    # LLM Configuration
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    openai_api_key: Optional[str] = None
    
    # Conversation Settings
    context_window: int = 10
    max_conversation_length: int = 50
    session_timeout_minutes: int = 30
    
    # System Prompts
    system_prompt: str = "You are a helpful, engaging AI assistant focused on creating meaningful conversations with users."
    
    # Storage Settings
    storage_path: str = "interactions"
    auto_backup: bool = True
    backup_interval_hours: int = 24
    
    # Evaluation Settings
    enable_evaluation: bool = True
    evaluation_interval: int = 100  # Evaluate every N interactions
    
    # Engagement Settings
    engagement_tracking: bool = True
    min_engagement_score: float = 0.3
    
    # Custom prompt variations for A/B testing
    prompt_variants: Dict[str, str] = field(default_factory=dict)
    
    # Tool configurations
    available_tools: List[str] = field(default_factory=list)
    tools: Optional[List[Any]] = field(default_factory=list)  # Actual tool objects
    tool_mode: str = "function"  # "text" for ReAct pattern, "function" for structured function calling
    
    def __post_init__(self):
        # Set OpenAI API key from environment if not provided
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key must be provided via config or OPENAI_API_KEY environment variable")
    
    @classmethod
    def from_file(cls, config_path: str) -> 'ChatbotConfig':
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def to_file(self, config_path: str):
        """Save configuration to JSON file"""
        # Convert to dict, excluding None values
        config_dict = {}
        for key, value in self.__dict__.items():
            if value is not None:
                config_dict[key] = value
        
        # Don't save the API key to file for security
        if 'openai_api_key' in config_dict:
            del config_dict['openai_api_key']
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def get_prompt_variant(self, variant_name: str) -> str:
        """Get a specific prompt variant or default system prompt"""
        return self.prompt_variants.get(variant_name, self.system_prompt)
    
    def add_prompt_variant(self, name: str, prompt: str):
        """Add a new prompt variant for testing"""
        self.prompt_variants[name] = prompt
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        if not self.openai_api_key:
            issues.append("OpenAI API key is required")
        
        if self.temperature < 0 or self.temperature > 2:
            issues.append("Temperature must be between 0 and 2")
        
        if self.context_window < 1:
            issues.append("Context window must be at least 1")
        
        if self.max_conversation_length < 2:
            issues.append("Max conversation length must be at least 2")
        
        if self.min_engagement_score < 0 or self.min_engagement_score > 1:
            issues.append("Min engagement score must be between 0 and 1")
        
        return issues


@dataclass
class ExperimentConfig:
    """Configuration for A/B testing and experiments"""
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    active: bool = True
    
    # Experiment parameters
    control_prompt: str = ""
    test_prompts: Dict[str, str] = field(default_factory=dict)
    traffic_split: Dict[str, float] = field(default_factory=dict)  # variant_name -> percentage
    
    # Success metrics
    target_metrics: List[str] = field(default_factory=list)
    success_threshold: float = 0.05  # Minimum improvement to consider success
    
    def validate_traffic_split(self) -> bool:
        """Ensure traffic split adds up to 100%"""
        total = sum(self.traffic_split.values())
        return abs(total - 1.0) < 0.01  # Allow for small floating point errors


class ConfigManager:
    """Manages configuration loading, saving, and experiments"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.main_config_path = self.config_dir / "chatbot_config.json"
        self.experiments_dir = self.config_dir / "experiments"
        self.experiments_dir.mkdir(exist_ok=True)
    
    def load_main_config(self) -> ChatbotConfig:
        """Load the main chatbot configuration"""
        if self.main_config_path.exists():
            return ChatbotConfig.from_file(str(self.main_config_path))
        else:
            # Create default config
            config = ChatbotConfig()
            self.save_main_config(config)
            return config
    
    def save_main_config(self, config: ChatbotConfig):
        """Save the main chatbot configuration"""
        config.to_file(str(self.main_config_path))
    
    def create_experiment(self, experiment: ExperimentConfig) -> str:
        """Create and save a new experiment configuration"""
        if not experiment.validate_traffic_split():
            raise ValueError("Traffic split must add up to 100%")
        
        experiment_file = self.experiments_dir / f"{experiment.name}.json"
        
        experiment_dict = {
            "name": experiment.name,
            "description": experiment.description,
            "start_date": experiment.start_date.isoformat(),
            "end_date": experiment.end_date.isoformat() if experiment.end_date else None,
            "active": experiment.active,
            "control_prompt": experiment.control_prompt,
            "test_prompts": experiment.test_prompts,
            "traffic_split": experiment.traffic_split,
            "target_metrics": experiment.target_metrics,
            "success_threshold": experiment.success_threshold
        }
        
        with open(experiment_file, 'w') as f:
            json.dump(experiment_dict, f, indent=2)
        
        return str(experiment_file)
    
    def load_experiment(self, experiment_name: str) -> Optional[ExperimentConfig]:
        """Load an experiment configuration"""
        experiment_file = self.experiments_dir / f"{experiment_name}.json"
        
        if not experiment_file.exists():
            return None
        
        with open(experiment_file, 'r') as f:
            data = json.load(f)
        
        # Convert date strings back to datetime objects
        data["start_date"] = datetime.fromisoformat(data["start_date"])
        if data["end_date"]:
            data["end_date"] = datetime.fromisoformat(data["end_date"])
        
        return ExperimentConfig(**data)
    
    def get_active_experiments(self) -> List[ExperimentConfig]:
        """Get all currently active experiments"""
        active_experiments = []
        
        for experiment_file in self.experiments_dir.glob("*.json"):
            experiment = self.load_experiment(experiment_file.stem)
            if experiment and experiment.active:
                # Check if experiment is still within date range
                now = datetime.now()
                if experiment.start_date <= now:
                    if experiment.end_date is None or now <= experiment.end_date:
                        active_experiments.append(experiment)
        
        return active_experiments
    
    def get_prompt_for_user(self, user_id: str, base_config: ChatbotConfig) -> str:
        """Get the appropriate prompt for a user based on active experiments"""
        active_experiments = self.get_active_experiments()
        
        if not active_experiments:
            return base_config.system_prompt
        
        # Simple hash-based assignment for consistent user experience
        import hashlib
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        
        for experiment in active_experiments:
            # Determine which variant this user should see
            cumulative_prob = 0.0
            normalized_hash = (user_hash % 1000) / 1000.0  # Normalize to [0, 1)
            
            for variant_name, probability in experiment.traffic_split.items():
                cumulative_prob += probability
                if normalized_hash < cumulative_prob:
                    if variant_name == "control":
                        return experiment.control_prompt or base_config.system_prompt
                    elif variant_name in experiment.test_prompts:
                        return experiment.test_prompts[variant_name]
                    break
        
        return base_config.system_prompt