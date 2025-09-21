# Abstract Syntax Tree Experiments with Data Structures

Yeah, very long repository name... but Welcome!

This repo is a study playground for learning and apply Python's AST module.

The goal is simple: feed in a JSON example and get back strongly typed Python structures like dataclasses, TypedDicts, attrs classes, NamedTuples, or Pydantic models using a factory design pattern.

## What is the Python`s AST?

The Abstract Syntax Tree is a tree representation of a code's structure. It's like a hierarchical map of how a code is built, from the simplest operations to the most complex class implementations. Using AST, one can access and modify the code in a metaprogramming approach or maybe build code using code (without parsing a lot of strings, lol).

Every time we code in Python, the Python interpreter first analyses our source code and then converts it into an AST. All static code analysis tools like Mypy or Pyright use AST. Formatters and linters do as well, I'm pretty sure, but I didn't check, to be honest. It's a great tool to have and worth exploring.  

## Quick CLI peek

Everything lives behind a small command-line tool:

- Infers types from JSON samples (numbers, booleans, nested objects, lists, etc.).
- Constructs Python AST nodes that describe the desired structure.
- Unparses those nodes into ready-to-use Python code with full type annotations.
- Supports multiple output styles so I can compare ergonomics side by side.

After installing the project dependencies with `make install`, you can experiment like this:

```bash
uv run aste \
  --json examples/user_example.json \
  --type dataclass \
  --name User
```

Key switches:

- `--type`: choose from `typed_dict`, `dataclass`, `pydantic`, `namedtuple`, or `attrs`.
- `--json` or `--url`: provide a local JSON file or fetch one from the web.
- `--name`: set the class name (defaults to `GeneratedModel`).
- `--output`: optionally save the generated code to a file; otherwise it prints to stdout.

There is also a bundled sample:

```bash
uv run aste --type attrs
```

Both commands leverage the `aste` console script defined in `pyproject.toml`, so the CLI is available immediately after syncing dependencies.

This command infers types from `examples/user_example.json` and renders an attrs class directly in the terminal.

## Developing and testing

> It's a study repository, but we are not savages here.

If you are too lazy to write `uv sync --dev`, run `make dev`.

- Run ruff with `make format` and `make lint`
- Run the static checker (Pyright) with `make type-check`
- Run tests with `make test`

## License

Feel free to explore, remix, or borrow ideas for your own learning journey.
