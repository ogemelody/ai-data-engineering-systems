
import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from src.dispatcher import execute_tool
from src.tool_schemas import TOOLS
from src.models import DatasetAnswer

load_dotenv()

client = OpenAI()


def run_agent(question: str) -> DatasetAnswer:
    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    inputs = [
        {"role": "user", "content": question}
    ]

    instructions = """
    You are a read-only Dataset Inspection Agent.

    Supported capabilities:
    - Inspect the dataset schema
    - Profile missing values and duplicates
    - Calculate sales metrics

    Use approved tools to establish dataset facts.
    Never invent numbers or claim unperformed actions.
    Do not assume a currency.
    For out-of-scope requests, explain the limitation.

    Populate structured fields only when supported
    by actual tool results. Otherwise use null.
    """

    # Keep trusted results from executed tools.
    verified_results = {}

    for step in range(8):
        response = client.responses.parse(
            model="gpt-5-mini",
            instructions=instructions,
            input=inputs,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,
            text_format=DatasetAnswer,
        )

        inputs.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            answer = response.output_parsed

            if answer is None:
                raise RuntimeError(
                    "No structured response returned."
                )

            # Verify structured values against
            # successful Python tool results.
            checks = [
                ("column_count", "inspect_schema"),
                ("total_revenue", "calculate_metrics"),
                ("top_category", "calculate_metrics"),
                ("missing_values", "profile_dataset"),
            ]

            for field, tool_name in checks:
                value = getattr(answer, field)

                if value is None:
                    continue

                if tool_name not in verified_results:
                    raise ValueError(
                        f"{field} has no supporting tool result"
                    )

                expected = verified_results[tool_name][field]

                if value != expected:
                    raise ValueError(
                        f"{field} differs from tool output: "
                        f"{value!r} != {expected!r}"
                    )

            return answer

        for call in tool_calls:
            print(f"Executing: {call.name}")

            try:
                arguments = json.loads(call.arguments)

                result = execute_tool(
                    call.name, arguments
                )

                verified_results[call.name] = result

            except (
                ValueError,
                TypeError,
                KeyError,
                ValidationError,
            ) as exc:
                result = {
                    "error": type(exc).__name__,
                    "message": "Tool execution failed."
                }

            inputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result)
            })

    raise RuntimeError("Agent exceeded step limit.")
