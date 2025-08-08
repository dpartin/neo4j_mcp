# mcp/router.py

import logging
from fastapi import APIRouter, Request, HTTPException
from mcp.validator import validate_message
from mcp.neo4j_client import neo4j_client

import uuid
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# Neo4j handlers with actual implementation
async def handle_neo4j_create_node(payload: dict):
    """Handle node creation requests."""
    try:
        labels = payload.get("labels", [])
        properties = payload.get("properties", {})
        
        if not properties:
            raise ValueError("Node properties are required")
        
        result = await neo4j_client.create_node(labels, properties)
        return result
    except Exception as e:
        logger.error(f"Error in create_node handler: {e}")
        return {"status": "error", "message": str(e)}

async def handle_run_cypher_query(payload: dict):
    """Handle Cypher query execution requests."""
    try:
        query = payload.get("query")
        parameters = payload.get("parameters", {})
        
        if not query:
            raise ValueError("Cypher query is required")
        
        result = await neo4j_client.run_cypher_query(query, parameters)
        return result
    except Exception as e:
        logger.error(f"Error in run_cypher_query handler: {e}")
        return {"status": "error", "message": str(e)}

async def handle_neo4j_create_relationship(payload: dict):
    """Handle relationship creation requests."""
    try:
        from_node_id = payload.get("from_node_id")
        to_node_id = payload.get("to_node_id")
        rel_type = payload.get("rel_type")
        properties = payload.get("properties", {})
        
        if not all([from_node_id, to_node_id, rel_type]):
            raise ValueError("from_node_id, to_node_id, and rel_type are required")
        
        result = await neo4j_client.create_relationship(
            from_node_id, to_node_id, rel_type, properties
        )
        return result
    except Exception as e:
        logger.error(f"Error in create_relationship handler: {e}")
        return {"status": "error", "message": str(e)}

# Map (target, action) to handler functions
HANDLERS = {
    ("neo4j", "create_node"): handle_neo4j_create_node,
    ("neo4j", "run_cypher_query"): handle_run_cypher_query,
    ("neo4j", "create_relationship"): handle_neo4j_create_relationship,
}

@router.post("/mcp/message")
async def route_message(request: Request):
    message = await request.json()
    # 1. Validate schema
    validate_message(message)

    # 2. Dispatch to handler
    key = (message["target"], message["action"])
    handler = HANDLERS.get(key)
    if not handler:
        raise HTTPException(status_code=404, detail=f"No handler for target={key[0]} action={key[1]}")

    # 3. Invoke handler and build response
    result = await handler(message["payload"])
    response = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": "response",
        "response_to": message["id"],
        "target": message["target"],
        "payload": result,
    }
    return response