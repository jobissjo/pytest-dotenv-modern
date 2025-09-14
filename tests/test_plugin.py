"""Tests for the pytest-dotenv plugin."""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

from pytest_dotenv_modern.plugin import DotenvPlugin, find_dotenv_file, get_dotenv_plugin


class TestFindDotenvFile:
    """Test the find_dotenv_file function."""
    
    def test_find_existing_file_in_current_dir(self, tmp_path):
        """Test finding a file in the current directory."""
        # Change to tmp_path
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            # Create a .env file
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_VAR=test_value")
            
            # Should find the file
            found_path = find_dotenv_file(".env")
            assert found_path is not None
            assert found_path.name == ".env"
            assert found_path.exists()
        finally:
            os.chdir(original_cwd)
    
    def test_find_file_in_parent_directory(self, tmp_path):
        """Test finding a file in a parent directory."""
        # Create directory structure
        parent_dir = tmp_path / "parent"
        child_dir = parent_dir / "child"
        child_dir.mkdir(parents=True)
        
        # Create .env file in parent
        env_file = parent_dir / ".env"
        env_file.write_text("PARENT_VAR=parent_value")
        
        # Change to child directory
        original_cwd = os.getcwd()
        os.chdir(child_dir)
        
        try:
            found_path = find_dotenv_file(".env")
            assert found_path is not None
            assert found_path.name == ".env"
            assert found_path.parent == parent_dir
        finally:
            os.chdir(original_cwd)
    
    def test_file_not_found(self, tmp_path):
        """Test behavior when file doesn't exist."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            found_path = find_dotenv_file("nonexistent.env")
            assert found_path is None
        finally:
            os.chdir(original_cwd)
    
    def test_absolute_path(self, tmp_path):
        """Test with absolute path."""
        env_file = tmp_path / "absolute.env"
        env_file.write_text("ABS_VAR=abs_value")
        
        found_path = find_dotenv_file(str(env_file))
        assert found_path == env_file


class TestDotenvPlugin:
    """Test the DotenvPlugin class."""
    
    def test_plugin_initialization(self):
        """Test plugin initialization."""
        # Create a mock config
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
        
        config = MockConfig()
        plugin = DotenvPlugin(config)
        
        assert plugin.config == config
        assert plugin.loaded_files == []
    
    def test_load_file_success(self, tmp_path):
        """Test successful file loading."""
        # Create mock config
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
        
        config = MockConfig()
        plugin = DotenvPlugin(config)
        
        # Create test env file
        env_file = tmp_path / "test.env"
        env_file.write_text("PLUGIN_TEST_VAR=plugin_value")
        
        # Load the file
        success = plugin.load_file(str(env_file))
        
        assert success
        assert len(plugin.loaded_files) == 1
        assert plugin.loaded_files[0] == env_file
        assert os.getenv("PLUGIN_TEST_VAR") == "plugin_value"
        
        # Clean up
        if "PLUGIN_TEST_VAR" in os.environ:
            del os.environ["PLUGIN_TEST_VAR"]
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file."""
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
        
        config = MockConfig()
        plugin = DotenvPlugin(config)
        
        success = plugin.load_file("nonexistent.env")
        
        assert not success
        assert len(plugin.loaded_files) == 0


class TestEnvironmentVariableLoading:
    """Test actual environment variable loading."""
    
    def test_basic_env_loading(self, tmp_path, monkeypatch):
        """Test basic environment variable loading."""
        # Create .env file
        env_file = tmp_path / ".env"
        env_file.write_text("BASIC_TEST_VAR=basic_value\nANOTHER_VAR=another_value")
        
        # Change to tmp_path to ensure the file is found
        original_cwd = os.getcwd()
        monkeypatch.chdir(tmp_path)
        
        # Create mock config that will load the .env file
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
            
            def getoption(self, name, default=None):
                if name == "envfile":
                    return []
                if name == "override_existing":
                    return False
                return default
            
            def getini(self, name):
                if name == "env_files":
                    return []
                if name == "env_override_existing_values":
                    return False
                return None
        
        config = MockConfig()
        
        # Import and call the configure function
        from pytest_dotenv_modern.plugin import pytest_configure
        pytest_configure(config)
        
        # Check if variables were loaded
        assert os.getenv("BASIC_TEST_VAR") == "basic_value"
        assert os.getenv("ANOTHER_VAR") == "another_value"
        
        # Clean up
        for var in ["BASIC_TEST_VAR", "ANOTHER_VAR"]:
            if var in os.environ:
                del os.environ[var]
    
    def test_override_existing_variables(self, tmp_path, monkeypatch):
        """Test overriding existing environment variables."""
        # Set an existing environment variable
        os.environ["OVERRIDE_TEST_VAR"] = "original_value"
        
        # Create .env file with the same variable
        env_file = tmp_path / ".env"
        env_file.write_text("OVERRIDE_TEST_VAR=overridden_value")
        
        monkeypatch.chdir(tmp_path)
        
        # Create mock config with override enabled
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
            
            def getoption(self, name, default=None):
                if name == "envfile":
                    return []
                if name == "override_existing":
                    return True
                return default
            
            def getini(self, name):
                if name == "env_files":
                    return []
                if name == "env_override_existing_values":
                    return True
                return None
        
        config = MockConfig()
        
        from pytest_dotenv_modern.plugin import pytest_configure
        pytest_configure(config)
        
        # Variable should be overridden
        assert os.getenv("OVERRIDE_TEST_VAR") == "overridden_value"
        
        # Clean up
        if "OVERRIDE_TEST_VAR" in os.environ:
            del os.environ["OVERRIDE_TEST_VAR"]
    
    def test_no_override_existing_variables(self, tmp_path, monkeypatch):
        """Test not overriding existing environment variables."""
        # Set an existing environment variable
        os.environ["NO_OVERRIDE_TEST_VAR"] = "original_value"
        
        # Create .env file with the same variable
        env_file = tmp_path / ".env"
        env_file.write_text("NO_OVERRIDE_TEST_VAR=should_not_override")
        
        monkeypatch.chdir(tmp_path)
        
        # Create mock config with override disabled
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
            
            def getoption(self, name, default=None):
                if name == "envfile":
                    return []
                if name == "override_existing":
                    return False
                return default
            
            def getini(self, name):
                if name == "env_files":
                    return []
                if name == "env_override_existing_values":
                    return False
                return None
        
        config = MockConfig()
        
        from pytest_dotenv_modern.plugin import pytest_configure
        pytest_configure(config)
        
        # Variable should not be overridden
        assert os.getenv("NO_OVERRIDE_TEST_VAR") == "original_value"
        
        # Clean up
        if "NO_OVERRIDE_TEST_VAR" in os.environ:
            del os.environ["NO_OVERRIDE_TEST_VAR"]


class TestConfigurationOptions:
    """Test configuration from pytest.ini and command line."""
    
    def test_multiple_env_files_from_config(self, tmp_path, monkeypatch):
        """Test loading multiple env files from configuration."""
        # Create multiple .env files
        env1 = tmp_path / ".env.test"
        env1.write_text("CONFIG_VAR1=value1")
        
        env2 = tmp_path / ".env.local"
        env2.write_text("CONFIG_VAR2=value2")
        
        monkeypatch.chdir(tmp_path)
        
        # Mock config with multiple files
        class MockConfig:
            def __init__(self):
                self.option = type('obj', (object,), {'verbose': 0})
            
            def getoption(self, name, default=None):
                if name == "envfile":
                    return []
                if name == "override_existing":
                    return False
                return default
            
            def getini(self, name):
                if name == "env_files":
                    return [".env.test", ".env.local"]
                if name == "env_override_existing_values":
                    return False
                return None
        
        config = MockConfig()
        
        from pytest_dotenv_modern.plugin import pytest_configure
        pytest_configure(config)
        
        # Check if both files were loaded
        assert os.getenv("CONFIG_VAR1") == "value1"
        assert os.getenv("CONFIG_VAR2") == "value2"
        
        # Clean up
        for var in ["CONFIG_VAR1", "CONFIG_VAR2"]:
            if var in os.environ:
                del os.environ[var]


@pytest.fixture
def clean_env():
    """Fixture to clean up environment variables after tests."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)