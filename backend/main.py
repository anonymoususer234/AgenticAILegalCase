from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
import logging

from models import LegalQuery, AgentResponse
from orchestrator import orchestrator
from vector_store import vector_store

app = FastAPI(
    title="Autonomous Legal Research Assistant",
    description="AI-powered legal research system with autonomous agents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/research", response_model=AgentResponse)
async def research_legal_query(query: LegalQuery):
    try:
        validation = await orchestrator.validate_query(query)
        
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid query: {', '.join(validation['errors'])}"
            )
        
        result = await orchestrator.process_legal_query(query)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Research endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/health")
async def health_check():
    try:
        health_status = await orchestrator.get_health_status()
        return JSONResponse(content=health_status)
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return JSONResponse(
            content={"status": "unhealthy", "error": str(e)},
            status_code=503
        )

@app.post("/api/add-documents")
async def add_documents(documents: Dict[str, Any]):
    try:
        docs = documents.get("documents", [])
        metadata = documents.get("metadata", [])
        
        if len(docs) != len(metadata):
            raise HTTPException(
                status_code=400,
                detail="Documents and metadata arrays must have the same length"
            )
        
        vector_store.add_documents(docs, metadata)
        
        return {"message": f"Successfully added {len(docs)} documents"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add documents error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add documents")

@app.get("/api/search")
async def search_documents(query: str, k: int = 5):
    try:
        results = vector_store.search(query, k)
        return {"results": results}
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/api/agents/status")
async def get_agents_status():
    try:
        health_status = await orchestrator.get_health_status()
        return {"agents": health_status["agents"]}
    except Exception as e:
        logger.error(f"Agents status error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get agents status")

@app.post("/api/validate-query")
async def validate_query(query: LegalQuery):
    try:
        validation = await orchestrator.validate_query(query)
        return validation
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Validation failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 