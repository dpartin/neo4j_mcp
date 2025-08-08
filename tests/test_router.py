# tests/test_router.py

import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMCPRouter:
    """Test cases for MCP router functionality."""
    
    def test_valid_create_node_message(self):
        """Test creating a node with valid MCP message."""
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "request",
            "action": "create_node",
            "target": "neo4j",
            "payload": {
                "labels": ["Person"],
                "properties": {"name": "John Doe", "age": 30}
            }
        }
        
        response = client.post("/api/v1/mcp/message", json=message)
        assert response.status_code == 200
        
        data = response.json()
        assert data["type"] == "response"
        assert data["response_to"] == message["id"]
        assert "payload" in data
    
    def test_valid_cypher_query_message(self):
        """Test executing Cypher query with valid MCP message."""
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "request",
            "action": "run_cypher_query",
            "target": "neo4j",
            "payload": {
                "query": "MATCH (n) RETURN n LIMIT 5",
                "parameters": {}
            }
        }
        
        response = client.post("/api/v1/mcp/message", json=message)
        assert response.status_code == 200
        
        data = response.json()
        assert data["type"] == "response"
        assert data["response_to"] == message["id"]
    
    def test_invalid_message_schema(self):
        """Test handling of invalid message schema."""
        invalid_message = {
            "id": "not-a-uuid",
            "timestamp": "invalid-timestamp",
            "type": "invalid-type",
            "action": "create_node",
            "target": "neo4j",
            "payload": {}
        }
        
        response = client.post("/api/v1/mcp/message", json=invalid_message)
        assert response.status_code == 400
    
    def test_unknown_handler(self):
        """Test handling of unknown target/action combination."""
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "request",
            "action": "unknown_action",
            "target": "neo4j",
            "payload": {}
        }
        
        response = client.post("/api/v1/mcp/message", json=message)
        assert response.status_code == 404
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        incomplete_message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "request",
            "action": "create_node",
            # Missing target and payload
        }
        
        response = client.post("/api/v1/mcp/message", json=incomplete_message)
        assert response.status_code == 400


class TestHealthEndpoints:
    """Test cases for health check endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "neo4j" in data
