# tests/conftest.py
"""Shared test configuration and fixtures."""

import os
import pytest
from typing import Dict, Any


@pytest.fixture
def clean_environment():
    """Clean up environment variables after each test."""
    # Store original environment
    original_env = dict(os.environ)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture  
def sample_env_content():
    """Sample environment file content for tests."""
    return """
# Sample environment variables
DATABASE_URL=sqlite:///test.db
API_KEY=test_api_key_12345
DEBUG=True
SECRET_KEY=super_secret_key
REDIS_URL=redis://localhost:6379/0

# Multiline values
MULTILINE_VAR="Line 1
Line 2  
Line 3"

# Numbers and booleans
MAX_CONNECTIONS=100
TIMEOUT=30.5
ENABLE_CACHE=false
"""


@pytest.fixture
def mock_pytest_config():
    """Create a mock pytest config for testing."""
    class MockOption:
        def __init__(self):
            self.verbose = 0
    
    class MockConfig:
        def __init__(self):
            self.option = MockOption()
            self._ini_values = {}
            self._cli_options = {}
        
        def getoption(self, name, default=None):
            return self._cli_options.get(name, default)
        
        def getini(self, name):
            return self._ini_values.get(name, [] if name == "env_files" else False)
        
        def set_cli_option(self, name, value):
            self._cli_options[name] = value
        
        def set_ini_value(self, name, value):
            self._ini_values[name] = value
    
    return MockConfig()