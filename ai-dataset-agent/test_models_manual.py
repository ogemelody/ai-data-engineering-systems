
from pydantic import ValidationError

from src.models import SalesMetrics
from src.tools import calculate_metrics


def run_validation_test(label: str, data: dict):
    print(f"\nTEST: {label}")

    try:
        validated = SalesMetrics.model_validate(data)
        print("VALIDATION SUCCESSFUL")
        print(validated.model_dump_json(indent=2))

    except ValidationError as error:
        print("VALIDATION FAILED")
        print(error)


# Test 1: Original, correct dataset
correct_metrics = calculate_metrics()

run_validation_test(
    "Correct sales metrics",
    correct_metrics
)


# Test 2: Incorrect total
incorrect_total = calculate_metrics()
incorrect_total["total_revenue"] = 9999.0

run_validation_test(
    "Incorrect total revenue",
    incorrect_total
)


# Test 3: Incorrect top category
incorrect_category = calculate_metrics()
incorrect_category["top_category"] = "Office"

run_validation_test(
    "Incorrect top category",
    incorrect_category
)
