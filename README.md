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
pyline validate -c examples/pipeline.yaml
pyline run -c examples/pipeline.yaml -d hello
```

Validate checks pipeline configuration before you run:

```bash
pyline validate -c examples/pipeline.yaml
```

Or from Python:

```python
from pyline import PyLineEngine

engine = PyLineEngine.from_config("examples/pipeline.yaml")
ctx = engine.run(initial_data="hello")
print(ctx.data, ctx.metadata)
```

## Architecture

A single pipeline request flows through:

```
Client (CLI or script) → pyline → load_pipeline → PyLineEngine → plugins (chain) → external API
```

Each `pyline run` or `engine.run()` call loads YAML, instantiates plugins, and passes a shared `PipelineContext` through each step.

## Pipeline configuration

Pipelines are defined in YAML:

```yaml
name: demo
plugins:
  - name: uppercase
  - name: trim
  - name: httpbin
    config:
      path: /get
      base_url: https://httpbin.org
      params:
        foo: bar
      retry: 2
    retry: 3
```

- `name` — pipeline identifier
- `plugins` — ordered list; each entry needs `name` (built-in registry name) and optional `config`
- `retry` — optional non-negative integer; number of retries on transient failures
- Each plugin should implement `configure()` to read its `config` block from YAML

Environment-specific values can be set in `config/prod.yaml` or via `PYLINE_*` env vars. Use `PYLINE_ENV=prod` to select config (see `config/dev.yaml` and `config/prod.yaml`).

Timeouts and retries are handled by the API client layer.

**Session**: pipeline context and HTTP client state passed between plugins.

## Writing plugins

See [src/pyline/plugins/README.md](src/pyline/plugins/README.md) for extension options.

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

Replace `httpbin` with your own API plugin when integrating a different backend.

Built-in plugins: `uppercase`, `trim`, `httpbin`.

External example (`module` / `class` in YAML):

```yaml
plugins:
  - name: hello
    module: examples.plugins.hello_plugin
    class: HelloPlugin
```

## Performance

- Network I/O in API plugins (e.g. `httpbin`) dominates latency for typical pipelines
- Long plugin chains increase sequential processing time
- Enable parallel mode in pipeline config for independent steps (see roadmap)

## Logging

| Level | Component | Destination |
|-------|-----------|-------------|
| INFO | Engine, plugin loader | stderr (`pyline.*` loggers) |
| INFO | HTTP requests | logged by APIClient |
| output | Pipeline result (`pyline run`) | stdout (pipeline output log) |

Set `PYLINE_LOG_LEVEL` for verbose diagnostics.

## Roadmap

- Parallel plugin execution for independent steps
- Dry-run mode to preview pipeline steps without side effects
- `pyline serve` HTTP API for remote pipeline execution

## Project layout

```
src/pyline/
  core.py           # PyLineEngine / RequestPipeline
  config/           # YAML loading, settings
  context.py        # PipelineContext
  plugins/
    trim_plugin.py
    example_plugin.py
    httpbin_plugin.py
  api/              # APIClient, APIPlugin
config/
  dev.yaml
  prod.yaml
examples/
tests/
```

## Tests

```bash
pytest
```
