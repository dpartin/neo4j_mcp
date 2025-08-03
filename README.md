# MCP Server with Neo4j Support

A modular, context-aware server that implements a Model Context Protocol (MCP) to orchestrate AI agents and provide graph creation, modification, and augmentation via Neo4j for Retrieval-Augmented Generation (RAG).

## Overview

This project defines a JSON-based MCP schema for structured messaging between agents and services. It includes a validation and routing scaffold, with pluggable handlers for Neo4j CRUD operations and graph augmentation workflows.

## Architecture

### Core Modules

| Module | Description |
|--------|-------------|
| Context Manager | Stores shared context such as extracted entities and user intents |
| MCP Protocol Engine | Routes and validates messages according to the MCP schema |
| Graph Interface Layer | Wraps Neo4j operations (CRUD, Cypher queries) exposed via MCP actions |
| Augmentation Engine | Transforms graph data into embeddings or prompt snippets for RAG |
| Model Agents | Specialized agents (e.g., NER, summarizer, retriever) communicating over MCP |
| API Gateway | Exposes endpoints for external clients or workflows |

### Tech Stack

| Layer | Tools/Technologies |
|-------|-------------------|
| Backend | Python, FastAPI |
| Validation | jsonschema |
| Messaging | JSON-over-HTTP |
| Graph Database | Neo4j with neo4j-driver or py2neo |
| Containerization | Docker, Kubernetes or GCP Cloud Run |
| Observability | Prometheus, Grafana, OpenTelemetry |

## MCP Message Schema

The following JSON Schema defines the structure for all MCP messages:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MCP Message",
  "type": "object",
  "required": ["id", "timestamp", "type", "action", "target", "payload"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
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
      "additionalProperties": true
    }
  }
}
```

## Router & Validator Scaffold

### Project Structure
```
mcp_server/
├── main.py
├── mcp
│   ├── __init__.py
│   ├── schema.py
│   ├── validator.py
│   └── router.py
└── requirements.txt
```

### Validator (mcp/validator.py)
```python
from jsonschema import validate, ValidationError
from fastapi import HTTPException
from mcp.schema import MCP_JSON_SCHEMA

def validate_message(message: dict) -> None:
    try:
        validate(instance=message, schema=MCP_JSON_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid MCP message: {e.message}")
```

### Router (mcp/router.py)
```python
import uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from mcp.validator import validate_message

router = APIRouter()

# Stub handlers
async def handle_neo4j_create_node(payload: dict):
    return {"status": "success", "detail": "node created"}

async def handle_run_cypher_query(payload: dict):
    return {"status": "success", "results": []}

# Handler map
HANDLERS = {
    ("neo4j", "create_node"): handle_neo4j_create_node,
    ("neo4j", "run_cypher_query"): handle_run_cypher_query,
}

@router.post("/mcp/message")
async def route_message(request: Request):
    message = await request.json()
    validate_message(message)
    key = (message["target"], message["action"])
    handler = HANDLERS.get(key)
    if not handler:
        raise HTTPException(status_code=404, detail=f"No handler for {key}")
    result = await handler(message["payload"])
    response = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": "response",
        "response_to": message["id"],
        "target": message["target"],
        "payload": result
    }
    return response
```

### Main Application (main.py)
```python
from fastapi import FastAPI
from mcp.router import router

app = FastAPI(title="MCP Server with Neo4j Support")
app.include_router(router)
```

## Neo4j Integration Options

| Library | Style | Pros | Cons |
|---------|-------|------|------|
| neo4j-driver | Low-level Bolt driver | Official support, high performance | Requires manual session/transaction management |
| py2neo | High-level OGM toolkit | Pythonic API, graph-object mapper | May lag behind Neo4j releases |

## Next Steps

- Define custom MCP actions for RAG (e.g., merge_subgraph, extract_paths)
- Implement Neo4j handlers using neo4j-driver or py2neo
- Build the Augmentation Engine to transform subgraphs into embeddings or prompt context
- Add authentication, logging, and tracing middleware
- Containerize the application with Docker and deploy on Kubernetes or Cloud Run
