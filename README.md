# RavenNet

[![Daily Intelligence Run](https://github.com/PR-CYBR/rav3n-n3t/actions/workflows/daily-intelligence.yml/badge.svg)](https://github.com/PR-CYBR/rav3n-n3t/actions/workflows/daily-intelligence.yml)

Central orchestration hub for pr-cybr's **rav3n-n3t** framework — coordinates the **Huginn** and **Muninn** pipelines, automates intelligence workflows, and publishes reports across pr-cybr platforms.

## Overview

RavenNet is the central nervous system of the rav3n-n3t intelligence framework, orchestrating two complementary pipelines:

- **Huginn**: The "thought" pipeline - gathers and processes information
- **Muninn**: The "memory" pipeline - analyzes, stores, and retrieves intelligence

Named after Odin's ravens in Norse mythology, RavenNet ensures these pipelines work in harmony to deliver actionable intelligence.

## Architecture

```
RavenNet (Orchestrator)
    ├── Huginn Pipeline (Thought/Collection)
    │   ├── Data Gathering
    │   ├── Processing
    │   └── Initial Analysis
    │
    └── Muninn Pipeline (Memory/Storage)
        ├── Deep Analysis
        ├── Knowledge Storage
        └── Report Generation
```

## Features

- **Automated Orchestration**: Sequential execution of Huginn → Muninn pipelines
- **Daily Scheduling**: Automated runs via GitHub Actions
- **Output Management**: Captures and archives pipeline results
- **Report Publishing**: Prepares summaries for distribution
- **Error Handling**: Robust failure detection and reporting
- **Extensible**: Easy to add new pipelines or modify existing workflows

## Installation

### For Development

```bash
# Clone the repository
git clone https://github.com/PR-CYBR/rav3n-n3t.git
cd rav3n-n3t

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### For Production

```bash
pip install git+https://github.com/PR-CYBR/rav3n-n3t.git
```

## Usage

### Command Line Interface

```bash
# Run full orchestration (Huginn → Muninn)
ravennet run

# Run only Huginn pipeline
ravennet run --pipeline huginn

# Run only Muninn pipeline
ravennet run --pipeline muninn

# Run with custom configuration
ravennet run --config config.yaml

# Check status of last run
ravennet status
```

### Python API

```python
from ravennet import Orchestrator

# Create orchestrator instance
orchestrator = Orchestrator()

# Run full pipeline
results = orchestrator.run_full_pipeline()

# Access results
huginn_output = results['huginn']
muninn_output = results['muninn']
```

## Configuration

RavenNet can be configured via YAML file or environment variables:

```yaml
# config.yaml
pipelines:
  huginn:
    enabled: true
    timeout: 3600
    retry_count: 3
  
  muninn:
    enabled: true
    timeout: 3600
    retry_count: 3

output:
  directory: "./reports"
  archive: true
  format: "json"

notifications:
  on_failure: true
  on_success: false
```

## Project Structure

```
rav3n-n3t/
├── src/ravennet/          # Main package
│   ├── __init__.py
│   ├── orchestrator.py    # Core orchestration logic
│   ├── pipelines/         # Pipeline implementations
│   │   ├── __init__.py
│   │   ├── huginn.py
│   │   └── muninn.py
│   ├── config.py          # Configuration management
│   ├── reporter.py        # Report generation
│   └── cli.py             # Command-line interface
├── tests/                 # Test suite
├── .github/workflows/     # GitHub Actions
├── pyproject.toml         # Project metadata
└── README.md
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ravennet --cov-report=html

# Run specific test file
pytest tests/test_orchestrator.py
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Deployment

RavenNet runs automatically every day via GitHub Actions. The workflow:

1. Sets up Python environment
2. Installs dependencies
3. Runs Huginn pipeline
4. Runs Muninn pipeline
5. Archives outputs
6. Publishes reports (if configured)

Manual triggers are also available through GitHub Actions UI.

## Roadmap

### Phase 1: Scaffolding ✅
- [x] Project structure
- [x] README and documentation
- [x] GitHub Actions daily trigger

### Phase 2: Orchestration (In Progress)
- [ ] Implement Huginn pipeline runner
- [ ] Implement Muninn pipeline runner
- [ ] Sequential execution logic
- [ ] Output capture and handling

### Phase 3: Publication
- [ ] Report archiving
- [ ] Summary generation
- [ ] Publishing mechanisms
- [ ] Notification system

## Contributing

Contributions are welcome! Please ensure:

1. Code follows existing style (black formatting)
2. Tests are included for new features
3. Documentation is updated
4. All tests pass

## License

MIT License - See LICENSE file for details

## Contact

For questions or issues, please open an issue on GitHub or contact the PR-CYBR team.

---

*Part of the pr-cybr intelligence framework*
