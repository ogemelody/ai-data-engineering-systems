
import pandas as pd

DATASET_PATH = "data/sales.csv"


def inspect_schema() -> dict:
    """
    Inspect the dataset structure without using an LLM.
    """
    df = pd.read_csv(DATASET_PATH)

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": [
            {
                "name": col,
                "dtype": str(df[col].dtype)
            }
            for col in df.columns
        ]
    }



def profile_dataset() -> dict:
    df = pd.read_csv(DATASET_PATH)

    return {
        "total_rows": len(df),
        "missing_values": {
            col: int(count)
            for col, count in df.isna().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum())
    }


def calculate_metrics() -> dict:
    df = pd.read_csv(DATASET_PATH)

    required = {"category", "quantity", "unit_price"}

    if not required.issubset(df.columns):
        raise ValueError("Missing required sales columns")

    if df[list(required)].isna().any().any():
        raise ValueError("Missing values in required sales columns")

    if not pd.api.types.is_numeric_dtype(df["quantity"]):
        raise ValueError("Quantity must be numeric")

    if not pd.api.types.is_numeric_dtype(df["unit_price"]):
        raise ValueError("Unit price must be numeric")

    if (df["quantity"] < 0).any() or (df["unit_price"] < 0).any():
        raise ValueError("Negative quantities or prices found")

    df["revenue"] = df["quantity"] * df["unit_price"]

    by_category = df.groupby("category")["revenue"].sum()

    return {
        "total_revenue": float(df["revenue"].sum()),
        "revenue_by_category": {
            category: float(revenue)
            for category, revenue in by_category.items()
        },
        "top_category": (
            str(by_category.idxmax()) if not by_category.empty else None
        )
    }
