from typing import List, Dict, Any
from datetime import datetime
from agents.base_agent import BaseAgent
from models import SubtaskResult, LegalBrief, LegalFinding, Citation

class ComposerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Composer")
    
    async def execute(self, input_data: Dict[str, Any]) -> SubtaskResult:
        try:
            query = input_data.get("query", "")
            findings = input_data.get("findings", [])
            analysis = input_data.get("analysis", {})
            summary = input_data.get("summary", {})
            
            supporting_cases = self._extract_supporting_cases(findings)
            
            legal_analysis = await self._compose_legal_analysis(
                query, findings, analysis
            )
            
            jurisdiction_analysis = analysis.get("jurisdictional_analysis", {})
            
            brief = LegalBrief(
                query=query,
                executive_summary=summary.get("executive_summary", ""),
                key_findings=summary.get("key_findings", []),
                supporting_cases=supporting_cases,
                legal_analysis=legal_analysis,
                conclusions=summary.get("conclusions", []),
                jurisdiction_analysis=jurisdiction_analysis,
                generated_at=datetime.now()
            )
            
            formatted_brief = await self._format_brief(brief)
            
            return SubtaskResult(
                task_type="composition",
                success=True,
                data={
                    "brief": brief,
                    "formatted_brief": formatted_brief
                },
                processing_time=0
            )
            
        except Exception as e:
            return SubtaskResult(
                task_type="composition",
                success=False,
                data=None,
                processing_time=0
            )
    
    def _extract_supporting_cases(self, findings: List[LegalFinding]) -> List[Citation]:
        citations = []
        
        for finding in findings:
            citations.extend(finding.citations)
        
        citations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return citations[:10]
    
    async def _compose_legal_analysis(self, query: str, findings: List[LegalFinding], analysis: Dict[str, Any]) -> str:
        findings_text = "\n".join([f.content for f in findings])
        analysis_text = analysis.get("analysis", "")
        patterns = analysis.get("key_patterns", [])
        
        composition_prompt = f"""
        Compose a comprehensive legal analysis for the query: "{query}"
        
        Structure the analysis with:
        1. Legal Framework and Applicable Law
        2. Case Law Analysis
        3. Jurisdictional Considerations
        4. Practical Implications
        5. Risk Assessment
        
        Base the analysis on:
        Findings: {findings_text}
        Analysis: {analysis_text}
        Key Patterns: {patterns}
        
        Write in formal legal brief style with proper legal reasoning.
        Include specific case references where applicable.
        """
        
        return await self.llm.apredict(composition_prompt)
    
    async def _format_brief(self, brief: LegalBrief) -> str:
        formatted_prompt = f"""
        Format this legal brief into a professional document structure:
        
        Query: {brief.query}
        Executive Summary: {brief.executive_summary}
        Key Findings: {brief.key_findings}
        Legal Analysis: {brief.legal_analysis}
        Conclusions: {brief.conclusions}
        Supporting Cases: {[c.case_name for c in brief.supporting_cases]}
        
        Create a well-structured legal brief with:
        - Proper headings and sections
        - Citation formatting
        - Professional legal language
        - Clear organization
        
        Return the formatted brief as a string.
        """
        
        return await self.llm.apredict(formatted_prompt)

composer_agent = ComposerAgent() 