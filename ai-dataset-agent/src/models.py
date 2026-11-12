
from pydantic import BaseModel, ConfigDict, Field, model_validator
import math
from typing import Self


class SalesMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_revenue: float = Field(ge=0, allow_inf_nan=False)
    revenue_by_category: dict[str, float]
    top_category: str | None

    @model_validator(mode="after")
    def validate_revenue_consistency(self) -> Self:
        category_revenues = self.revenue_by_category

        # Ensure every category revenue is valid.
        for category, revenue in category_revenues.items():
            if not math.isfinite(revenue) or revenue < 0:
                raise ValueError(
                    f"Invalid revenue for category: {category}"
                )

        # Calculate the expected total.
        calculated_total = sum(category_revenues.values())

        # Compare totals, accounting for small
        # floating-point differences.
        if not math.isclose(
            self.total_revenue,
            calculated_total,
            rel_tol=1e-9,
            abs_tol=1e-6,
        ):
            raise ValueError(
                "Revenue mismatch: "
                f"reported={self.total_revenue}, "
                f"calculated={calculated_total}"
            )

        # Validate that the top category is consistent.
        if category_revenues:
            expected_top = max(
                category_revenues,
                key=category_revenues.get,
            )

            if self.top_category != expected_top:
                raise ValueError(
                    "Top category mismatch: "
                    f"expected={expected_top}, "
                    f"received={self.top_category}"
                )
        elif self.top_category is not None:
            raise ValueError(
                "Top category must be None for empty results"
            )

        return self



class DatasetProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_rows: int = Field(ge=0)
    missing_values: dict[str, int]
    duplicate_rows: int = Field(ge=0)


class DatasetSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    row_count: int = Field(ge=0)
    column_count: int = Field(ge=0)
    columns: list[dict[str, str]]



class DatasetAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str
    column_count: int | None
    total_revenue: float | None
    top_category: str | None
    missing_values: dict[str, int] | None
