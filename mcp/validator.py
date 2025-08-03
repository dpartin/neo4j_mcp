# mcp/validator.py

from jsonschema import validate, ValidationError
from fastapi import HTTPException
from mcp.schema import MCP_JSON_SCHEMA

def validate_message(message: dict) -> None:
    """
    Validate an incoming MCP message against the JSON schema.
    Raises HTTPException(400) if validation fails.
    """
    try:
        validate(instance=message, schema=MCP_JSON_SCHEMA)
    except ValidationError as e:
        # You can extract e.path or e.message for more details
        raise HTTPException(status_code=400, detail=f"Invalid MCP message: {e.message}")