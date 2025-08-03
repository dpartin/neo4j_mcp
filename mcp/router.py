# mcp/router.py

from fastapi import APIRouter, Request, HTTPException
from mcp.validator import validate_message

import uuid
from datetime import datetime


router = APIRouter()

# Stub handlers for demonstration
async def handle_neo4j_create_node(payload: dict):
    # TODO: implement Neo4j creation logic
    return {"status": "success", "detail": "node created"}

async def handle_run_cypher_query(payload: dict):
    # TODO: implement Cypher query logic
    return {"status": "success", "results": []}

# Map (target, action) to handler functions
HANDLERS = {
    ("neo4j", "create_node"): handle_neo4j_create_node,
    ("neo4j", "run_cypher_query"): handle_run_cypher_query,
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