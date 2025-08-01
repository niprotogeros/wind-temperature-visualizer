
# Contributing to Wind Temperature Visualizer

Thank you for your interest in contributing to the Wind Temperature Visualizer project! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Docker (optional, for containerized development)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/wind-temperature-visualizer.git
   cd wind-temperature-visualizer
   ```

## Development Setup

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

4. Run the application:
   ```bash
   streamlit run src/wind_temp_visualizer.py
   ```

### Docker Development

1. Build and run with Docker Compose:
   ```bash
   # For development with hot reload
   docker-compose --profile dev up wind-temp-visualizer-dev
   
   # For production-like environment
   docker-compose up wind-temp-visualizer
   ```

2. Access the application at `http://localhost:8501` (or `8502` for dev)

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-chart-type`
- `bugfix/fix-temperature-calculation`
- `docs/update-installation-guide`

### Commit Messages

Follow conventional commit format:
- `feat: add wind rose visualization`
- `fix: correct temperature unit conversion`
- `docs: update README with Docker instructions`
- `test: add unit tests for data processing`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_data_processing.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both happy path and edge cases
- Mock external dependencies when appropriate

## Code Style

We use several tools to maintain code quality:

### Formatting

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/
```

### Linting

```bash
# Check code style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Pre-commit Hooks

Pre-commit hooks will automatically run these tools before each commit. To run manually:

```bash
pre-commit run --all-files
```

## Submitting Changes

### Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests as needed
3. Update documentation if necessary
4. Ensure all tests pass
5. Create a pull request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for changes
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Sample EPW file (if relevant)

### Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use case or problem it solves
- Proposed implementation (if any)
- Examples or mockups (if applicable)

## Development Guidelines

### Code Organization

- Keep functions small and focused
- Use meaningful variable and function names
- Add docstrings for public functions
- Separate concerns (data processing, visualization, UI)

### Performance Considerations

- Profile code for large datasets
- Use efficient pandas operations
- Consider memory usage for large EPW files
- Implement caching where appropriate

### Accessibility

- Ensure visualizations are colorblind-friendly
- Provide alternative text for charts
- Use semantic HTML elements
- Test with screen readers when possible

## Getting Help

- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Join our community chat (if available)
- Contact maintainers for urgent issues

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- README.md contributors section
- GitHub contributors page

Thank you for contributing to Wind Temperature Visualizer!
