from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from typing import List, Dict, Any, Callable
import inspect
import json

# Sample tools for demonstration
@tool
def calculate_tax(amount: float, state: str, filing_status: str = "single") -> str:
    """Calculate tax for given income amount and state."""
    return f"Tax calculated for ${amount} in {state}"

@tool  
def book_flight(departure_city: str, arrival_city: str, departure_date: str, 
                passengers: int = 1, class_type: str = "economy") -> str:
    """Book a flight between cities."""
    return f"Flight booked from {departure_city} to {arrival_city}"

@tool
def create_meeting(title: str, duration_minutes: int, attendees: List[str]) -> str:
    """Create a meeting with specified details."""
    return f"Meeting '{title}' created for {duration_minutes} minutes"

# Template library for experimentation
TEMPLATES = {
    "basic": """You have access to these tools: {tool_names}

Tool Details:
{tools}

Arguments to extract:
{tool_args}

User request: {input}

Call the appropriate tool with extracted arguments.""",

    "detailed": """You are an expert assistant that extracts arguments from user requests.

AVAILABLE TOOLS: {tool_names}
{tools}

ARGUMENT EXTRACTION GUIDE:
{tool_args}

INSTRUCTIONS:
1. Identify which tool the user needs
2. Extract the required arguments from their request
3. Use the argument guide above to understand what to look for
4. Call the tool with the extracted arguments

USER REQUEST: {input}""",

    "step_by_step": """Let's work through this step by step.

Available tools: {tool_names}
{tools}

Step 1: Analyze the user's request
Step 2: Identify which tool is needed
Step 3: Extract arguments using this guide:
{tool_args}
Step 4: Call the tool with extracted arguments

User request: {input}""",

    "json_focused": """Extract arguments and call tools using JSON format.

Tools: {tool_names}
{tools}

Expected argument structure:
{tool_args}

For the request: {input}

Extract arguments in JSON format and call the appropriate tool."""
}

# Argument formatting strategies
class ArgumentFormatters:
    @staticmethod
    def simple(tools: List) -> str:
        """Simple argument listing."""
        result = ""
        for tool in tools:
            result += f"\n{tool.name}:\n"
            sig = inspect.signature(tool.func)
            for param_name, param in sig.parameters.items():
                param_type = getattr(param.annotation, '__name__', 'any')
                required = param.default == inspect.Parameter.empty
                status = "required" if required else f"optional (default: {param.default})"
                result += f"  - {param_name} ({param_type}): {status}\n"
        return result

    @staticmethod
    def detailed_with_hints(tools: List) -> str:
        """Detailed formatting with extraction hints."""
        # This would use tool-specific argument specifications
        specs = {
            "calculate_tax": {
                "amount": {"type": "float", "required": True, "hints": ["dollar amounts", "$50k = 50000", "salary figures"]},
                "state": {"type": "str", "required": True, "hints": ["state names", "CA = California", "location mentions"]},
                "filing_status": {"type": "str", "required": False, "default": "single", "hints": ["married", "single", "head of household"]}
            },
            "book_flight": {
                "departure_city": {"type": "str", "required": True, "hints": ["from [city]", "departing from", "NYC, LAX codes"]},
                "arrival_city": {"type": "str", "required": True, "hints": ["to [city]", "going to", "destination"]},
                "departure_date": {"type": "str", "required": True, "hints": ["YYYY-MM-DD format", "tomorrow = next day", "March 15"]},
                "passengers": {"type": "int", "required": False, "default": 1, "hints": ["for 2 people", "family of 4"]},
                "class_type": {"type": "str", "required": False, "default": "economy", "hints": ["business class", "first class", "coach"]}
            },
            "create_meeting": {
                "title": {"type": "str", "required": True, "hints": ["meeting about", "subject", "topic"]},
                "duration_minutes": {"type": "int", "required": True, "hints": ["30 minutes", "1 hour = 60", "duration"]},
                "attendees": {"type": "List[str]", "required": True, "hints": ["with John and Mary", "team members", "email addresses"]}
            }
        }
        
        result = ""
        for tool in tools:
            if tool.name in specs:
                result += f"\n=== {tool.name.upper()} ARGUMENTS ===\n"
                for arg_name, spec in specs[tool.name].items():
                    status = "REQUIRED" if spec["required"] else f"OPTIONAL (default: {spec.get('default')})"
                    result += f"• {arg_name} ({spec['type']}) - {status}\n"
                    result += f"  Look for: {', '.join(spec['hints'])}\n\n"
        return result

    @staticmethod
    def json_schema(tools: List) -> str:
        """JSON schema format for arguments."""
        schemas = {}
        for tool in tools:
            sig = inspect.signature(tool.func)
            schema = {"type": "object", "properties": {}, "required": []}
            
            for param_name, param in sig.parameters.items():
                param_type = getattr(param.annotation, '__name__', 'string')
                type_mapping = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}
                json_type = type_mapping.get(param_type, "string")
                
                schema["properties"][param_name] = {"type": json_type}
                if param.default == inspect.Parameter.empty:
                    schema["required"].append(param_name)
                else:
                    schema["properties"][param_name]["default"] = param.default
                    
            schemas[tool.name] = schema
        
        return json.dumps(schemas, indent=2)

    @staticmethod
    def extraction_focused(tools: List) -> str:
        """Format focused on extraction patterns."""
        result = ""
        for tool in tools:
            result += f"\n🔍 {tool.name.upper()} - What to extract:\n"
            sig = inspect.signature(tool.func)
            
            for param_name, param in sig.parameters.items():
                required = param.default == inspect.Parameter.empty
                if required:
                    result += f"  ✅ MUST FIND: {param_name}\n"
                else:
                    result += f"  🔶 OPTIONAL: {param_name} (default: {param.default})\n"
        return result

FORMATTERS = {
    "simple": ArgumentFormatters.simple,
    "detailed": ArgumentFormatters.detailed_with_hints,
    "json": ArgumentFormatters.json_schema,
    "extraction": ArgumentFormatters.extraction_focused
}

class PromptExperiment:
    def __init__(self, template_id: str, tools: List, format_strategy: str, 
                 include_tool_args: bool = True):
        """
        Initialize a prompt experiment configuration.
        
        Args:
            template_id: Key for template in TEMPLATES dict
            tools: List of tools to include
            format_strategy: Key for formatter in FORMATTERS dict
            include_tool_args: Whether to include tool arguments in prompt
        """
        self.template_id = template_id
        self.template = TEMPLATES[template_id]
        self.tools = tools
        self.format_strategy = format_strategy
        self.formatter = FORMATTERS[format_strategy]
        self.include_tool_args = include_tool_args
    
    def generate_prompt(self, user_input: str) -> str:
        """Generate the complete prompt for given user input."""
        tool_args = self.formatter(self.tools) if self.include_tool_args else ""
        
        return PromptTemplate.from_template(self.template).format(
            tools=self._format_tools(),
            tool_names=', '.join([t.name for t in self.tools]),
            tool_args=tool_args,
            input=user_input
        )
    
    def _format_tools(self) -> str:
        """Format tool descriptions."""
        result = ""
        for tool in self.tools:
            result += f"{tool.name}: {tool.description}\n"
        return result
    
    def compare_with(self, other_experiment: 'PromptExperiment', user_input: str):
        """Compare this experiment with another."""
        print(f"=== EXPERIMENT 1: {self.template_id} + {self.format_strategy} ===")
        print(self.generate_prompt(user_input))
        print(f"\n=== EXPERIMENT 2: {other_experiment.template_id} + {other_experiment.format_strategy} ===")
        print(other_experiment.generate_prompt(user_input))
    
    def __repr__(self):
        return f"PromptExperiment(template='{self.template_id}', formatter='{self.format_strategy}', tools={len(self.tools)})"

# Example usage and experimentation
if __name__ == "__main__":
    # Define different experimental configurations
    experiments = [
        PromptExperiment("basic", [calculate_tax], "simple"),
        PromptExperiment("detailed", [calculate_tax, book_flight], "detailed"), 
        PromptExperiment("step_by_step", [book_flight], "extraction"),
        PromptExperiment("json_focused", [create_meeting], "json"),
    ]
    
    test_inputs = [
        "Calculate tax for $75000 income in California filing as married",
        "Book a business class flight from NYC to LA on March 25th for 2 people",
        "Schedule a 1 hour meeting with John and Sarah about quarterly review"
    ]
    
    print("PROMPT EXPERIMENT COMPARISON")
    print("=" * 50)
    
    # Test each experiment
    for i, experiment in enumerate(experiments):
        print(f"\n🧪 EXPERIMENT {i+1}: {experiment}")
        print("-" * 40)
        
        relevant_input = test_inputs[i % len(test_inputs)]
        prompt = experiment.generate_prompt(relevant_input)
        print(f"Input: {relevant_input}")
        print(f"Generated Prompt:\n{prompt}")
    
    # Compare two experiments side by side
    print(f"\n🔄 COMPARISON: Different formatting strategies")
    print("=" * 60)
    exp1 = PromptExperiment("detailed", [calculate_tax], "simple")
    exp2 = PromptExperiment("detailed", [calculate_tax], "detailed")
    exp1.compare_with(exp2, "Calculate tax for $50000 in Texas")