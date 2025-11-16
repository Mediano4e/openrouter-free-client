"""Basic usage example for OpenRouter Free Client."""

import asyncio
import os
from openrouter_free import FreeOpenRouterClient, MODELS, AllKeysExhausted
import logging

# Setup logging to see key rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def basic_chat_example():
    """Basic chat completion example."""
    # You can load keys from environment variables for security
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
        os.getenv("OPENROUTER_KEY_3", "your-key-3"),
    ]
    
    # Initialize client with multiple keys
    client = FreeOpenRouterClient(
        model=MODELS["gpt-oss-20b"],
        api_keys=api_keys,
        max_retries=2
    )
    
    try:
        # Simple chat completion
        response = await client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain what Python is in 2 sentences."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        print("Response:", response.choices[0].message.content)
        print(f"Keys status: {client.available_keys_count}/{client.total_keys_count} available")
        
    except AllKeysExhausted:
        print("All API keys have been exhausted. Please try again later.")


async def streaming_example():
    """Example of streaming responses."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
    ]
    
    client = FreeOpenRouterClient(
        model="openai/gpt-3.5-turbo",
        api_keys=api_keys
    )
    
    print("Streaming response:")
    async for chunk in client.stream_chat_completion(
        messages=[
            {"role": "user", "content": "Write a haiku about programming"}
        ],
        temperature=0.9
    ):
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print("\n")


async def key_management_example():
    """Example of dynamic key management."""
    initial_keys = ["key1", "key2"]
    
    client = FreeOpenRouterClient(
        model=MODELS["deepseek-r1t2-chimera"],
        api_keys=initial_keys
    )
    
    print(f"Initial keys: {client.total_keys_count}")
    
    # Add a new key
    client.add_key("key3")
    print(f"After adding: {client.total_keys_count}")
    
    # Remove a key
    client.remove_key("key1")
    print(f"After removing: {client.total_keys_count}")
    
    # Reset all keys (mark as non-exhausted)
    client.reset_keys()
    print(f"Available after reset: {client.available_keys_count}")


async def main():
    """Run all examples."""
    print("=" * 50)
    print("1. Basic Chat Example")
    print("=" * 50)
    await basic_chat_example()
    
    print("\n" + "=" * 50)
    print("2. Streaming Example")
    print("=" * 50)
    # await streaming_example()
    
    print("\n" + "=" * 50)
    print("3. Key Management Example")
    print("=" * 50)
    await key_management_example()


if __name__ == "__main__":
    asyncio.run(main())
