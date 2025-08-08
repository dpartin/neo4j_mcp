# mcp/neo4j_client.py

import logging
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver
from config import settings

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j client wrapper for MCP operations."""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )
            # Test connection
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
    
    async def create_node(self, labels: List[str], properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new node with given labels and properties."""
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                # Build Cypher query
                label_str = ":".join(labels) if labels else ""
                props_str = ", ".join([f"{k}: ${k}" for k in properties.keys()])
                
                query = f"CREATE (n{':' + label_str if label_str else ''} {{{props_str}}}) RETURN n"
                
                result = session.run(query, properties)
                node = result.single()["n"]
                
                return {
                    "status": "success",
                    "node_id": node.id,
                    "labels": list(node.labels),
                    "properties": dict(node)
                }
        except Exception as e:
            logger.error(f"Error creating node: {e}")
            return {"status": "error", "message": str(e)}
    
    async def run_cypher_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a Cypher query and return results."""
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                result = session.run(query, parameters or {})
                records = [dict(record) for record in result]
                
                return {
                    "status": "success",
                    "results": records,
                    "count": len(records)
                }
        except Exception as e:
            logger.error(f"Error executing Cypher query: {e}")
            return {"status": "error", "message": str(e)}
    
    async def create_relationship(self, from_node_id: int, to_node_id: int, 
                                rel_type: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a relationship between two nodes."""
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                props_str = ", ".join([f"{k}: ${k}" for k in (properties or {}).keys()])
                props_clause = f"{{{props_str}}}" if properties else ""
                
                query = f"""
                MATCH (a), (b) 
                WHERE id(a) = $from_id AND id(b) = $to_id
                CREATE (a)-[r:{rel_type} {props_clause}]->(b)
                RETURN r
                """
                
                params = {"from_id": from_node_id, "to_id": to_node_id, **(properties or {})}
                result = session.run(query, params)
                relationship = result.single()["r"]
                
                return {
                    "status": "success",
                    "relationship_id": relationship.id,
                    "type": relationship.type,
                    "properties": dict(relationship)
                }
        except Exception as e:
            logger.error(f"Error creating relationship: {e}")
            return {"status": "error", "message": str(e)}


# Global Neo4j client instance
neo4j_client = Neo4jClient()
