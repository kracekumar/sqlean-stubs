"""Tests that verify type hints work correctly with mypy."""

# This file is not meant to be executed directly, but rather analyzed by mypy
# to verify type hints are correct. Run: mypy tests/test_mypy.py

from typing import TYPE_CHECKING, Dict, Optional, List
import sqlean
from sqlean import dbapi2, extensions

if TYPE_CHECKING:
    # These imports are only for type checking
    from typing import Sequence, Callable, Any, Tuple


def test_basic_connection() -> None:
    """Test basic connection and query."""
    conn: sqlean.Connection = sqlean.connect(":memory:")
    
    # Should be able to call cursor
    cursor: sqlean.Cursor = conn.cursor()
    
    # Should be able to execute
    result_cursor: sqlean.Cursor = cursor.execute("SELECT 1")
    
    # Should be able to fetch
    row: Optional[tuple] = cursor.fetchone()
    rows: List[tuple] = cursor.fetchall()
    many_rows: List[tuple] = cursor.fetchmany(10)
    
    # Should be able to commit/rollback
    conn.commit()
    conn.rollback()
    
    # Should be able to close
    cursor.close()
    conn.close()


def test_context_manager() -> None:
    """Test connection as context manager."""
    with sqlean.connect(":memory:") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")


def test_row_factory() -> None:
    """Test row factory type hints."""
    conn: sqlean.Connection = sqlean.connect(":memory:")
    
    # Test with Row factory
    conn.row_factory = sqlean.Row
    cursor = conn.execute("SELECT 1 AS num")
    row: Optional[sqlean.Row] = cursor.fetchone()
    
    if row:
        # Should be able to access by index
        val_idx: sqlean.dbapi2._SQLiteValue = row[0]
        # Should be able to access by name
        val_name: sqlean.dbapi2._SQLiteValue = row["num"]
    
    conn.close()


def test_custom_row_factory() -> None:
    """Test custom row factory."""
    from typing import Any
    def dict_factory(
        cursor: sqlean.Cursor, row: tuple
    ) -> Dict[str, Any]:
        return {desc[0]: val for desc, val in zip(cursor.description or [], row)}
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.row_factory = dict_factory
    cursor = conn.execute("SELECT 1 AS num")
    row: Optional[Dict[str, Any]] = cursor.fetchone()
    conn.close()


def test_text_factory() -> None:
    """Test text factory type hints."""
    conn: sqlean.Connection = sqlean.connect(":memory:")
    
    # Test default (str)
    conn.text_factory = str
    
    # Test bytes
    conn.text_factory = bytes
    
    # Test bytearray
    conn.text_factory = bytearray
    
    # Test custom
    conn.text_factory = lambda x: x.decode("utf-8")
    
    conn.close()


def test_execute_with_params() -> None:
    """Test execute with different parameter types."""
    conn: sqlean.Connection = sqlean.connect(":memory:")
    
    # Sequence parameters
    conn.execute("SELECT ?", (42,))
    conn.execute("SELECT ?", [42])
    
    # Dict parameters
    conn.execute("SELECT :val", {"val": 42})
    
    conn.close()


def test_create_function() -> None:
    """Test create_function type hints."""
    conn: sqlean.Connection = sqlean.connect(":memory:")
    
    def my_func(x: int) -> int:
        return x * 2
    
    def nullable_func(x: Optional[str]) -> Optional[str]:
        return x
    
    conn.create_function("double", 1, my_func)
    conn.create_function("nullable", 1, nullable_func)
    conn.create_function("determ", 1, my_func, deterministic=True)
    
    conn.close()


def test_create_aggregate() -> None:
    """Test create_aggregate type hints."""
    class MyAggregate:
        def __init__(self) -> None:
            self.value: int = 0
        
        def step(self, x: int) -> None:
            self.value += x
        
        def finalize(self) -> int:
            return self.value
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.create_aggregate("myagg", 1, MyAggregate)
    conn.close()


def test_create_window_function() -> None:
    """Test create_window_function type hints."""
    class MyWindow:
        def __init__(self) -> None:
            self._value: int = 0
        
        def step(self, x: int) -> None:
            self._value += x
        
        def inverse(self, x: int) -> None:
            self._value -= x
        
        def value(self) -> int:
            return self._value
        
        def finalize(self) -> int:
            return self._value
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.create_window_function("mywin", 1, MyWindow)
    conn.close()


def test_create_collation() -> None:
    """Test create_collation type hints."""
    def my_collation(a: str, b: str) -> int:
        return -((a > b) - (a < b))
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.create_collation("mycoll", my_collation)
    # Create and then deregister a collation
    conn.create_collation("nocoll", my_collation)
    conn.create_collation("nocoll", None)
    conn.close()


def test_set_authorizer() -> None:
    """Test set_authorizer type hints."""
    def my_authorizer(
        action: int, arg1: str, arg2: str, dbname: str, source: str
    ) -> int:
        return sqlean.SQLITE_OK
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.set_authorizer(my_authorizer)
    conn.set_authorizer(None)
    conn.close()


def test_set_progress_handler() -> None:
    """Test set_progress_handler type hints."""
    def my_progress() -> int:
        return 0
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.set_progress_handler(my_progress, 100)
    conn.set_progress_handler(None, 100)
    conn.close()


def test_set_trace_callback() -> None:
    """Test set_trace_callback type hints."""
    def my_trace(statement: str) -> None:
        print(statement)
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.set_trace_callback(my_trace)
    conn.set_trace_callback(None)
    conn.close()


def test_set_busy_handler() -> None:
    """Test set_busy_handler type hints."""
    def my_handler(n: int) -> int:
        return 0
    
    conn: sqlean.Connection = sqlean.connect(":memory:")
    conn.set_busy_handler(my_handler)
    conn.set_busy_handler(None)
    conn.close()


def test_date_time_constructors() -> None:
    """Test date/time constructor type hints."""
    from datetime import date, time, datetime
    d: date = sqlean.Date(2024, 1, 15)
    t: time = sqlean.Time(14, 30, 45)
    ts: datetime = sqlean.Timestamp(2024, 1, 15, 14, 30, 45)
    
    d2: date = sqlean.DateFromTicks(0)
    t2: time = sqlean.TimeFromTicks(0)
    ts2: datetime = sqlean.TimestampFromTicks(0)


def test_binary_factory() -> None:
    """Test Binary factory type hints."""
    b: memoryview = sqlean.Binary(b"test")


def test_extensions() -> None:
    """Test extensions type hints."""
    extensions.enable_all()
    extensions.disable_all()
    extensions.enable("uuid", "crypto", "text")
    extensions.disable("uuid")
