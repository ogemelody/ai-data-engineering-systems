
from agent import run_agent

question = (
    "How many columns are in the dataset? "
    "Which category generated the highest revenue? "
    "Are there any missing values? "
    "What is the total revenue?"
)

result = run_agent(question)

print("\nSTRUCTURED AGENT RESPONSE:")
print(result.model_dump_json(indent=2))

print("\nHUMAN-READABLE ANSWER:")
print(result.answer)
