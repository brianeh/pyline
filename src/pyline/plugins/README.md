# Plugins

Ways to add a plugin to PyLine:

1. **Built-in registry** — subclass `Plugin`, use `@register_plugin("name")`, import the module from `registry._register_builtins()`.
2. **Pipeline YAML** — set `module` and `class` on a plugin entry (see `examples/plugins/`).
3. **Legacy file** — add `plugins/{name}.py` next to this package with a `run(data)` function or `Plugin` class.
4. **Setuptools entry point** — register under `pyline.plugins` in `pyproject.toml` (see project packaging docs).

Built-in plugins: `uppercase`, `trim`, `httpbin`.
