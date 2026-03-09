import os
import shutil
from git import Repo
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.services.embedding_service import embedding_service
from backend.repositories.vector_repo import vector_repository
from backend.core.database import get_database
from bson import ObjectId

class IngestionService:
    def __init__(self):
        self.temp_dir = "./temp_repos"
        # 500 tokens is roughly 2000 characters. Overlap is good for context.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
        )

    async def ingest_repository(self, repo_id: str, clone_url: str):
        repo_path = os.path.join(self.temp_dir, repo_id)
        db = get_database()
        
        try:
            # Update status
            await db.repositories.update_one(
                {"_id": ObjectId(repo_id)}, 
                {"$set": {"status": "processing"}}
            )
            
            # Clone repo
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            Repo.clone_from(clone_url, repo_path)
            
            # Process files
            chunks_to_embed = []
            metadata_list = []
            
            # Supported extensions
            valid_extensions = {".md", ".py", ".js", ".ts", ".txt", ".json", ".html"}
            
            for root, _, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in root:
                    continue
                    
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext not in valid_extensions:
                        continue
                        
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # Split text
                        texts = self.text_splitter.split_text(content)
                        
                        for i, text in enumerate(texts):
                            chunks_to_embed.append(text)
                            metadata_list.append({
                                "repo_id": repo_id,
                                "file_path": rel_path,
                                "chunk_index": i,
                                "content": text
                            })
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
            
            if chunks_to_embed:
                # Generate embeddings
                embeddings = embedding_service.generate_embeddings_batch(chunks_to_embed)
                
                # Store in vector DB
                vector_ids = vector_repository.add_embeddings(embeddings, metadata_list)
                
                # Store document metadata in MongoDB
                documents = []
                for meta, v_id in zip(metadata_list, vector_ids):
                    doc = meta.copy()
                    doc["vector_id"] = v_id
                    documents.append(doc)
                    
                await db.documents.insert_many(documents)
            
            # Update status
            await db.repositories.update_one(
                {"_id": ObjectId(repo_id)}, 
                {"$set": {"status": "completed"}}
            )
            
        except Exception as e:
            print(f"Error ingesting repo: {e}")
            await db.repositories.update_one(
                {"_id": ObjectId(repo_id)}, 
                {"$set": {"status": "failed", "error": str(e)}}
            )
        finally:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)

ingestion_service = IngestionService()
