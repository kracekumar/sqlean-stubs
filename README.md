# sqlean-stubs

Type hints for [sqlean.py](https://github.com/nalgeon/sqlean.py) - Python's sqlite3 + extensions.

This package provides comprehensive type hints for the sqlean library, enabling better IDE support and static type checking with tools like mypy and ty.

## Installation

### Using pip

```bash
pip install sqlean-stubs
```

### Using uv

```bash
uv add sqlean-stubs
```

Once installed, type checkers like mypy, pyright, and IDE autocomplete will automatically detect the type information.

## Usage

Once installed, the type hints enable full type checking and IDE autocomplete support for sqlean:

```python
import sqlean

# Type checker knows conn is of type Connection
conn: sqlean.Connection = sqlean.connect(":memory:")

# Type checker knows cursor is of type Cursor
cursor = conn.cursor()

# Type hints work with query parameters
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))

# Type checker knows fetchone() returns Optional[Any]
row = cursor.fetchone()
if row is not None:
    # IDE provides autocomplete and type checking
    print(row[0])  # Access by index
    print(row["name"])  # Access by column name (with Row factory)

# Type hints work with Row factory
conn.row_factory = sqlean.Row
cursor.execute("SELECT id, name FROM users")
rows = cursor.fetchall()  # Type checker knows this is List[Any]

# Type hints for user-defined functions
def double(x: int) -> int:
    return x * 2

conn.create_function("double", 1, double)
cursor.execute("SELECT double(21)")
result = cursor.fetchone()

conn.close()
```

**Benefits:**

- **IDE Autocomplete**: Get code completion suggestions as you type
- **Type Checking**: Catch type errors before runtime with mypy or ty
- **Better Documentation**: Type hints serve as inline documentation
- **Refactoring Safety**: Rename and refactor with confidence

## Features

- Complete type hints for Connection, Cursor, and Row objects
- Support for custom factories and row factories
- Type hints for user-defined functions and aggregates
- Support for callbacks (authorizer, progress handler, trace callback, busy handler)
- Window function support
- Extensions management API
- Fully compatible with mypy, ty, pyright, and other type checkers

## Requirements

- **Python**: 3.9 or later
- **Package Manager**: `pip`, `uv`, or `pipx`

## Python Version Support

This project supports **Python 3.9 to 3.14**. When using uv, it will automatically use your default Python version, or you can specify one:

```bash
# Use a specific Python version
uv sync --python 3.12

# Run tests with a specific Python version
uv run --python 3.11 pytest tests/
```

---

## Contributing

Thank you for your interest in contributing to sqlean-stubs!

### Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management. Install uv from https://docs.astral.sh/uv/getting-started/installation/

```bash
# Clone this repository
git clone https://github.com/nalgeon/sqlean-stubs.git
cd sqlean-stubs

# Sync dependencies (creates virtual environment automatically)
uv sync

# Or use a specific Python version
uv sync --python 3.12
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run type checking with mypy
uv run mypy tests/test_mypy.py

# Run type checking with ty
uv run ty check

# Run tests across multiple Python versions (3.9-3.14) with tox
uv run tox

# Run a specific test
uv run pytest tests/test_types.py::test_connect_returns_connection -v
```

### Type Stub Structure

The type hints are organized as follows:

- `sqlean/__init__.pyi` - Package exports and re-exports
- `sqlean/dbapi2.pyi` - Main DB-API 2.0 interface (Connection, Cursor, Row, exceptions, constants)
- `sqlean/extensions.pyi` - Extension management API
- `sqlean/py.typed` - PEP 561 marker file (empty file required for typed packages)

### Key Design Decisions

#### Row Class
The `Row` class supports:
- Integer indexing: `row[0]`
- String indexing (column names): `row["column_name"]`
- Slicing: `row[1:3]`

#### Overloads for execute()
The `execute()` method has three overloads:
1. With no parameters: `execute(sql: str)`
2. With sequence parameters: `execute(sql: str, parameters: Sequence[...])`
3. With dict parameters: `execute(sql: str, parameters: Dict[...])`

#### Type Aliases
Key type aliases:
- `_SQLiteValue` - Types that can be stored in SQLite (str, int, float, bytes, None)
- `_SQLiteParam` - Types that can be used as parameters (includes memoryview)
- `_Parameters` - Either Sequence or Dict of parameters
- `_RowFactory` - Callable that transforms cursor results into row objects

### Adding New Type Hints

When adding type hints for new sqlean features:

1. Update the `.pyi` stub file with the new types
2. Add corresponding test in `tests/test_types.py` (runtime tests)
3. Add type checking tests in `tests/test_mypy.py`
4. Run `pytest tests/` to verify all tests pass
5. Run `mypy tests/test_mypy.py` to verify type checking works
6. Run `ty check` to verify ty type checking works

### Testing Guidelines

- **Runtime tests** (`test_types.py`): Verify the functionality actually works with sqlean
- **Type tests** (`test_mypy.py`): Verify mypy can correctly type-check the code

Tests should cover:
- Basic functionality
- Edge cases (None, empty sequences, etc.)
- Different parameter types
- All public methods and properties
- Factory patterns and callbacks

### Code Style

- Follow PEP 484 for type hints
- Use `Optional[X]` instead of `X | None` for Python 3.9 compatibility
- Use `Literal` types for constrained string values
- Provide docstrings for complex type definitions

### Validation

Before submitting a contribution:

```bash
# Run all tests
uv run pytest tests/ -v

# Run type checking with mypy
uv run mypy tests/test_mypy.py

# Run type checking with ty
uv run ty check

# Check for any issues
uv run mypy sqlean/ --show-error-codes
```

### Common Issues

#### "Single overload definition, multiple required"
This error occurs when you have an `@overload` decorator but only one definition. Either:
- Remove the `@overload` decorator if there's only one signature
- Add more overload variants

#### "Signature of ... incompatible with supertype"
When overriding methods from base classes (like `Sequence`), ensure your signature is compatible with the parent class signature.

#### MyPy not finding types
Ensure the `py.typed` marker file exists in the `sqlean/` directory. This file can be empty but must be present for the package to be recognized as typed.

### Environment Variables

uv automatically manages the virtual environment. The environment is created in:
- `.venv/` directory (standard location)
- Or `VIRTUAL_ENV` environment variable if set

To activate the environment manually (rarely needed):

```bash
# Source the activation script
source .venv/bin/activate
```

### Questions?

If you have questions about the type hints or how they should work, please open an issue or check the [sqlean.py](https://github.com/nalgeon/sqlean.py) project documentation.

## License

Zlib (same as sqlean.py)
