# Enhanced Tool Argument Support - Usage Guide

## Overview
The enhanced system provides better tool argument extraction for LLMs by including detailed argument guides in prompts.

## Quick Start

### 1. Run Enhanced Financial Chatbot
```bash
python run_finchat_with_tools.py
```
The existing script now automatically uses enhanced prompts with detailed argument extraction guides.

### 2. Test Different Formatting Strategies
```python
from prompts import render_template_with_tools, format_tool_arguments

# Your tools
tools = [calculate_risk, get_stock_info, portfolio_analyzer]

# Different formatting strategies
simple_prompt = render_template_with_tools("finchat_prompt", tools=tools, formatter_strategy="simple")
detailed_prompt = render_template_with_tools("finchat_prompt", tools=tools, formatter_strategy="detailed")  # Default
json_prompt = render_template_with_tools("finchat_prompt", tools=tools, formatter_strategy="json")
extraction_prompt = render_template_with_tools("finchat_prompt", tools=tools, formatter_strategy="extraction")
```

## Formatting Strategies

### `"simple"` - Basic listing
```
calculate_risk:
  - portfolio (str): required

get_stock_info:
  - symbol (str): required
```

### `"detailed"` - With extraction hints (default)
```
=== CALCULATE_RISK ARGUMENTS ===
• portfolio (str) - REQUIRED
  Look for: portfolio description, asset types mentioned, investment mix, crypto/stocks/bonds

=== GET_STOCK_INFO ARGUMENTS ===
• symbol (str) - REQUIRED
  Look for: stock ticker symbols, AAPL, MSFT, TSLA, company abbreviations, stock codes
```

### `"json"` - JSON schema format
```json
{
  "calculate_risk": {
    "type": "object",
    "properties": {
      "portfolio": {
        "type": "string",
        "description": "Look for: portfolio description, asset types mentioned..."
      }
    },
    "required": ["portfolio"]
  }
}
```

### `"extraction"` - Visual indicators
```
🔍 CALCULATE_RISK - What to extract:
  ✅ MUST FIND: portfolio (Look for: portfolio description, asset types mentioned...)

🔍 GET_STOCK_INFO - What to extract:
  ✅ MUST FIND: symbol (Look for: stock ticker symbols, AAPL, MSFT, TSLA...)
```

## Adding Custom Tool Specifications

Edit `TOOL_ARGUMENT_SPECS` in `prompts.py`:

```python
TOOL_ARGUMENT_SPECS = {
    "your_tool_name": {
        "parameter_name": {
            "type": "str",
            "required": True,
            "hints": ["what to look for", "examples", "patterns"]
        }
    }
}
```

## Benefits

- **Better argument extraction**: LLMs get clear guidance on what to extract from user input
- **Multiple formats**: Choose the strategy that works best for your use case
- **Backward compatible**: Existing code continues to work
- **Extensible**: Easy to add specifications for new tools