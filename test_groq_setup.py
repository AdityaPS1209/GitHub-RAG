import asyncio
import os
import sys

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.config import settings

def test_settings():
    print("Testing settings...")
    print(f"GROQ_API_KEY is set: {bool(settings.GROQ_API_KEY)}")

async def test_llm_setup():
    print("\nTesting LLM service setup...")
    from backend.services.llm_service import llm_service
    print(f"Using Groq: {llm_service.use_groq}")
    if llm_service.use_groq:
        print(f"Base URL: {llm_service.client.base_url}")
    print("Setup tests complete.")

async def main():
    test_settings()
    await test_llm_setup()

if __name__ == "__main__":
    asyncio.run(main())
