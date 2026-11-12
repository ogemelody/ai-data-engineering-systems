
import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict

from src.tools import calculate_metrics


load_dotenv()

client = OpenAI()


# Define the expected structure of the LLM response.
class SalesSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    top_category: str
    total_revenue: float
    explanation: str


# Step 1: Compute trusted metrics with Pandas.
metrics = calculate_metrics()

print("SOURCE METRICS:")
print(json.dumps(metrics, indent=2))


# Step 2: Ask the model to return structured data.
response = client.responses.parse(
    model="gpt-5-mini",
    instructions=(
        "You are a data engineering assistant. "
        "Summarize the provided sales metrics. "
        "Use only the supplied values. "
        "Do not invent numbers or currency units."
    ),
    input=json.dumps(metrics),
    text_format=SalesSummary,
)

# Step 3: Get the parsed Pydantic object.
summary = response.output_parsed

if summary is None:
    raise RuntimeError(
        "The model did not return a structured response."
    )

print("\nSTRUCTURED LLM RESPONSE:")
print(summary.model_dump_json(indent=2))


# Step 4: Verify the response against source calculations.
if summary.total_revenue != metrics["total_revenue"]:
    raise ValueError("Revenue does not match source data")

if summary.top_category != metrics["top_category"]:
    raise ValueError("Top category does not match source data")

print("\nValidation against source data passed.")
