from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openrouter-free",
    version="0.1.0",
    author="Mediano4e",
    author_email="mediano4e@gmail.com",
    description="A Python client for managing multiple free OpenRouter API keys with automatic rotation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mediano4e/openrouter-free-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "httpx>=0.24.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "llama-index": ["llama-index-core>=0.10.0"],
        "langchain": ["langchain-core>=0.1.0"],
        "all": [
            "llama-index-core>=0.10.0",
            "langchain-core>=0.1.0",
        ],
    },
)
