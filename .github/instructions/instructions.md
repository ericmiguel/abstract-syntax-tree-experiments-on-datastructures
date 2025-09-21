# Abstract Syntax Tree Experiments - AI Coding Guidelines

## Project Overview

**Repository**: `abstract-syntax-tree-experiments`  
**Owner**: ericmiguel  
**Purpose**: Experimental repository for Abstract Syntax Tree (AST) manipulation and code generation building using Python's AST module.

### Core Components

1. **Data Structure Builders** (`src/aste/datastructures/`)
   - Abstract factory pattern for generating Python data structures
   - AST-based code generation for TypedDict, dataclasses, etc.
   - Template method pattern implementation

## Development Environment

### Dependencies & Tooling
- **Python**: `>=3.13` (uses modern type syntax)
- **Package Manager**: `uv` (modern Python package manager)
- **Linting**: `ruff` (fast Python linter/formatter)
- **Type Checking**: `pyright` (Microsoft's TypeScript-based type checker)
- **UI Libraries**: `rich` (terminal formatting), `pydantic` (data validation)

### Build Commands
- `make install` - Install dependencies
- `make dev` - Install with dev dependencies  
- `make format` - Format code with ruff
- `make lint` - Lint and fix code issues
- `make type-check` - Run type checking
- `make check` - Run all quality checks

## Coding Standards & Guidelines

### Type Safety (CRITICAL)
- **Always use modern Python 3.10+ type syntax**:
  - ✅ `list[dict[str, Any]]` instead of `List[Dict[str, Any]]`
  - ✅ `str | None` instead of `Optional[str]`  
  - ✅ `int | float` instead of `Union[int, float]`
- **Comprehensive type annotations**: Every function, method, and class attribute must have type hints
- **Type-safe data structures**: Prefer dataclasses with explicit types over dictionaries
- **No `Any` without justification**: Only use `Any` when truly dynamic content is needed

### Language & Documentation
- **English Only**: All code, comments, docstrings, and variable names in English
- **Docstring Standard**: Use NumPy style with max 88 characters per line
```python
def example_method(param: str, option: bool = False) -> dict[str, Any]:
    """
    Brief description of the method.

    Parameters
    ----------
    param : str
        Description of param parameter.
    option : bool, optional
        Description of option parameter, by default False

    Returns
    -------
    dict[str, Any]
        Description of return value.

    Examples
    --------
    >>> example_method("test", option=True)
    {'result': 'test processed'}
    """
```

### Architecture Principles
1. **Prototype-First**: This is experimental code - prioritize clean, type-safe APIs over backward compatibility
2. **Fluent Interfaces**: Chain methods for pipeline building (e.g., `.match().group().sort()`)
3. **Immutable Data**: Use dataclasses for configuration objects
4. **Rich Output**: Always use Rich library for beautiful terminal formatting
5. **Factory Patterns**: Use factory/builder patterns for complex object creation

### Data Structure Builder Specifics
- **Template Method Pattern**: Abstract base class defines structure, concrete builders implement details
- **Factory Pattern**: Use `DataStructureFactory.get_builder()` for builder instantiation
- **AST-Based Generation**: All code generation uses Python's `ast` module for type-safe manipulation
- **Multiple Formats**: Support TypedDict, dataclass, Pydantic, NamedTuple, and attrs
- **Separation of Concerns**: Base class, concrete builders, and factory in separate modules

### Code Organization
```
src/aste/
├── __init__.py                    # Package root exports
├── datastructures/                # AST-based code generation
│   ├── __init__.py               # Public API exports
│   ├── base.py                   # DataStructureBuilder ABC
│   ├── builders.py               # Concrete builder implementations
│   └── factory.py                # DataStructureFactory
└── cli/                          # Command-line interface
    ├── __init__.py               # CLI exports
    └── main.py                   # CLI entry point
```

### Error Handling
- **Descriptive Errors**: Include field names, model names, and suggestions in error messages
- **Early Validation**: Validate inputs at method entry, not during execution
- **Type Safety**: Leverage type system to prevent errors at compile time

### Testing & Quality
- **Type Checking**: Must pass `make type-check` with 0 errors
- **Linting**: Must pass `make lint` with minimal warnings
- **Examples**: Every public method should have working examples in docstrings
- **Rich Output**: Test that Rich formatting works correctly

## Specific Implementation Guidelines

### AST Manipulation
- Use visitor pattern for AST traversal
- Validate AST node types before processing
- Provide helpful error messages for unsupported constructs

### Data Structure Generation
- **Template Method Pattern**: `DataStructureBuilder.build()` orchestrates the generation process
- **Abstract Methods**: Subclasses implement `_build_imports()`, `_build_body_nodes()`, `_build_bases()`
- **Optional Hook**: `_build_decorators()` can be overridden for decorator-based patterns
- **Supported Formats**: TypedDict, dataclass, Pydantic BaseModel, NamedTuple, attrs
- **Proper AST Generation**: Use `ast.fix_missing_locations()` and `ast.unparse()` for clean output
- **Type Annotations**: All generated fields include proper type annotations

## AI Assistant Behavior

### When Generating Code:
1. **Always** check current file contents before making edits
2. **Always** use modern Python type syntax (3.10+)
3. **Always** include comprehensive type annotations
4. **Always** write English docstrings in NumPy format
5. **Always** test code with `make type-check` and `make lint`
6. **Always** use Rich for formatted output

### When Reviewing Changes:
1. Verify type safety and modern syntax usage
2. Check that all docstrings are in English with proper format
3. Ensure error messages are descriptive and helpful
4. Validate that examples in docstrings are realistic and working

### When Answering Questions:
1. Reference specific code patterns from the existing codebase
2. Suggest type-safe alternatives to dynamic approaches
3. Recommend using existing utilities (Rich, dataclasses, etc.)
4. Consider both the experimental nature and code quality standards

## Project Philosophy

This is an **experimental repository** focused on:
- **Modern Python features** (AST manipulation, advanced typing)
- **Beautiful developer experience** (Rich formatting, fluent APIs)
- **Type safety as a first-class citizen**
- **Clean, readable, maintainable code**

When in doubt, favor **explicitness over implicitness** and **type safety over convenience**.