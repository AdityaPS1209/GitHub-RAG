import redis.asyncio as redis
import json
import hashlib
from backend.core.config import settings
from backend.services.embedding_service import embedding_service
from backend.repositories.vector_repo import vector_repository
from backend.services.llm_service import llm_service
from backend.core.database import get_database

class QueryService:
    def __init__(self):
        # Async redis client
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        # Cache expiration in seconds
        self.cache_ttl = 3600

    def _generate_cache_key(self, query: str, repo_id: str = None) -> str:
        key_str = f"{query}:{repo_id}"
        return f"rag_query:{hashlib.md5(key_str.encode()).hexdigest()}"

    async def process_query(self, query: str, user_id: str, repo_id: str = None):
        cache_key = self._generate_cache_key(query, repo_id)
        
        # 1. Check Cache
        try:
            cached_result = await self.redis_client.get(cache_key)
            if cached_result:
                print("Cache hit!")
                return json.loads(cached_result)
        except Exception as e:
            print(f"Redis cache GET error (ignoring): {e}")

        # 2. Get Query Embedding
        query_embedding = embedding_service.generate_embedding(query)
        
        # 3. Search VectorDB
        raw_results = vector_repository.search(query_embedding, k=5)
        
        # 4. Filter by Repo (if specified) and construct context
        context_chunks = []
        sources = []
        for res in raw_results:
            meta = res["metadata"]
            if repo_id and meta.get("repo_id") != repo_id:
                continue # Skip if it doesn't match the requested repo
                
            context_chunks.append(f"File: {meta.get('file_path')}\nContent:\n{meta.get('content')}")
            sources.append({
                "file_path": meta.get("file_path"),
                "content": meta.get("content")[:200] + "...", # truncate for summary
                "distance": res["distance"]
            })

        # 5. Construct Prompt
        context_str = "\n\n---\n\n".join(context_chunks)
        system_prompt = (
            "You are a helpful programming assistant. Use the following context retrieved from "
            "the user's repositories to answer their question. If the answer is not contained "
            "in the context, say 'I don't have enough information from the indexed repositories to answer that'.\n\n"
            f"Context:\n{context_str}"
        )
        
        # 6. Generate Answer
        answer = await llm_service.generate_response(prompt=query, system_prompt=system_prompt)
        
        response_data = {
            "answer": answer,
            "sources": sources
        }
        
        # 7. Store History
        try:
            db = get_database()
            history_doc = {
                "user_id": user_id,
                "query": query,
                "answer": answer,
                "sources": sources,
                "repo_id": repo_id
            }
            # using the Pydantic model wouldn't hurt, but raw dict is fast here
            from backend.models.query import QueryHistoryModel
            history_model = QueryHistoryModel(**history_doc)
            await db.query_history.insert_one(history_model.model_dump(by_alias=True, exclude={"id"}))
        except Exception as e:
            print(f"Failed to save history: {e}")

        # 8. Cache result
        try:
            await self.redis_client.setex(cache_key, self.cache_ttl, json.dumps(response_data))
        except Exception as e:
            print(f"Failed to set cache (ignoring): {e}")
            
        return response_data

query_service = QueryService()
