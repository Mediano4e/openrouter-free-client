"""LlamaIndex integration example."""

import os
import asyncio
from openrouter_free import LlamaORFAdapter, MODELS

# Optional: only if llama-index is installed
try:
    from llama_index.core.llms.types import ChatMessage, MessageRole
    from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader
except ImportError:
    print("Please install llama-index-core to run this example:")
    print("pip install openrouter-free[llama-index]")
    exit(1)


def basic_llama_example():
    """Basic LlamaIndex usage."""
    # Initialize adapter with multiple keys
    llm = LlamaORFAdapter(
        model=MODELS["gpt-oss-20b"],
        api_keys=[
            os.getenv("OPENROUTER_KEY_1", "your-key-1"),
            os.getenv("OPENROUTER_KEY_2", "your-key-2"),
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    # Simple chat
    response = llm.chat([
        ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful AI assistant."),
        ChatMessage(role=MessageRole.USER, content="What is LlamaIndex?")
    ])
    
    print("Response:", response.message.content)
    print(f"Available keys: {llm.available_keys}")


def streaming_llama_example():
    """Streaming with LlamaIndex."""
    llm = LlamaORFAdapter(
        model=MODELS["deepseek-chat-v3.1"],
        api_keys=["key1", "key2"],
        temperature=0.8
    )
    
    print("Streaming response:")
    for chunk in llm.stream_chat([
        ChatMessage(role=MessageRole.USER, content="Tell me a short story about a robot")
    ]):
        if chunk.delta:
            print(chunk.delta, end="", flush=True)
    print()


async def async_llama_example():
    """Async operations with LlamaIndex."""
    llm = LlamaORFAdapter(
        model=MODELS["deepseek-r1t2-chimera"],
        api_keys=["key1", "key2", "key3"],
    )
    
    # Async chat
    response = await llm.achat([
        ChatMessage(role=MessageRole.USER, content="What is async programming?")
    ])
    
    print("Async response:", response.message.content)
    
    # Async streaming
    print("\nAsync streaming:")
    async for chunk in llm.astream_chat([
        ChatMessage(role=MessageRole.USER, content="Explain Python in one sentence")
    ]):
        if chunk.delta:
            print(chunk.delta, end="", flush=True)
    print()


def rag_example():
    """RAG (Retrieval-Augmented Generation) example."""
    # Initialize LLM
    llm = LlamaORFAdapter(
        model=MODELS["gpt-oss-20b"],
        api_keys=["key1", "key2"],
        temperature=0.5
    )
    
    # Create some sample documents
    documents = [
        Document(text="Python is a high-level programming language."),
        Document(text="Machine learning is a subset of artificial intelligence."),
        Document(text="LlamaIndex is a framework for building LLM applications."),
    ]
    
    # Create index
    index = VectorStoreIndex.from_documents(
        documents,
        # llm=llm  # Uncomment if you want to use the LLM for indexing
    )
    
    # Create query engine with our LLM
    query_engine = index.as_query_engine(llm=llm)
    
    # Query
    response = query_engine.query("What is Python?")
    print("RAG Response:", response)


def main():
    """Run all examples."""
    print("=" * 50)
    print("1. Basic LlamaIndex Example")
    print("=" * 50)
    basic_llama_example()
    
    print("\n" + "=" * 50)
    print("2. Streaming Example")
    print("=" * 50)
    # streaming_llama_example()
    
    print("\n" + "=" * 50)
    print("3. Async Example")
    print("=" * 50)
    # asyncio.run(async_llama_example())
    
    print("\n" + "=" * 50)
    print("4. RAG Example")
    print("=" * 50)
    # rag_example()


if __name__ == "__main__":
    main()
