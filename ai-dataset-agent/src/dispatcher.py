# connects the function names the LLM knows about to your actual Python functions.

from src.tools import (
    inspect_schema,
    profile_dataset,
    calculate_metrics
)

AVAILABLE_FUNCTIONS = {
    "inspect_schema": inspect_schema,
    "profile_dataset": profile_dataset,
    "calculate_metrics": calculate_metrics
}


def execute_tool(name: str, arguments: dict) -> dict:
    if name not in AVAILABLE_FUNCTIONS:
        raise ValueError(f"Unknown tool: {name}")

    if arguments:
        raise ValueError(
            f"Tool {name} does not accept arguments"
        )

    function = AVAILABLE_FUNCTIONS[name]

    return function()

#The model cannot call every Python function on your computer.
# It can only request functions you've made available through your tool definitions, dispatcher independently enforces that allowlist.