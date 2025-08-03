# main.py

from fastapi import FastAPI
from mcp.router import router

app = FastAPI(title="MCP Server with Neo4j Support")
app.include_router(router)