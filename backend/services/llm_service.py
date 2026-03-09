import openai
from backend.core.config import settings

class LLMService:
    def __init__(self):
        # Allow default to Ollama if no API key is provided, or use Groq if available
        self.use_groq = bool(settings.GROQ_API_KEY)
        if self.use_groq:
            self.client = openai.AsyncOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=settings.GROQ_API_KEY
            )
        else:
            # Point to local Ollama instance (default port 11434)
            # You must have Ollama running with e.g. `ollama run mistral`
            self.client = openai.AsyncOpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama" 
            )
            self.local_model = "mistral" # Default local model

    async def generate_response(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        try:
            model_name = "llama-3.3-70b-versatile" if self.use_groq else self.local_model
            
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3, # Lower temperature for more factual RAG responses
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Sorry, I encountered an error while trying to generate the response."

llm_service = LLMService()
