import httpx
import asyncio
from typing import List, Dict, Any, Optional
from config import settings
from models import Citation
from datetime import datetime
import json

class CourtListenerAPI:
    def __init__(self):
        self.base_url = "https://www.courtlistener.com/api/rest/v3"
        self.headers = {
            "Authorization": f"Token {settings.courtlistener_api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_cases(self, query: str, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            params = {
                "q": query,
                "type": "o",
                "order_by": "score desc",
                "format": "json"
            }
            
            if jurisdiction:
                params["court"] = jurisdiction
            
            try:
                response = await client.get(
                    f"{self.base_url}/search/",
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json().get("results", [])
            except Exception as e:
                return []
    
    async def get_case_details(self, case_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/opinions/{case_id}/",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception:
                return None

class HarvardCaselawAPI:
    def __init__(self):
        self.base_url = "https://api.case.law/v1"
    
    async def search_cases(self, query: str, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            params = {
                "search": query,
                "format": "json",
                "full_case": "true"
            }
            
            if jurisdiction:
                params["jurisdiction"] = jurisdiction
            
            try:
                response = await client.get(
                    f"{self.base_url}/cases/",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json().get("results", [])
            except Exception:
                return []

class LegalAPIManager:
    def __init__(self):
        self.courtlistener = CourtListenerAPI()
        self.harvard = HarvardCaselawAPI()
    
    async def search_all_sources(self, query: str, jurisdiction: Optional[str] = None) -> List[Citation]:
        tasks = [
            self.courtlistener.search_cases(query, jurisdiction),
            self.harvard.search_cases(query, jurisdiction)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        citations = []
        
        for result in results:
            if isinstance(result, list):
                for case in result:
                    citation = self._parse_case_to_citation(case)
                    if citation:
                        citations.append(citation)
        
        return citations
    
    def _parse_case_to_citation(self, case_data: Dict[str, Any]) -> Optional[Citation]:
        try:
            return Citation(
                case_name=case_data.get("caseName", case_data.get("name", "Unknown")),
                citation=case_data.get("citation", case_data.get("citations", [""])[0]),
                court=case_data.get("court", case_data.get("court_name", "Unknown")),
                date=datetime.fromisoformat(case_data.get("dateFiled", case_data.get("decision_date", "2000-01-01"))),
                jurisdiction=case_data.get("jurisdiction", "Unknown"),
                relevance_score=case_data.get("score", 0.5),
                url=case_data.get("absolute_url", case_data.get("url"))
            )
        except Exception:
            return None

legal_api_manager = LegalAPIManager() 