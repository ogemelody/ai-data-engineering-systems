
import json

from dotenv import load_dotenv
from openai import OpenAI

from src.dispatcher import execute_tool
from src.tool_schemas import TOOLS

load_dotenv()

client = OpenAI()


def run_agent(question: str) -> str:
    inputs = [
        {
            "role": "user",
            "content": question
        }
    ]

    instructions = (
        """
You are a specialized Data Engineering Dataset Inspection Agent.

Your responsibilities are limited to:
1. Inspecting the schema of the sales dataset.
2. Profiling the dataset for missing values and duplicates.
3. Calculating sales metrics using approved Python tools.

Rules:
- Use the available tools for dataset questions.
- Never invent dataset values or calculations.
- Never claim to have accessed data you haven't accessed.
- If a question is outside dataset analysis, politely explain
  that it is outside your supported capabilities.
- Do not answer unrelated general knowledge questions.
- Do not suggest external tools or services for unrelated tasks.
- Do not assume a currency unless the dataset specifies one.
- When a tool fails, explain the limitation.
"""
    )

# We're limiting the execution to five iterations for this learning project.
# In production, we'd also add timeouts, rate limits, cost controls, and more robust exception handling.

    for step in range(5):
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=inputs,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False
        )

        # Preserve the model output, including tool requests.
        inputs.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            return response.output_text or "No answer generated."

        for call in tool_calls:
            print(f"Executing: {call.name}")
            print(f"Call ID: {call.call_id}")
            print(f"Arguments: {call.arguments}")

            try:
                arguments = json.loads(call.arguments)
                result = execute_tool(call.name, arguments)

                print(f"Tool result: {result}")

            except (ValueError, TypeError, KeyError) as exc:
                result = {
                    "error": type(exc).__name__,
                    "message": str(exc)
                }

            # Return the actual Python result to the model.
            inputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result)
            })

    raise RuntimeError("Agent exceeded its step limit.")
