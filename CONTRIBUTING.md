# Contributing to ToolUniverse CLI

Thank you for your interest in contributing to ToolUniverse CLI!

## Development Setup

### 1. Create a virtual environment

```bash
cd /path/to/tooluniverse-cli
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install in development mode

```bash
pip install -e .
```

This will install the package in development mode, allowing you to make changes and test them without reinstalling.

### 3. Install development dependencies

```bash
pip install pytest pytest-cov black isort flake8
```

## Testing

Run tests with pytest:

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=tooluniverse_cli
```

## Code Style

Format your code with Black and isort:

```bash
black src tests
isort src tests
```

Check code quality with flake8:

```bash
flake8 src tests
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## Release Process

1. Update version in `pyproject.toml`
2. Create a new tag: `git tag v0.1.0`
3. Push the tag: `git push origin v0.1.0`
4. Build the package: `python -m build`
5. Upload to PyPI: `python -m twine upload dist/*`
