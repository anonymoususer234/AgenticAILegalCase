import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from config import settings
from models import SubtaskResult

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.llm = ChatOpenAI(
            openai_api_key=settings.openai_api_key,
            model_name="gpt-4",
            temperature=0.1
        )
        self.max_retries = 3
    
    @abstractmethod
    async def execute(self, input_data: Any) -> SubtaskResult:
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def execute_with_retry(self, input_data: Any) -> SubtaskResult:
        start_time = time.time()
        retry_count = 0
        
        try:
            result = await self.execute(input_data)
            processing_time = time.time() - start_time
            
            result.processing_time = processing_time
            result.retry_count = retry_count
            
            if await self.self_evaluate(input_data, result):
                return result
            else:
                raise Exception("Self-evaluation failed")
                
        except Exception as e:
            retry_count += 1
            if retry_count >= self.max_retries:
                return SubtaskResult(
                    task_type=self.name,
                    success=False,
                    data=None,
                    processing_time=time.time() - start_time,
                    retry_count=retry_count
                )
            raise
    
    async def self_evaluate(self, input_data: Any, result: SubtaskResult) -> bool:
        if not result.success:
            return False
        
        evaluation_prompt = f"""
        Evaluate the quality of this {self.name} result:
        
        Input: {input_data}
        Output: {result.data}
        
        Rate the relevance and authority on a scale of 1-10.
        Respond with only 'PASS' or 'FAIL'.
        """
        
        try:
            response = await self.llm.apredict(evaluation_prompt)
            return "PASS" in response.upper()
        except Exception:
            return True
    
    def format_error(self, error: Exception) -> str:
        return f"{self.name} Error: {str(error)}" 