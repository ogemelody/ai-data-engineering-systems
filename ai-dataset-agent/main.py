from src.tools import (
    inspect_schema,
    profile_dataset,
    calculate_metrics
)

print("SCHEMA:")
print(inspect_schema())

print("\nDATA QUALITY:")
print(profile_dataset())

print("\nSALES METRICS:")
print(calculate_metrics())