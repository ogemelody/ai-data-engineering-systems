
import pytest

from src.dispatcher import execute_tool


def test_approved_tool_executes():
    result = execute_tool("inspect_schema", {})

    assert result["row_count"] == 8


def test_unknown_tool_is_rejected():
    with pytest.raises(ValueError, match="Unknown tool"):
        execute_tool("delete_sales_records", {})


def test_unexpected_arguments_rejected():
    with pytest.raises(ValueError):
        execute_tool(
            "calculate_metrics",
            {"delete_all": True},
        )
