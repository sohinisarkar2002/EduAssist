"""
Gemini API Client Service
"""
import google.generativeai as genai
from typing import List, Optional
import asyncio
from functools import wraps

from ..config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def async_wrap(func):
    """Wrapper to make sync Gemini calls async"""
    @wraps(func)
    async def run(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return run

class GeminiClient:
    """Gemini API client for text generation and embeddings"""

    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.embedding_model = settings.GEMINI_EMBEDDING_MODEL

    async def generate_completion(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate text completion"""
        try:
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"
            else:
                full_prompt = prompt

            response = await self._generate_async(full_prompt, temperature=temperature)
            return response.text

        except Exception as e:
            print(f"Error generating completion: {e}")
            raise

    @async_wrap
    def _generate_async(self, prompt: str, **kwargs):
        """Async wrapper for generation"""
        generation_config = {
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        return self.model.generate_content(prompt, generation_config=generation_config)

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts"""
        try:
            embeddings = []
            for text in texts:
                result = await self._embed_async(text)
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

    @async_wrap
    def _embed_async(self, text: str):
        """Async wrapper for embedding"""
        return genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document"
        )

# Singleton instance
gemini_client = GeminiClient()

async def get_gemini_content(prompt: str, response_format: str = 'text', **kwargs):
    """Unified async interface for Gemini LLM completion (used by other services)"""
    result = await gemini_client.generate_completion(prompt)
    if response_format == "json":
        import json
        return json.loads(result)
    return result
