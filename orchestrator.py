import asyncio
import time
from typing import Dict, Any
from models import LegalQuery, LegalBrief, AgentResponse
from agents.retriever_agent import retriever_agent
from agents.analyzer_agent import analyzer_agent
from agents.summarizer_agent import summarizer_agent
from agents.composer_agent import composer_agent

class LegalResearchOrchestrator:
    def __init__(self):
        self.agents = {
            "retriever": retriever_agent,
            "analyzer": analyzer_agent,
            "summarizer": summarizer_agent,
            "composer": composer_agent
        }
    
    async def process_legal_query(self, query: LegalQuery) -> AgentResponse:
        start_time = time.time()
        
        try:
            retrieval_result = await self.agents["retriever"].execute_with_retry(query)
            
            if not retrieval_result.success:
                return AgentResponse(
                    success=False,
                    error="Failed to retrieve legal information",
                    processing_time=time.time() - start_time
                )
            
            findings = retrieval_result.data
            
            analysis_result = await self.agents["analyzer"].execute_with_retry(findings)
            
            if not analysis_result.success:
                return AgentResponse(
                    success=False,
                    error="Failed to analyze legal findings",
                    processing_time=time.time() - start_time
                )
            
            summary_input = {
                "findings": findings,
                "analysis": analysis_result.data,
                "query": query.query
            }
            
            summary_result = await self.agents["summarizer"].execute_with_retry(summary_input)
            
            if not summary_result.success:
                return AgentResponse(
                    success=False,
                    error="Failed to summarize findings",
                    processing_time=time.time() - start_time
                )
            
            composition_input = {
                "query": query.query,
                "findings": findings,
                "analysis": analysis_result.data,
                "summary": summary_result.data
            }
            
            composition_result = await self.agents["composer"].execute_with_retry(composition_input)
            
            if not composition_result.success:
                return AgentResponse(
                    success=False,
                    error="Failed to compose legal brief",
                    processing_time=time.time() - start_time
                )
            
            processing_time = time.time() - start_time
            
            return AgentResponse(
                success=True,
                data=composition_result.data,
                processing_time=processing_time
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Orchestration error: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    async def get_health_status(self) -> Dict[str, Any]:
        health_status = {
            "orchestrator": "healthy",
            "agents": {},
            "timestamp": time.time()
        }
        
        for agent_name, agent in self.agents.items():
            try:
                health_status["agents"][agent_name] = "healthy"
            except Exception:
                health_status["agents"][agent_name] = "unhealthy"
        
        return health_status
    
    async def validate_query(self, query: LegalQuery) -> Dict[str, Any]:
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not query.query or len(query.query.strip()) < 10:
            validation_result["valid"] = False
            validation_result["errors"].append("Query must be at least 10 characters long")
        
        if query.jurisdiction and len(query.jurisdiction) < 2:
            validation_result["warnings"].append("Jurisdiction should be more specific")
        
        return validation_result

orchestrator = LegalResearchOrchestrator() 