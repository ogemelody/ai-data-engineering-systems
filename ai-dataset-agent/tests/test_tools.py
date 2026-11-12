
import pytest

from src.tools import (
    inspect_schema,
    profile_dataset,
    calculate_metrics,
)


def test_schema():
    result = inspect_schema()

    assert result["row_count"] == 8
    assert result["column_count"] == 6


def test_missing_values():
    result = profile_dataset()

    assert all(
        count == 0
        for count in result["missing_values"].values()
    )


def test_duplicates():
    result = profile_dataset()

    assert result["duplicate_rows"] == 0


def test_total_revenue():
    result = calculate_metrics()

    assert result["total_revenue"] == pytest.approx(1140.0)


def test_category_revenue():
    result = calculate_metrics()

    assert result["revenue_by_category"] == {
        "Electronics": 590.0,
        "Furniture": 490.0,
        "Office": 60.0,
    }


def test_top_category():
    result = calculate_metrics()

    assert result["top_category"] == "Electronics"
