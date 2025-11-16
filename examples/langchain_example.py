"""LangChain integration example."""

import os
import asyncio
from openrouter_free import LangChainORFAdapter, MODELS

# Optional: only if langchain is installed
try:
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain.chains import LLMChain
    from langchain.memory import ConversationBufferMemory
except ImportError:
    print("Please install langchain-core to run this example:")
    print("pip install openrouter-free[langchain]")
    exit(1)


def basic_langchain_example():
    """Basic LangChain usage."""
    # Initialize adapter
    chat = LangChainORFAdapter(
        model=MODELS["gpt-oss-20b"],
        api_keys=[
            os.getenv("OPENROUTER_KEY_1", "your-key-1"),
            os.getenv("OPENROUTER_KEY_2", "your-key-2"),
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    # Simple chat
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is LangChain?")
    ]
    
    response = chat.invoke(messages)
    print("Response:", response.content)
    print(f"Available keys: {chat.available_keys}")


def streaming_langchain_example():
    """Streaming with LangChain."""
    chat = LangChainORFAdapter(
        model=MODELS["deepseek-chat-v3.1"],
        api_keys=["key1", "key2"],
        temperature=0.8
    )
    
    messages = [HumanMessage(content="Write a poem about coding")]
    
    print("Streaming response:")
    for chunk in chat.stream(messages):
        print(chunk.content, end="", flush=True)
    print()


async def async_langchain_example():
    """Async operations with LangChain."""
    chat = LangChainORFAdapter(
        model=MODELS["deepseek-r1t2-chimera"],
        api_keys=["key1", "key2", "key3"],
    )
    
    messages = [HumanMessage(content="What is asynchronous programming?")]
    
    # Async invoke
    response = await chat.ainvoke(messages)
    print("Async response:", response.content)
    
    # Async streaming
    print("\nAsync streaming:")
    async for chunk in chat.astream(messages):
        print(chunk.content, end="", flush=True)
    print()


def chain_example():
    """Example using LangChain chains."""
    # Initialize chat model
    chat = LangChainORFAdapter(
        model=MODELS["gpt-4o-mini"],
        api_keys=["key1", "key2"],
        temperature=0.5
    )
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are a helpful assistant that translates text."),
        HumanMessage(content="Translate the following {language} text to English: {text}")
    ])
    
    # Create chain
    chain = prompt | chat | StrOutputParser()
    
    # Run chain
    result = chain.invoke({
        "language": "French",
        "text": "Bonjour, comment allez-vous?"
    })
    
    print("Translation:", result)


def conversation_example():
    """Example with conversation memory."""
    # Initialize chat model
    chat = LangChainORFAdapter(
        model="openai/gpt-3.5-turbo",
        api_keys=["key1", "key2"],
        temperature=0.7
    )
    
    # Create conversation prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{input}")
    ])
    
    # Create chain with memory
    chain = prompt | chat | StrOutputParser()
    
    # Simulate conversation
    history = []
    
    # First message
    response1 = chain.invoke({
        "history": history,
        "input": "Hi! My name is Alice."
    })
    print("AI:", response1)
    history.extend([
        HumanMessage(content="Hi! My name is Alice."),
        AIMessage(content=response1)
    ])
    
    # Second message (AI should remember the name)
    response2 = chain.invoke({
        "history": history,
        "input": "What's my name?"
    })
    print("AI:", response2)


def batch_processing_example():
    """Example of batch processing."""
    chat = LangChainORFAdapter(
        model=MODELS["gpt-4o-mini"],
        api_keys=["key1", "key2", "key3"],
        temperature=0.5
    )
    
    # Multiple inputs
    inputs = [
        [HumanMessage(content="What is 2+2?")],
        [HumanMessage(content="What is the capital of France?")],
        [HumanMessage(content="What color is the sky?")]
    ]
    
    # Batch invoke
    responses = chat.batch(inputs)
    
    for i, response in enumerate(responses):
        print(f"Q{i+1}: {inputs[i][0].content}")
        print(f"A{i+1}: {response.content}\n")


def main():
    """Run all examples."""
    print("=" * 50)
    print("1. Basic LangChain Example")
    print("=" * 50)
    basic_langchain_example()
    
    print("\n" + "=" * 50)
    print("2. Streaming Example")
    print("=" * 50)
    # streaming_langchain_example()
    
    print("\n" + "=" * 50)
    print("3. Async Example")
    print("=" * 50)
    # asyncio.run(async_langchain_example())
    
    print("\n" + "=" * 50)
    print("4. Chain Example")
    print("=" * 50)
    # chain_example()
    
    print("\n" + "=" * 50)
    print("5. Conversation Example")
    print("=" * 50)
    # conversation_example()
    
    print("\n" + "=" * 50)
    print("6. Batch Processing Example")
    print("=" * 50)
    # batch_processing_example()


if __name__ == "__main__":
    main()
