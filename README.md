# PyLine

PyLine is a modular Python framework for building plugin-based pipelines and reusable API integrations.

## Install

```bash
pip install -e .
pip install -e ".[dev]"   # optional: pytest, ruff
```

## Quick start

```bash
pyline list
pyline run -c examples/pipeline.yaml -d hello
```

Or from Python:

```python
from pyline import PyLineEngine

engine = PyLineEngine.from_config("examples/pipeline.yaml")
ctx = engine.run(initial_data="hello")
print(ctx.data, ctx.metadata)
```

## Pipeline configuration

Pipelines are defined in YAML:

```yaml
name: demo
plugins:
  - name: uppercase
  - name: httpbin
    config:
      path: /get
      params:
        foo: bar
```

- `name` — pipeline identifier
- `plugins` — ordered list; each entry needs `name` (built-in registry name) and optional `config`
- External plugins: set `module` and `class` instead of a built-in `name`

## Writing plugins

### Transform plugin

Subclass `Plugin` and register with `@register_plugin("my_plugin")`:

```python
from pyline import Plugin, PipelineContext
from pyline.plugins.registry import register_plugin

@register_plugin("my_plugin")
class MyPlugin(Plugin):
    name = "my_plugin"

    def configure(self, config: dict) -> None:
        ...

    def run(self, ctx: PipelineContext) -> PipelineContext:
        ctx.data = ...
        return ctx
```

### API plugin

Subclass `APIPlugin`, implement `request()`, and use `self.client` (`APIClient`):

```python
from pyline.api.base import APIPlugin

class MyAPIPlugin(APIPlugin):
    def __init__(self):
        super().__init__("https://api.example.com", api_key="...")

    def request(self, ctx):
        return self.client.get("/resource", params={"q": ctx.data})
```

Built-in examples: `uppercase`, `httpbin`.

## Project layout

```
src/pyline/
  core.py           # PyLineEngine
  config.py         # YAML loading
  context.py        # PipelineContext
  plugins/          # Plugin base, loader, registry, builtins
  api/              # APIClient, APIPlugin
  cli.py            # pyline run | list
examples/
tests/
```

## Tests

```bash
pytest
```
