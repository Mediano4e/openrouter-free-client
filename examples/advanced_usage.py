"""Advanced usage examples for OpenRouter Free Client."""

import asyncio
import os
from openrouter_free import FreeOpenRouterClient, MODELS, AllKeysExhausted, InvalidKeyError
from loguru import logger

# Setup better logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)


async def error_handling_example():
    """Example of proper error handling."""
    # Use invalid keys to demonstrate error handling
    client = FreeOpenRouterClient(
        model=MODELS["gpt-oss-20b"],
        api_keys=["invalid-key-1", "invalid-key-2"]
    )
    
    try:
        response = await client.chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print("Response:", response.choices[0].message.content)
        
    except InvalidKeyError as e:
        print(f"❌ Invalid API keys: {e}")
    except AllKeysExhausted as e:
        print(f"❌ All keys exhausted: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def context_manager_example():
    """Example using context manager for proper cleanup."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
    ]
    
    # Use context manager to ensure proper cleanup
    async with FreeOpenRouterClient(
        model=MODELS["deepseek-chat-v3.1"],
        api_keys=api_keys,
        timeout=10.0
    ) as client:
        
        response = await client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": "Write a simple Python function to calculate factorial."}
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        print("Factorial function:")
        print(response.choices[0].message.content)


async def health_check_example():
    """Example of checking API key health."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
        "invalid-key-for-demo"  # This will fail health check
    ]
    
    client = FreeOpenRouterClient(
        model=MODELS["gpt-oss-20b"],
        api_keys=api_keys
    )
    
    print("🔍 Checking API key health...")
    health_status = await client.health_check()
    
    for key_mask, is_healthy in health_status.items():
        status = "✅ Healthy" if is_healthy else "❌ Unhealthy"
        print(f"Key {key_mask}: {status}")


async def concurrent_requests_example():
    """Example of handling multiple concurrent requests."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
        os.getenv("OPENROUTER_KEY_3", "your-key-3"),
    ]
    
    client = FreeOpenRouterClient(
        model=MODELS["deepseek-r1t2-chimera"],
        api_keys=api_keys,
        max_retries=1
    )
    
    # Prepare multiple requests
    questions = [
        "What is Python?",
        "What is JavaScript?", 
        "What is machine learning?",
        "What is blockchain?",
        "What is quantum computing?"
    ]
    
    print("🚀 Making concurrent requests...")
    
    # Execute requests concurrently
    tasks = []
    for i, question in enumerate(questions):
        task = client.chat_completion(
            messages=[{"role": "user", "content": f"Explain {question} in one sentence."}],
            temperature=0.5,
            max_tokens=50
        )
        tasks.append(task)
    
    # Wait for all to complete
    try:
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"❌ Question {i+1} failed: {response}")
            else:
                print(f"✅ Q{i+1}: {questions[i]}")
                print(f"   A{i+1}: {response.choices[0].message.content.strip()}\n")
                
    except Exception as e:
        print(f"❌ Concurrent requests failed: {e}")
    
    print(f"📊 Final status: {client.available_keys_count}/{client.total_keys_count} keys available")


async def streaming_with_callback_example():
    """Example of streaming with custom callback processing."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
    ]
    
    client = FreeOpenRouterClient(
        model=MODELS["gpt-oss-20b"],
        api_keys=api_keys
    )
    
    print("📝 Streaming story with word counting...")
    
    word_count = 0
    accumulated_text = ""
    
    async for chunk in client.stream_chat_completion(
        messages=[
            {"role": "user", "content": "Write a very short story about a robot learning to paint."}
        ],
        temperature=0.8,
        max_tokens=200
    ):
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            
            # Count words as they come in
            accumulated_text += content
            word_count = len(accumulated_text.split())
    
    print(f"\n\n📊 Total words: {word_count}")


async def dynamic_model_switching_example():
    """Example of switching models dynamically."""
    api_keys = [
        os.getenv("OPENROUTER_KEY_1", "your-key-1"),
        os.getenv("OPENROUTER_KEY_2", "your-key-2"),
    ]
    
    # Start with one model
    client = FreeOpenRouterClient(
        model=MODELS["gpt-oss-20b"],
        api_keys=api_keys
    )
    
    print("🤖 Using GPT OSS 20B model:")
    response1 = await client.chat_completion(
        messages=[{"role": "user", "content": "What's your model name?"}],
        max_tokens=50
    )
    print(response1.choices[0].message.content)
    
    # Switch to different model by creating new client
    print(f"\n🔄 Switching to DeepSeek model...")
    client2 = FreeOpenRouterClient(
        model=MODELS["deepseek-chat-v3.1"],
        api_keys=api_keys
    )
    
    response2 = await client2.chat_completion(
        messages=[{"role": "user", "content": "What's your model name?"}],
        max_tokens=50
    )
    print(response2.choices[0].message.content)
    
    # Clean up
    await client.close()
    await client2.close()


async def main():
    """Run all advanced examples."""
    examples = [
        ("Error Handling", error_handling_example),
        ("Context Manager", context_manager_example),
        ("Health Check", health_check_example),
        ("Concurrent Requests", concurrent_requests_example),
        ("Streaming with Callback", streaming_with_callback_example),
        ("Dynamic Model Switching", dynamic_model_switching_example),
    ]
    
    for name, func in examples:
        print("=" * 60)
        print(f"🔥 {name} Example")
        print("=" * 60)
        
        try:
            await func()
        except Exception as e:
            print(f"❌ Example failed: {e}")
        
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
