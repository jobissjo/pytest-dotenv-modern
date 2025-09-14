# Complete Project Setup Guide

## Project Structure

Create the following directory structure:

```
pytest-dotenv-modern/
├── src/
│   └── pytest_dotenv/
│       ├── __init__.py
│       └── plugin.py
├── tests/
│   ├── __init__.py
│   ├── test_plugin.py
│   └── conftest.py
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
└── tox.ini
```

## Additional Files Needed

Let me create the remaining essential files:

### LICENSE
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### .gitignore
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pytest, python-dotenv, types-all]
```

### tox.ini
```ini
[tox]
envlist = py38,py39,py310,py311,py312,lint,type-check
isolated_build = true

[testenv]
deps = 
    pytest>=6.0.0
    pytest-cov
    python-dotenv>=0.19.0
commands = 
    pytest tests/ --cov=pytest_dotenv --cov-report=term-missing

[testenv:lint]
deps = 
    black
    isort
    flake8
commands = 
    black --check src tests
    isort --check-only src tests
    flake8 src tests

[testenv:type-check]
deps = 
    mypy
    pytest
    python-dotenv
    types-all
commands = 
    mypy src

[testenv:format]
deps = 
    black
    isort
commands = 
    black src tests
    isort src tests

[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

## Step-by-Step Setup Instructions

### 1. Initialize the Project

```bash
# Create project directory
mkdir pytest-dotenv-modern
cd pytest-dotenv-modern

# Initialize with uv
uv init --name pytest-dotenv-modern --package

# Or initialize git repository
git init
```

### 2. Create the Directory Structure

```bash
# Create source directory
mkdir -p src/pytest_dotenv
mkdir -p tests

# Create __init__.py files
touch src/pytest_dotenv/__init__.py
touch tests/__init__.py
```

### 3. Add the Files

Copy each artifact content into the respective files:
- `pyproject.toml` → root directory
- `src/pytest_dotenv/__init__.py` → package initialization
- `src/pytest_dotenv/plugin.py` → main plugin code
- `tests/test_plugin.py` → test suite
- `README.md` → project documentation

### 4. Install Development Dependencies

```bash
# With uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### 5. Set Up Pre-commit (Optional but Recommended)

```bash
uv run pre-commit install
# or
pip install pre-commit
pre-commit install
```

### 6. Run Tests

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=pytest_dotenv --cov-report=html

# Run linting
uv run black src tests
uv run isort src tests  
uv run flake8 src tests
uv run mypy src
```

### 7. Build the Package

```bash
# Build wheel and source distribution
uv build

# Or with build
pip install build
python -m build
```

### 8. Test the Package Locally

```bash
# Install in development mode
uv pip install -e .

# Create a test project
mkdir test-project
cd test-project

# Create a .env file
echo "TEST_VAR=hello_world" > .env

# Create a simple test
cat > test_example.py << EOF
import os

def test_env_loaded():
    assert os.getenv("TEST_VAR") == "hello_world"
EOF

# Run pytest (your plugin should load the .env automatically)
pytest test_example.py -v
```

## Publishing to PyPI

### 1. Set Up PyPI Account
- Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
- Generate API tokens

### 2. Configure uv for Publishing

```bash
# Test on TestPyPI first
uv publish --index-url https://test.pypi.org/legacy/

# Publish to PyPI
uv publish
```

### 3. Or Use Twine

```bash
# Install twine
pip install twine

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI  
twine upload dist/*
```

## Customization Tips

### 1. Update Package Metadata

In `pyproject.toml`, update:
- `name`: Your package name
- `authors`: Your information
- `project.urls`: Your repository URLs

### 2. Add More Features

Consider adding:
- Support for different file formats (YAML, TOML)
- Environment variable validation
- Integration with specific testing frameworks
- Docker support

### 3. Improve Documentation

Add:
- API documentation with Sphinx
- More usage examples
- Integration guides for popular frameworks

## Troubleshooting

### Common Issues

1. **Plugin not discovered**: Ensure the entry point in `pyproject.toml` is correct
2. **Import errors**: Check that `src/pytest_dotenv/__init__.py` exists
3. **Tests fail**: Verify all dependencies are installed

### Debug Mode

```bash
# Run pytest with verbose plugin info
pytest --trace-config

# Check if plugin is loaded
pytest --help | grep -i dotenv
```

This setup gives you a complete, modern pytest plugin that's ready for development and distribution!