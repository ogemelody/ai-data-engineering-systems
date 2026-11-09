from agent import run_agent

question = (
    "How many columns are in my dataset?"
    "Which category generated the highest revenue?"
    "Check the dataset for missing values and give me total revenue."
)

answer = run_agent(question)

print("\nAGENT RESPONSE:")
print(answer)
