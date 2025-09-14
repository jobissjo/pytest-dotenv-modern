"""A pytest plugin for loading environment variables from dotenv files."""

import os
from pathlib import Path
from typing import List, Optional, Union

import pytest
from dotenv import load_dotenv


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command-line options for the dotenv plugin."""
    group = parser.getgroup("dotenv")
    group.addoption(
        "--envfile",
        action="append",
        dest="envfile",
        help="Load environment variables from specified .env file(s). Can be used multiple times.",
    )
    group.addoption(
        "--override-existing-vars",
        action="store_true",
        dest="override_existing",
        help="Override existing environment variables with values from .env files.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure the dotenv plugin based on pytest configuration."""
    # Get command line options
    envfiles_from_cli = config.getoption("envfile", default=[])
    override_from_cli = config.getoption("override_existing", default=False)
    
    # Get configuration from pytest.ini/tox.ini/setup.cfg
    envfiles_from_config = config.getini("env_files")
    override_from_config = config.getini("env_override_existing_values")
    
    # Normalize config values
    if isinstance(envfiles_from_config, str):
        envfiles_from_config = [envfiles_from_config]
    
    # Convert override setting to boolean
    if isinstance(override_from_config, str):
        override_from_config = override_from_config.lower() in ("1", "true", "yes", "on")
    
    # Combine CLI and config file options
    all_envfiles = list(envfiles_from_cli) + list(envfiles_from_config)
    should_override = override_from_cli or bool(override_from_config)
    
    # If no specific files are provided, try to load default .env file
    if not all_envfiles:
        default_env_path = find_dotenv_file(".env")
        if default_env_path:
            all_envfiles = [str(default_env_path)]
    
    # Load environment files
    for envfile in all_envfiles:
        envfile_path = find_dotenv_file(envfile)
        if envfile_path and envfile_path.exists():
            load_dotenv(
                dotenv_path=envfile_path,
                override=should_override,
                verbose=config.option.verbose > 0
            )
        elif config.option.verbose > 0:
            print(f"Warning: Environment file {envfile} not found")


def find_dotenv_file(filename: Union[str, Path]) -> Optional[Path]:
    """
    Find a dotenv file by searching in the current directory and parent directories.
    
    Args:
        filename: The name of the dotenv file to search for
        
    Returns:
        Path to the dotenv file if found, None otherwise
    """
    if isinstance(filename, str):
        filename = Path(filename)
    
    # If it's an absolute path, return as-is
    if filename.is_absolute():
        return filename if filename.exists() else None
    
    # Search from current directory upwards
    current_dir = Path.cwd()
    
    # First try the exact filename
    for parent in [current_dir] + list(current_dir.parents):
        candidate = parent / filename
        if candidate.exists():
            return candidate
    
    return None


def pytest_sessionstart(session: pytest.Session) -> None:
    """Called after the Session object has been created."""
    # This hook can be used for additional session-level initialization if needed
    pass





# Register configuration options
def pytest_addoption(parser: pytest.Parser) -> None:
    """Add configuration options that can be used in pytest.ini."""
    parser.addini(
        "env_files",
        type="linelist",
        help="List of dotenv files to load (one per line)",
        default=[]
    )
    parser.addini(
        "env_override_existing_values",
        type="bool",
        help="Override existing environment variables with values from dotenv files",
        default=False
    )


class DotenvPlugin:
    """Main plugin class for pytest-dotenv functionality."""
    
    def __init__(self, config: pytest.Config):
        self.config = config
        self._loaded_files: List[Path] = []
    
    @property
    def loaded_files(self) -> List[Path]:
        """Return list of successfully loaded dotenv files."""
        return self._loaded_files.copy()
    
    def load_file(self, filepath: Union[str, Path], override: bool = False) -> bool:
        """
        Load a specific dotenv file.
        
        Args:
            filepath: Path to the dotenv file
            override: Whether to override existing environment variables
            
        Returns:
            True if file was loaded successfully, False otherwise
        """
        dotenv_path = find_dotenv_file(filepath)
        if dotenv_path and dotenv_path.exists():
            success = load_dotenv(
                dotenv_path=dotenv_path,
                override=override,
                verbose=self.config.option.verbose > 0
            )
            if success:
                self._loaded_files.append(dotenv_path)
            return success
        return False


# Store plugin instance for potential access from tests
_dotenv_plugin_instance: Optional[DotenvPlugin] = None


def get_dotenv_plugin() -> Optional[DotenvPlugin]:
    """Get the current dotenv plugin instance."""
    return _dotenv_plugin_instance


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Configure the plugin (implementation with tryfirst=True for early execution)."""
    global _dotenv_plugin_instance
    _dotenv_plugin_instance = DotenvPlugin(config)
    
    # Get command line options
    envfiles_from_cli = config.getoption("envfile", default=[]) or []
    override_from_cli = config.getoption("override_existing", default=False)
    
    # Get configuration from pytest.ini/tox.ini/setup.cfg
    envfiles_from_config = config.getini("env_files") or []
    override_from_config = config.getini("env_override_existing_values")
    
    # Combine CLI and config file options
    all_envfiles = list(envfiles_from_cli) + list(envfiles_from_config)
    should_override = override_from_cli or bool(override_from_config)
    
    # If no specific files are provided, try to load default .env file
    if not all_envfiles:
        default_env_path = find_dotenv_file(".env")
        if default_env_path:
            all_envfiles = [str(default_env_path)]
    
    # Load environment files
    for envfile in all_envfiles:
        _dotenv_plugin_instance.load_file(envfile, override=should_override)