from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate
from datasets import Dataset

from backend.core.config import settings
import os

# Ragas may require specific init to use Groq instead of default OpenAI
try:
    from langchain_community.chat_models import ChatOpenAI
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    ChatOpenAI = None
    HuggingFaceEmbeddings = None

class EvaluationService:
    def __init__(self):
        self.metrics = [faithfulness, answer_relevancy]
        
        # Note: Ragas needs both an LLM and an embedding model.
        # Groq provides LLMs but currently no embeddings, so we use HuggingFace for embeddings by default.
        if ChatOpenAI and settings.GROQ_API_KEY:
            self.groq_llm = ChatOpenAI(
                openai_api_base="https://api.groq.com/openai/v1",
                openai_api_key=settings.GROQ_API_KEY,
                model_name="llama-3.3-70b-versatile"
            )
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Update metrics to use our custom LLM and Embeddings
            for m in self.metrics:
                m.llm = self.groq_llm
                if hasattr(m, 'embeddings'):
                    m.embeddings = self.embeddings
        else:
            self.groq_llm = None

    def evaluate_response(self, question: str, answer: str, contexts: list[str]) -> dict:
        """
        Evaluates a single RAG response.
        Note: Ragas requires an OpenAI API key by default to run these evaluations.
        """
        if not self.groq_llm:
            return {"error": "Groq LLM for evaluation is not configured appropriately. Provide GROQ_API_KEY and langchain."}

        # Convert single interaction to HF Dataset format
        data = {
            "question": [question],
            "contexts": [contexts],
            "answer": [answer]
        }
        dataset = Dataset.from_dict(data)
        
        try:
            result = evaluate(
                dataset,
                metrics=self.metrics,
                # In newer Ragas versions, llm and embeddings can be passed here instead
            )
            return dict(result)
        except Exception as e:
            print(f"Ragas evaluation failed: {e}")
            return {"error": str(e)}

eval_service = EvaluationService()
