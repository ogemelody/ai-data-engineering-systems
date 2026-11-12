
from agent import run_agent

question = (
     "How many columns are in my dataset, "
    "and what is the total revenue?"
)

result = run_agent(question)

print("\nSTRUCTURED AGENT RESPONSE:")
print(result.model_dump_json(indent=2))

print("\nHUMAN-READABLE ANSWER:")
print(result.answer)
