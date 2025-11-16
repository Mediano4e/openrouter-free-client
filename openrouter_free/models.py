"""Model information classes for OpenRouter."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelInfo:
    """Information about an AI model."""
    
    name: str
    context_length: int
    max_output_tokens: Optional[int] = None
    
    @property
    def openrouter_name(self) -> str:
        """Get the OpenRouter-compatible model name."""
        return self.name if "/" in self.name else f"openai/{self.name}"


# Predefined common models
MODELS = {
    "gpt-4o-mini": ModelInfo(
        name="openai/gpt-4o-mini",
        context_length=128000,
        max_output_tokens=16384
    ),
    "gpt-4o-mini-2024-07-18": ModelInfo(
        name="openai/gpt-4o-mini-2024-07-18",
        context_length=128000,
        max_output_tokens=16384
    ),
    "gpt-3.5-turbo": ModelInfo(
        name="openai/gpt-3.5-turbo",
        context_length=16385,
        max_output_tokens=4096
    ),
    "claude-3-haiku": ModelInfo(
        name="anthropic/claude-3-haiku",
        context_length=200000,
        max_output_tokens=4096
    ),
    "llama-3.2-3b-instruct": ModelInfo(
        name="meta-llama/llama-3.2-3b-instruct",
        context_length=131072,
        max_output_tokens=131072
    ),
    "phi-3.5-mini-128k-instruct": ModelInfo(
        name="microsoft/phi-3.5-mini-128k-instruct",
        context_length=128000,
        max_output_tokens=4096
    ),
    "gemini-2.0-flash-exp": ModelInfo(
        name="google/gemini-2.0-flash-exp:free",
        context_length=1048576,
        max_output_tokens=8192
    ),
}
