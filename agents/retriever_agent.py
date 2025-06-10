import asyncio
from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from models import SubtaskResult, LegalQuery, LegalFinding, Citation
from legal_apis import legal_api_manager
from vector_store import vector_store

class RetrieverAgent(BaseAgent):
    def __init__(self):
        super().__init__("Retriever")
    
    async def execute(self, input_data: LegalQuery) -> SubtaskResult:
        try:
            api_citations = await legal_api_manager.search_all_sources(
                input_data.query, 
                input_data.jurisdiction
            )
            
            vector_results = vector_store.search(input_data.query, k=10)
            
            findings = []
            
            for citation in api_citations[:5]:
                finding = LegalFinding(
                    content=f"Case: {citation.case_name}",
                    source="Legal Database",
                    citations=[citation],
                    relevance_score=citation.relevance_score,
                    authority_score=self._calculate_authority_score(citation)
                )
                findings.append(finding)
            
            for result in vector_results[:5]:
                if result["score"] > 0.7:
                    finding = LegalFinding(
                        content=result["content"],
                        source="Vector Store",
                        citations=[],
                        relevance_score=result["score"],
                        authority_score=0.8
                    )
                    findings.append(finding)
            
            enhanced_findings = await self._enhance_findings(findings, input_data.query)
            
            return SubtaskResult(
                task_type="retrieval",
                success=True,
                data=enhanced_findings,
                processing_time=0
            )
            
        except Exception as e:
            return SubtaskResult(
                task_type="retrieval",
                success=False,
                data=None,
                processing_time=0
            )
    
    def _calculate_authority_score(self, citation: Citation) -> float:
        authority_map = {
            "Supreme Court": 1.0,
            "Court of Appeals": 0.9,
            "Federal": 0.8,
            "District": 0.7
        }
        
        for court_type, score in authority_map.items():
            if court_type.lower() in citation.court.lower():
                return score
        
        return 0.6
    
    async def _enhance_findings(self, findings: List[LegalFinding], query: str) -> List[LegalFinding]:
        enhancement_prompt = f"""
        Given the legal query: "{query}"
        
        Rank these findings by relevance and legal authority:
        {[f.content[:200] for f in findings]}
        
        Return only the indices of the top 5 most relevant findings.
        Format: [0, 1, 2, 3, 4]
        """
        
        try:
            response = await self.llm.apredict(enhancement_prompt)
            indices = eval(response.strip())
            return [findings[i] for i in indices if i < len(findings)]
        except Exception:
            return findings[:5]

retriever_agent = RetrieverAgent() 