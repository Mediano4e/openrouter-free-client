import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from openrouter_free import FreeOpenRouterClient, ModelInfo, AllKeysExhausted, InvalidKeyError


class TestFreeOpenRouterClient:
    @pytest.fixture
    def client(self):
        return FreeOpenRouterClient(
            model="openai/gpt-4o-mini",
            api_keys=["key1", "key2", "key3"]
        )
    
    def test_initialization(self):
        # Test with valid keys
        client = FreeOpenRouterClient(
            model="openai/gpt-4o-mini",
            api_keys=["key1", "key2"]
        )
        assert client.total_keys_count == 2
        assert client.available_keys_count == 2
        
        # Test with ModelInfo
        model_info = ModelInfo("test-model", 4096, 1024)
        client = FreeOpenRouterClient(
            model=model_info,
            api_keys=["key1"]
        )
        assert client.model.name == "test-model"
    
    def test_initialization_no_keys(self):
        # Test initialization without keys
        with pytest.raises(ValueError, match="At least one API key must be provided"):
            FreeOpenRouterClient(model="test", api_keys=[])
    
    def test_add_remove_keys(self, client):
        # Test adding key
        initial_count = client.total_keys_count
        client.add_key("new_key")
        assert client.total_keys_count == initial_count + 1
        
        # Test removing key
        assert client.remove_key("new_key") == True
        assert client.total_keys_count == initial_count
        
        # Test removing non-existent key
        assert client.remove_key("non_existent") == False
    
    def test_key_masking(self, client):
        from openrouter_free.client import KeyState
        
        # Test normal key masking
        key_state = KeyState(key="sk-or-v1-1234567890abcdef")
        assert key_state.mask() == "sk-or-...abcdef"
        
        # Test short key masking
        key_state = KeyState(key="short")
        assert key_state.mask() == "***"
    
    def test_reset_keys(self, client):
        # Simulate exhausted keys
        client._exhausted_count = 2
        client._key_states[0].exhausted = True
        client._key_states[1].exhausted = True
        
        # Reset keys
        client.reset_keys()
        assert client._exhausted_count == 0
        assert all(not key.exhausted for key in client._key_states)
    
    @pytest.mark.asyncio
    async def test_all_keys_exhausted(self, client):
        # Mark all keys as exhausted
        client._exhausted_count = client.total_keys_count
        
        # Should raise AllKeysExhausted
        with pytest.raises(AllKeysExhausted):
            await client.chat_completion(messages=[{"role": "user", "content": "test"}])
    
    @pytest.mark.asyncio
    async def test_key_rotation(self):
        with patch('openrouter_free.client.AsyncOpenAI'):
            client = FreeOpenRouterClient(
                model="test-model",
                api_keys=["key1", "key2", "key3"]
            )
            
            # Test rotation logic
            assert client._current_key_index == 0
            result = await client._rotate_key()
            assert result == True
            assert client._current_key_index == 1
            assert client._exhausted_count == 1
