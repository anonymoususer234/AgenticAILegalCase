from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from models import SubtaskResult, LegalFinding

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Summarizer")
    
    async def execute(self, input_data: Dict[str, Any]) -> SubtaskResult:
        try:
            findings = input_data.get("findings", [])
            analysis = input_data.get("analysis", {})
            query = input_data.get("query", "")
            
            executive_summary = await self._create_executive_summary(query, findings, analysis)
            
            key_findings = await self._extract_key_findings(findings, analysis)
            
            conclusions = await self._generate_conclusions(findings, analysis)
            
            result_data = {
                "executive_summary": executive_summary,
                "key_findings": key_findings,
                "conclusions": conclusions
            }
            
            return SubtaskResult(
                task_type="summarization",
                success=True,
                data=result_data,
                processing_time=0
            )
            
        except Exception as e:
            return SubtaskResult(
                task_type="summarization",
                success=False,
                data=None,
                processing_time=0
            )
    
    async def _create_executive_summary(self, query: str, findings: List[LegalFinding], analysis: Dict[str, Any]) -> str:
        findings_text = "\n".join([f.content[:300] for f in findings[:5]])
        analysis_text = analysis.get("analysis", "")
        
        summary_prompt = f"""
        Create a concise executive summary for this legal research query: "{query}"
        
        Based on these findings:
        {findings_text}
        
        And this analysis:
        {analysis_text}
        
        The summary should be 2-3 paragraphs and include:
        1. Direct answer to the legal question
        2. Key supporting legal principles
        3. Important caveats or limitations
        
        Write in professional legal language suitable for attorneys.
        """
        
        return await self.llm.apredict(summary_prompt)
    
    async def _extract_key_findings(self, findings: List[LegalFinding], analysis: Dict[str, Any]) -> List[str]:
        findings_text = "\n".join([f.content for f in findings])
        patterns = analysis.get("key_patterns", [])
        
        key_findings_prompt = f"""
        Extract 5-7 key legal findings from this research:
        
        Findings: {findings_text}
        Patterns: {patterns}
        
        Format as bullet points, focusing on actionable legal insights.
        Each finding should be specific and cite-able.
        """
        
        response = await self.llm.apredict(key_findings_prompt)
        return [line.strip("- ").strip() for line in response.split("\n") if line.strip().startswith("-")]
    
    async def _generate_conclusions(self, findings: List[LegalFinding], analysis: Dict[str, Any]) -> List[str]:
        precedent_strength = analysis.get("precedent_strength", 0.0)
        confidence_score = analysis.get("confidence_score", 0.0)
        
        conclusions_prompt = f"""
        Generate practical legal conclusions based on:
        - Precedent strength: {precedent_strength}
        - Confidence score: {confidence_score}
        - Analysis: {analysis.get("analysis", "")}
        
        Provide 3-5 actionable conclusions for legal practitioners.
        Include confidence levels and practical recommendations.
        """
        
        response = await self.llm.apredict(conclusions_prompt)
        return [line.strip("- ").strip() for line in response.split("\n") if line.strip().startswith("-")]

summarizer_agent = SummarizerAgent() 