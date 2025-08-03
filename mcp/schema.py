# mcp/schema.py

MCP_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "MCP Message",
    "type": "object",
    "required": ["id", "timestamp", "type", "action", "target", "payload"],
    "properties": {
        "id": {
            "type": "string",
            "format": "uuid",
            "description": "Unique message identifier"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp"
        },
        "type": {
            "type": "string",
            "enum": ["request", "response"]
        },
        "action": {
            "type": "string"
        },
        "target": {
            "type": "string"
        },
        "payload": {
            "type": "object"
        },
        "response_to": {
            "type": "string",
            "format": "uuid"
        },
        "metadata": {
            "type": "object",
            "additionalProperties": True
        }
    }
}