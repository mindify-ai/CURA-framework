# CURA Framework

CURA (Code Understanding & Reasoning Agent) is a modular framework for programmatic code reasoning, test generation, and code synthesis using LLMs. It is designed for research and practical applications in code generation, evaluation, and dataset creation.

## Features
- Modular agent and pipeline design
- Automated prompt engineering for code understanding, test generation, and code synthesis
- Dataset generation and evaluation utilities
- CLI for batch evaluation

## Installation

You can install CURA and its dependencies using pip:

```bash
pip install .
```

Or with Poetry:

```bash
poetry install
```

## Requirements
- Python 3.9+
- macOS, Linux, or Windows

## Usage

### Programmatic API

```python
from cura.agent import Agent

agent = Agent(
    name="CodeGenAgent",
    description="Generates code from prompts",
    tools=[],
    model="gpt-4o-mini"
)

result = agent.run("Write a Python function to add two numbers.")
print(result)
```

### CURA Pipeline

```python
from cura.pipeline import CURAPipeline

pipeline = CURAPipeline()
code = pipeline.generate("Write a function to reverse a string.")
print(code)
```

### CLI

You can run dataset evaluation from the command line:

```bash
python cli.py evaluate-dataset --subset hard --split complete
```

## Project Structure

```
cura/
    __init__.py
    agent.py
    base_agent.py
    pipeline.py
    prompts.py
    tasks.py
    utils.py
cli.py
sample.py
setup.py
requirements.txt
README.md
```

## Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key for LLM access.

## License
MIT License