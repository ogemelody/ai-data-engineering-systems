from agent import run_agent

#the foundation for measuring tool-selection accuracy and efficiency
executed_tools = []

answer = run_agent(
    "How many columns are in my dataset?",
    trace=executed_tools,
)

print("\nEXECUTED TOOLS:")
print(executed_tools)

print("\nSTRUCTURED RESPONSE:")
print(answer.model_dump_json(indent=2))