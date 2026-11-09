

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
