# Dataset Intelligence Agent

A controlled AI data system for inspecting datasets, profiling data quality, calculating business metrics, and returning validated structured responses.

This project demonstrates how to combine deterministic data processing with LLM-driven tool selection while maintaining clear execution boundaries and validation controls.

## Why this project exists

AI systems that work with data should not rely on the language model to perform calculations or access data arbitrarily.

This project separates responsibilities across:

- deterministic Python computation
- model-driven tool selection
- explicit tool schemas
- allowlisted function execution
- Pydantic validation
- structured outputs
- source-result verification
- scope and permission controls
- automated testing
- agent evaluation

## Architecture

User Question
    ↓
LLM
    ↓
Tool Selection
    ↓
Approved Python Dispatcher
    ↓
Pandas / Dataset
    ↓
Validated Tool Results
    ↓
Structured LLM Response
    ↓
Pydantic + Source Verification
    ↓
Final Response

## Capabilities

The agent currently supports:

- inspecting dataset schema
- counting rows and columns
- profiling missing values
- detecting duplicate rows
- calculating total revenue
- calculating revenue by category
- identifying the top revenue category
- returning machine-readable structured responses
- rejecting unsupported operations

## Tooling

- Python
- Pandas
- OpenAI Responses API
- Function Calling
- Pydantic
- Pytest
- uv

## Agent Tools

### `inspect_schema`

Returns:

- row count
- column count
- column names
- inferred data types

### `profile_dataset`

Returns:

- total rows
- missing-value counts
- duplicate-row count

### `calculate_metrics`

Returns:

- total revenue
- revenue by category
- top-performing category




The dispatcher only executes registered tools.

Unsupported operations such as record deletion are rejected.

### Pydantic validation

Tool outputs are validated for:

- required fields
- types
- non-negative values
- unexpected fields



### Structured response verification

Structured LLM fields are checked against the successful tool results that produced them.

A field such as `column_count` cannot be accepted unless `inspect_schema` was actually executed.

## Testing

The project includes deterministic unit tests for:

- tool calculations
- Pydantic models
- dispatcher permission boundaries






## Understand the Schema (tools_schema)

| Property | Purpose |
|---|---|
| `type: function` | Declares a callable tool |
| `name` | Identifies which Python operation the model can request |
| `description` | Helps the model decide when to use the tool |
| `parameters` | Defines accepted arguments and their types |
| `properties: {}` | Our functions currently accept no arguments |
| `additionalProperties: false` | Prevents unexpected argument fields in strict mode |
| `strict: true` | Enforces supported schema constraints for generated tool arguments |

This follows the current OpenAI Responses API function-tool format.

