# MCP Server with Neo4j Support

A modular, context-aware server that implements a Model Context Protocol (MCP) to orchestrate AI agents and provide graph creation, modification, and augmentation via Neo4j for Retrieval-Augmented Generation (RAG).

## Overview

This project defines a JSON-based MCP schema for structured messaging between agents and services. It includes a validation and routing scaffold, with pluggable handlers for Neo4j CRUD operations and graph augmentation workflows.

## Architecture

### Core Modules

| Module                | Description                                                                  |
| --------------------- | ---------------------------------------------------------------------------- |
| Context Manager       | Stores shared context such as extracted entities and user intents            |
| MCP Protocol Engine   | Routes and validates messages according to the MCP schema                    |
| Graph Interface Layer | Wraps Neo4j operations (CRUD, Cypher queries) exposed via MCP actions        |
| Augmentation Engine   | Transforms graph data into embeddings or prompt snippets for RAG             |
| Model Agents          | Specialized agents (e.g., NER, summarizer, retriever) communicating over MCP |
| API Gateway           | Exposes endpoints for external clients or workflows                          |

### Tech Stack

| Layer            | Tools/Technologies      |
| ---------------- | ----------------------- |
| Backend          | Python, FastAPI         |
| Validation       | jsonschema              |
| Messaging        | JSON-over-HTTP          |
| Graph Database   | Neo4j with neo4j-driver |
| Containerization | Docker, Docker Compose  |
| Testing          | pytest, httpx           |

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Neo4j 5.14.1 (included in Docker setup)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd neo4j_mcp
   ```

2. **Set up environment variables:**

   ```bash
   cp env.example .env
   # Edit .env with your Neo4j credentials
   ```

3. **Run with Docker Compose (recommended):**

   ```bash
   docker-compose up -d
   ```

4. **Or run locally:**
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

### API Endpoints

- **Health Check:** `GET /` and `GET /health`
- **MCP Messages:** `POST /api/v1/mcp/message`

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

## Supported Actions

### Neo4j Operations

| Action                | Target  | Payload                                                                  | Description          |
| --------------------- | ------- | ------------------------------------------------------------------------ | -------------------- |
| `create_node`         | `neo4j` | `{"labels": [], "properties": {}}`                                       | Create a new node    |
| `run_cypher_query`    | `neo4j` | `{"query": "", "parameters": {}}`                                        | Execute Cypher query |
| `create_relationship` | `neo4j` | `{"from_node_id": 1, "to_node_id": 2, "rel_type": "", "properties": {}}` | Create relationship  |

### Example Usage

#### Create a Person Node

```bash
curl -X POST "http://localhost:8000/api/v1/mcp/message" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2024-01-01T12:00:00Z",
    "type": "request",
    "action": "create_node",
    "target": "neo4j",
    "payload": {
      "labels": ["Person"],
      "properties": {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
      }
    }
  }'
```

#### Execute Cypher Query

```bash
curl -X POST "http://localhost:8000/api/v1/mcp/message" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "timestamp": "2024-01-01T12:00:00Z",
    "type": "request",
    "action": "run_cypher_query",
    "target": "neo4j",
    "payload": {
      "query": "MATCH (p:Person) RETURN p.name, p.age LIMIT 5",
      "parameters": {}
    }
  }'
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

```
neo4j_mcp/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Development environment
├── mcp/
│   ├── __init__.py
│   ├── schema.py         # MCP message schema
│   ├── validator.py      # Message validation
│   ├── router.py         # Request routing
│   └── neo4j_client.py  # Neo4j operations
├── tests/
│   ├── __init__.py
│   └── test_router.py    # Unit tests
└── README.md
```

## Configuration

Environment variables can be set in a `.env` file:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Logging
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Next Steps

### Phase 2: Advanced Features (Week 2-3)

- [ ] **Graph Augmentation Engine**: Transform subgraphs into embeddings
- [ ] **RAG Integration**: Connect with vector databases and LLMs
- [ ] **Advanced Cypher Operations**: Path finding, graph algorithms
- [ ] **Authentication & Authorization**: JWT tokens, role-based access

### Phase 3: Production Ready (Week 4)

- [ ] **Monitoring & Observability**: Prometheus metrics, structured logging
- [ ] **Error Handling**: Comprehensive error management and recovery
- [ ] **Performance Optimization**: Connection pooling, caching
- [ ] **Security Hardening**: Input validation, rate limiting

### Phase 4: AI Agent Integration (Week 5-6)

- [ ] **Agent Communication**: Multi-agent orchestration
- [ ] **Context Management**: Shared state and memory
- [ ] **Workflow Engine**: Complex graph operations
- [ ] **API Documentation**: OpenAPI/Swagger integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
