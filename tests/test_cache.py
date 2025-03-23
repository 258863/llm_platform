import pytest
import time
from llm_platform.utils.cache import Cache

@pytest.fixture
def cache():
    """Create a test cache."""
    return Cache(max_size=1000, ttl=1)  # 1 second TTL

def test_cache_set_get(cache):
    """Test basic cache set and get operations."""
    # Test setting and getting a value
    cache.set('test_key', 'test_value')
    assert cache.get('test_key') == 'test_value'
    
    # Test getting non-existent key
    assert cache.get('nonexistent_key') is None
    
    # Test getting expired key
    time.sleep(1.1)  # Wait for TTL to expire
    assert cache.get('test_key') is None

def test_cache_delete(cache):
    """Test cache deletion."""
    # Set a value
    cache.set('test_key', 'test_value')
    assert cache.get('test_key') == 'test_value'
    
    # Delete the value
    cache.delete('test_key')
    assert cache.get('test_key') is None
    
    # Delete non-existent key
    cache.delete('nonexistent_key')  # Should not raise an error

def test_cache_clear(cache):
    """Test cache clearing."""
    # Set multiple values
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    # Clear cache
    cache.clear()
    
    # Verify all values are gone
    assert cache.get('key1') is None
    assert cache.get('key2') is None
    assert cache.get('key3') is None

def test_cache_size_limit(cache):
    """Test cache size limit."""
    # Fill cache to limit
    for i in range(1000):
        cache.set(f'key{i}', f'value{i}')
    
    # Try to add one more item
    cache.set('overflow_key', 'overflow_value')
    
    # Verify oldest item was removed
    assert cache.get('key0') is None
    assert cache.get('overflow_key') == 'overflow_value'

def test_cache_ttl(cache):
    """Test cache TTL functionality."""
    # Set a value
    cache.set('test_key', 'test_value')
    assert cache.get('test_key') == 'test_value'
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Verify value is expired
    assert cache.get('test_key') is None

def test_cache_update(cache):
    """Test cache update operation."""
    # Set initial value
    cache.set('test_key', 'initial_value')
    assert cache.get('test_key') == 'initial_value'
    
    # Update value
    cache.set('test_key', 'updated_value')
    assert cache.get('test_key') == 'updated_value'

def test_cache_exists(cache):
    """Test cache exists operation."""
    # Set a value
    cache.set('test_key', 'test_value')
    assert cache.exists('test_key') is True
    assert cache.exists('nonexistent_key') is False
    
    # Wait for TTL to expire
    time.sleep(1.1)
    assert cache.exists('test_key') is False

def test_cache_keys(cache):
    """Test cache keys operation."""
    # Set multiple values
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    # Get all keys
    keys = cache.keys()
    assert 'key1' in keys
    assert 'key2' in keys
    assert 'key3' in keys
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Verify expired keys are not returned
    keys = cache.keys()
    assert len(keys) == 0

def test_cache_values(cache):
    """Test cache values operation."""
    # Set multiple values
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    # Get all values
    values = cache.values()
    assert 'value1' in values
    assert 'value2' in values
    assert 'value3' in values
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Verify expired values are not returned
    values = cache.values()
    assert len(values) == 0

def test_cache_items(cache):
    """Test cache items operation."""
    # Set multiple values
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    # Get all items
    items = cache.items()
    assert ('key1', 'value1') in items
    assert ('key2', 'value2') in items
    assert ('key3', 'value3') in items
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Verify expired items are not returned
    items = cache.items()
    assert len(items) == 0

def test_cache_size(cache):
    """Test cache size operation."""
    # Set multiple values
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    # Get cache size
    assert cache.size() == 3
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Verify size is 0 after expiration
    assert cache.size() == 0

def test_cache_ttl_update(cache):
    """Test cache TTL update on access."""
    # Set a value
    cache.set('test_key', 'test_value')
    
    # Wait for half of TTL
    time.sleep(0.5)
    
    # Access the value (should update TTL)
    assert cache.get('test_key') == 'test_value'
    
    # Wait for half of TTL again
    time.sleep(0.5)
    
    # Value should still be valid
    assert cache.get('test_key') == 'test_value'
    
    # Wait for full TTL
    time.sleep(1.1)
    
    # Value should now be expired
    assert cache.get('test_key') is None 