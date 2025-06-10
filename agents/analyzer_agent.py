from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from models import SubtaskResult, LegalFinding

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Analyzer")
    
    async def execute(self, input_data: List[LegalFinding]) -> SubtaskResult:
        try:
            analysis = await self._analyze_findings(input_data)
            
            key_patterns = await self._identify_patterns(input_data)
            
            jurisdictional_analysis = await self._analyze_jurisdictions(input_data)
            
            precedent_strength = await self._evaluate_precedent_strength(input_data)
            
            result_data = {
                "analysis": analysis,
                "key_patterns": key_patterns,
                "jurisdictional_analysis": jurisdictional_analysis,
                "precedent_strength": precedent_strength,
                "confidence_score": self._calculate_confidence_score(input_data)
            }
            
            return SubtaskResult(
                task_type="analysis",
                success=True,
                data=result_data,
                processing_time=0
            )
            
        except Exception as e:
            return SubtaskResult(
                task_type="analysis",
                success=False,
                data=None,
                processing_time=0
            )
    
    async def _analyze_findings(self, findings: List[LegalFinding]) -> str:
        content = "\n".join([f.content for f in findings])
        
        analysis_prompt = f"""
        Analyze these legal findings for common themes and legal principles:
        
        {content}
        
        Provide a comprehensive legal analysis focusing on:
        1. Common legal principles
        2. Conflicting viewpoints
        3. Emerging trends
        4. Jurisdictional differences
        
        Keep the analysis concise but thorough.
        """
        
        return await self.llm.apredict(analysis_prompt)
    
    async def _identify_patterns(self, findings: List[LegalFinding]) -> List[str]:
        content = "\n".join([f.content for f in findings])
        
        pattern_prompt = f"""
        Identify key legal patterns and recurring themes in these findings:
        
        {content}
        
        Return a list of 3-5 key patterns as bullet points.
        """
        
        response = await self.llm.apredict(pattern_prompt)
        return [line.strip("- ").strip() for line in response.split("\n") if line.strip().startswith("-")]
    
    async def _analyze_jurisdictions(self, findings: List[LegalFinding]) -> Dict[str, str]:
        jurisdictions = {}
        
        for finding in findings:
            for citation in finding.citations:
                if citation.jurisdiction not in jurisdictions:
                    jurisdictions[citation.jurisdiction] = []
                jurisdictions[citation.jurisdiction].append(citation.case_name)
        
        analysis = {}
        for jurisdiction, cases in jurisdictions.items():
            jurisdiction_prompt = f"""
            Analyze the legal position in {jurisdiction} based on these cases:
            {cases}
            
            Provide a brief summary of the jurisdiction's stance.
            """
            
            analysis[jurisdiction] = await self.llm.apredict(jurisdiction_prompt)
        
        return analysis
    
    async def _evaluate_precedent_strength(self, findings: List[LegalFinding]) -> float:
        authority_scores = [f.authority_score for f in findings]
        relevance_scores = [f.relevance_score for f in findings]
        
        if not authority_scores:
            return 0.0
        
        weighted_score = sum(a * r for a, r in zip(authority_scores, relevance_scores))
        total_weight = sum(relevance_scores)
        
        return weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _calculate_confidence_score(self, findings: List[LegalFinding]) -> float:
        if not findings:
            return 0.0
        
        avg_relevance = sum(f.relevance_score for f in findings) / len(findings)
        avg_authority = sum(f.authority_score for f in findings) / len(findings)
        
        return (avg_relevance + avg_authority) / 2

analyzer_agent = AnalyzerAgent() 