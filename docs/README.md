# LangGraph Chatbot Framework

A Python framework for building and evaluating LLM/AI agentic chatbots with high user engagement using LangGraph.

## Features

- 🤖 **LangGraph-based Agent**: Sophisticated conversation flow management
- 📊 **Interaction Storage**: File-based storage for conversation history and analysis  
- 🎯 **Engagement Scoring**: Multi-metric evaluation system for conversation quality
- 🧪 **A/B Testing**: Built-in experiment framework for prompt optimization
- ⚙️ **Configurable**: Flexible configuration system for different use cases
- 📈 **Analytics**: Detailed metrics and improvement suggestions
- 🎨 **Abstract Base Class**: Extensible architecture for custom chatbot implementations
- 📝 **Predefined Prompts**: Dictionary-based prompt management system
- 💬 **Chat History**: Retrieve conversation history with flexible commands
- 🔧 **Command-Line Interface**: Rich CLI for prompt management and interactions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Run Interactive Chat**
   ```bash
   # Basic chat
   python main.py chat
   
   # Chat with predefined prompt
   python main.py chat --prompt coding_mentor
   
   # Chat with custom prompt
   python main.py chat --prompt "You are a helpful assistant"
   
   # Chat with config file
   python main.py chat --config config/my_config.json
   ```

## Directory Structure

```
chatbot_framework/
├── agents/           # Core chatbot agent implementation
│   ├── base_chatbot_agent.py    # Abstract base class
│   └── chatbot_agent.py         # Default implementation
├── storage/          # Interaction storage and retrieval
├── evaluation/       # Scoring and evaluation metrics
├── config/          # Configuration management and A/B testing
├── tools/           # Additional tools and utilities
├── prompts/         # Prompt templates and variants
└── tests/           # Unit tests

examples/            # Usage examples and demos
config/             # Configuration files
prompts.py          # Predefined prompt dictionary
interactions/       # Stored conversation data (created at runtime)
├── conversations/   # Session-based conversation history
├── interactions/    # Individual interaction records
└── system_prompts/  # Stored system prompts by session
```

## Core Components

### BaseChatbotAgent (Abstract Base Class)
Abstract base class that defines the core chatbot interface:
- **Abstract Methods**: `_build_graph()` - must be implemented by subclasses
- **Common Methods**: `_process_input()`, `_generate_response()`, `_update_engagement()`, `_store_interaction()`, `chat()`
- **Extensible Design**: Create custom chatbot agents by inheriting from this class

### ChatbotAgent
Default implementation of the conversational agent built on LangGraph:
- Message processing and context management
- Response generation with LLM integration
- Session and conversation tracking
- Engagement scoring and optimization
- Inherits from `BaseChatbotAgent`

### InteractionStore
Enhanced file-based storage system that:
- Saves conversations for analysis
- Manages user sessions and history
- Stores system prompts by session
- Provides chat history retrieval
- Provides data export capabilities
- Tracks engagement metrics

### InteractionScorer
Evaluation framework that measures:
- **Conversation Length**: Number of message exchanges
- **Response Quality**: Relevance and helpfulness of responses
- **User Engagement**: Active user participation metrics
- **Conversation Flow**: Natural progression and timing
- **Stickiness**: User retention and session duration

### ConfigManager
Configuration and experiment management:
- A/B testing framework for prompt optimization
- Traffic splitting for experiments
- Dynamic prompt assignment per user
- Configuration validation and templates

### Prompt Management System
Dictionary-based prompt management with `prompts.py`:
- **Predefined Prompts**: 7 built-in specialist prompts (financial_advisor, coding_mentor, teacher, etc.)
- **Command-Line Integration**: Use prompt names or custom text via `--prompt` argument
- **Search & Discovery**: Find prompts by name or content keywords
- **Session Storage**: System prompts are stored per session in InteractionStore
- **Extensible**: Easy to add new prompts to the dictionary

## Usage Examples

### Basic Chat
```python
from chatbot_framework import ChatbotAgent, InteractionStore, ChatbotConfig

config = ChatbotConfig(
    model_name="gpt-3.5-turbo",
    system_prompt="You are a helpful assistant focused on engagement."
)

store = InteractionStore("./conversations")
agent = ChatbotAgent(config, store)

response = agent.chat("Hello!", user_id="user123")
print(response["response"])
```

### Using Predefined Prompts
```python
from prompts import get_prompt

# Get a predefined prompt
coding_prompt = get_prompt("coding_mentor")
config = ChatbotConfig(
    model_name="gpt-3.5-turbo",
    system_prompt=coding_prompt
)

agent = ChatbotAgent(config, store)
response = agent.chat("How do I learn Python?", user_id="user123")
```

### Creating Custom Chatbot Agents
```python
from chatbot_framework.agents import BaseChatbotAgent
from langgraph.graph import StateGraph, END

class CustomChatbotAgent(BaseChatbotAgent):
    def _build_graph(self) -> StateGraph:
        """Custom conversation flow"""
        graph = StateGraph(ConversationState)
        
        # Add your custom nodes
        graph.add_node("custom_process", self._custom_process)
        graph.add_node("generate_response", self._generate_response)
        graph.add_node("store_interaction", self._store_interaction)
        
        # Add custom edges
        graph.add_edge("custom_process", "generate_response")
        graph.add_edge("generate_response", "store_interaction")
        graph.add_edge("store_interaction", END)
        
        graph.set_entry_point("custom_process")
        return graph.compile()
    
    def _custom_process(self, state):
        # Your custom processing logic
        return state

# Use your custom agent
custom_agent = CustomChatbotAgent(config, store)
```

### Chat History Management
```python
# Get chat history
messages = agent.get_chat_history("user123", "session456", limit=10)

# Format for display
formatted_history = agent.format_chat_history(messages)
print(formatted_history)
```

### Running Evaluations
```python
from chatbot_framework import InteractionScorer

scorer = InteractionScorer()
interactions = store.get_interactions_for_evaluation()
results = scorer.evaluate_interactions(interactions)

print(f"Average engagement: {results['metric_statistics']['overall']['mean']}")
```

### A/B Testing Prompts
```python
from chatbot_framework.config import ConfigManager, ExperimentConfig

config_manager = ConfigManager()
experiment = ExperimentConfig(
    name="engagement_test",
    description="Testing different prompt styles",
    control_prompt="Standard helpful assistant prompt",
    test_prompts={
        "friendly": "Very friendly and enthusiastic prompt",
        "professional": "Professional and business-focused prompt"
    },
    traffic_split={"control": 0.33, "friendly": 0.33, "professional": 0.34}
)

config_manager.create_experiment(experiment)
```

## Command Line Interface

### Start Interactive Chat
```bash
# Basic chat
python main.py chat

# Chat with predefined prompt
python main.py chat --prompt financial_advisor
python main.py chat --prompt coding_mentor
python main.py chat --prompt teacher

# Chat with custom prompt text
python main.py chat --prompt "You are a helpful research assistant"

# Chat with config file
python main.py chat --config config/my_config.json

# Combined: config + predefined prompt
python main.py chat --prompt financial_advisor --config config/my_config.json
```

### Prompt Management
```bash
# List all available predefined prompts
python main.py prompts list

# Search for prompts by keyword
python main.py prompts search code
python main.py prompts search financial
python main.py prompts search teach
```

### Interactive Commands
During chat sessions, use these commands:
```bash
quit          # Exit the chat
new           # Start a new session
stats         # Show engagement statistics
history       # Show last 10 messages
history 5     # Show last 5 messages
history all   # Show all messages in session
```

### Evaluate Stored Interactions
```bash
python main.py evaluate --storage ./interactions
```

### Export Data for Analysis
```bash
python main.py export --storage ./interactions --output data.csv --format csv
```

### Create Configuration Template
```bash
python main.py config --output my_config.json
```

## Configuration

Create a configuration file or use environment variables:

```json
{
  "model_name": "gpt-3.5-turbo",
  "temperature": 0.7,
  "system_prompt": "Your engaging system prompt here",
  "context_window": 10,
  "storage_path": "interactions",
  "enable_evaluation": true
}
```

## Predefined Prompts

The framework includes 7 built-in specialist prompts in `prompts.py`:

| Prompt Name | Description | Use Case |
|-------------|-------------|----------|
| `default` | Basic helpful assistant | General purpose conversations |
| `financial_advisor` | Expert financial guidance with portfolio analysis | Investment advice, financial planning |
| `coding_mentor` | Programming and software engineering help | Code reviews, learning programming |
| `teacher` | Educational support across subjects | Learning, explanations, homework help |
| `creative_writer` | Creative writing and storytelling assistance | Writing projects, story development |
| `research_assistant` | Research and information gathering | Academic research, fact-checking |
| `prompt_optimizer` | Lyra - AI prompt optimization specialist | Improving and optimizing prompts |

### Adding Custom Prompts
```python
# Add to prompts.py SYSTEM_PROMPTS dictionary
SYSTEM_PROMPTS["my_custom_prompt"] = """
You are a specialized assistant for...
Your capabilities include...
"""
```

## Evaluation Metrics

The framework tracks multiple engagement metrics:

- **Conversation Length**: Measures sustained interaction
- **Response Quality**: Analyzes response depth and questions asked
- **User Engagement**: Tracks user message length and response patterns  
- **Conversation Flow**: Evaluates natural progression and timing
- **Stickiness**: Measures session duration and user retention

## Extending the Framework

### Custom Chatbot Agents
Create specialized chatbot agents by inheriting from `BaseChatbotAgent`:
```python
from chatbot_framework.agents import BaseChatbotAgent
from langgraph.graph import StateGraph, END

class SpecializedAgent(BaseChatbotAgent):
    def _build_graph(self) -> StateGraph:
        """Define your custom conversation flow"""
        graph = StateGraph(ConversationState)
        
        # Add custom processing nodes
        graph.add_node("specialized_process", self._specialized_process)
        graph.add_node("generate_response", self._generate_response)
        graph.add_node("custom_validation", self._custom_validation)
        graph.add_node("store_interaction", self._store_interaction)
        
        # Define custom flow
        graph.add_edge("specialized_process", "generate_response")
        graph.add_edge("generate_response", "custom_validation")
        graph.add_edge("custom_validation", "store_interaction")
        graph.add_edge("store_interaction", END)
        
        graph.set_entry_point("specialized_process")
        return graph.compile()
    
    def _specialized_process(self, state):
        # Your custom processing logic
        state["custom_data"] = "processed"
        return state
    
    def _custom_validation(self, state):
        # Custom validation logic
        return state
```

### Custom Metrics
```python
from chatbot_framework.evaluation import EvaluationMetric

def custom_scorer(interaction):
    # Your scoring logic here
    return score_0_to_1

custom_metric = EvaluationMetric(
    name="custom_metric",
    description="My custom scoring function",
    weight=0.2,
    score_function=custom_scorer
)

scorer.add_custom_metric(custom_metric)
```

### Custom Prompts
Add new prompts to the `prompts.py` dictionary:
```python
# In prompts.py
SYSTEM_PROMPTS["domain_expert"] = """
You are a domain-specific expert in...
Your expertise includes...
Always provide detailed, accurate information...
"""

# Use in code
from prompts import get_prompt
expert_prompt = get_prompt("domain_expert")
```

### Custom Tools
Add new tools to the `tools/` directory and register them in your configuration.

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.