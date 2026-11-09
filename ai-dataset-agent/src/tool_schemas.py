
TOOLS = [
    {
        "type": "function",
        "name": "inspect_schema",
        "description": (
            "Inspect the sales dataset and return its "
            "columns, data types, and row count."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "profile_dataset",
        "description": (
            "Check the sales dataset for missing "
            "values and duplicate rows."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "calculate_metrics",
        "description": (
            "Calculate sales revenue, revenue by "
            "category, and the top category."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
]
