# pytest-dotenv-modern

A modern pytest plugin that loads environment variables from dotenv files before running tests.

This project is a maintained replacement for the original `pytest-dotenv` plugin, built with modern Python practices and full support for contemporary pytest versions.

## Features

- 🚀 **Modern**: Built with Python 3.8+ and latest pytest versions
- 🔧 **Flexible**: Load from multiple dotenv files
- ⚙️ **Configurable**: Configure via pytest.ini, tox.ini, or command line
- 🔄 **Override Control**: Choose whether to override existing environment variables
- 🔍 **Smart Discovery**: Automatically finds .env files in current and parent directories
- 📝 **Well Tested**: Comprehensive test suite
- 🏗️ **Type Hinted**: Full type hints for better IDE support

## Installation

Install using uv (recommended):

```bash
uv add pytest-dotenv-modern
```

Or using pip:

```bash
pip install pytest-dotenv-modern
```

## Quick Start

1. Create a `.env` file in your project root:
```bash
# .env
DATABASE_URL=sqlite:///test.db
API_KEY=your-test-api-key
DEBUG=True
```

2. Run your tests:
```bash
pytest
```

The plugin will automatically discover and load your `.env` file!

## Configuration

### Automatic Discovery

By default, the plugin will look for a `.env` file in the current directory and parent directories. If found, it will be loaded automatically.

### Configuration File

Add configuration to your `pytest.ini`, `tox.ini`, or `setup.cfg`:

```ini
[pytest]
env_files = 
    .env
    .env.test
    .env.local

env_override_existing_values = 1
```

### Command Line

Use command line options for one-off overrides:

```bash
# Load specific env file
pytest --envfile .env.production

# Load multiple files
pytest --envfile .env --envfile .env.test

# Override existing environment variables
pytest --override-existing-vars
```

## Configuration Options

### `env_files`

Specify one or more dotenv files to load:

```ini
[pytest]
env_files =
    .env
    .env.test
    .env.deploy
```

Files are loaded in the order specified. The plugin searches for files in the current directory and parent directories.

### `env_override_existing_values`

Control whether to override existing environment variables:

```ini
[pytest]
env_override_existing_values = 1  # Override existing vars
# env_override_existing_values = 0  # Don't override (default)
```

### Command Line Options

- `--envfile PATH`: Load environment variables from specified file(s)
- `--override-existing-vars`: Override existing environment variables

## Examples

### Basic Usage

```python
# test_example.py
import os

def test_environment_variables():
    # These variables are loaded from your .env file
    assert os.getenv("DATABASE_URL") == "sqlite:///test.db"
    assert os.getenv("API_KEY") == "your-test-api-key"
    assert os.getenv("DEBUG") == "True"
```

### Multiple Environment Files

```ini
# pytest.ini
[pytest]
env_files = 
    .env           # Base configuration
    .env.test      # Test-specific overrides
    .env.local     # Local developer settings
```

### Environment-Specific Testing

```bash
# Test with development environment
pytest --envfile .env.development

# Test with staging environment  
pytest --envfile .env.staging

# Test with production environment
pytest --envfile .env.production
```

## Advanced Usage

### Programmatic Access

You can access the plugin instance from your tests:

```python
import pytest
from pytest_dotenv_modern import get_dotenv_plugin

def test_plugin_info():
    plugin = get_dotenv_plugin()
    if plugin:
        loaded_files = plugin.loaded_files
        print(f"Loaded {len(loaded_files)} dotenv files")
```

### Custom Configuration

```python
# conftest.py
import pytest
from pytest_dotenv_modern.plugin import DotenvPlugin

@pytest.fixture(scope="session")
def setup_custom_env(request):
    """Load additional environment files for specific test runs."""
    plugin = DotenvPlugin(request.config)
    
    # Load additional file based on test marker
    if request.node.get_closest_marker("integration"):
        plugin.load_file(".env.integration", override=True)
    
    return plugin
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/jobissjo/pytest-dotenv-modern.git
cd pytest-dotenv-modern

# Install with uv
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run tests with uv
uv run pytest

# Run tests with coverage
uv run pytest --cov=pytest_dotenv --cov-report=html

# Run with different Python versions using tox
tox
```

### Code Quality

```bash
# Format code
uv run black src tests
uv run isort src tests

# Lint code
uv run flake8 src tests
uv run mypy src

# Run pre-commit hooks
uv run pre-commit run --all-files
```

## Migration from pytest-dotenv

This plugin is designed as a drop-in replacement for the original `pytest-dotenv`. 

### Breaking Changes

- Minimum Python version is 3.8+
- Package name changed to `pytest-dotenv-modern`
- Some internal APIs may have changed

### Migration Steps

1. Uninstall the old plugin:
   ```bash
   pip uninstall pytest-dotenv
   ```

2. Install the new plugin:
   ```bash
   uv add pytest-dotenv-modern
   ```

3. Update any imports (if you were importing from the plugin):
   ```python
   # Old
   from pytest_dotenv import ...
   
   # New  
   from pytest_dotenv_modern import ...  # Same import path!
   ```

4. Your existing configuration should work without changes!

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

## License

MIT License - see LICENSE file for details.

## Changelog

### 0.1.0

- Initial release
- Modern Python 3.8+ support
- Full pytest compatibility
- Comprehensive test suite