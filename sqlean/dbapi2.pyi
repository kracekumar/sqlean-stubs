"""Type hints for sqlean.dbapi2 - DB-API 2.0 interface for SQLite."""

from typing import (
    Any,
    Callable,
    Optional,
    Union,
    List,
    Tuple,
    Dict,
    Iterator,
    Sequence,
    TypeVar,
    Type,
    Literal,
    overload,
    Protocol,
    NamedTuple,
)
from datetime import date, datetime, time
import collections.abc

# DB-API module constants
paramstyle: Literal["qmark"]
threadsafety: Literal[1]
apilevel: Literal["2.0"]

# Version information
version: str
sqlite_version: str
version_info: Tuple[int, int, int]
sqlite_version_info: Tuple[int, int, int]

# Type aliases
_SQLiteValue = Union[str, int, float, bytes, None]
_SQLiteParam = Union[str, int, float, bytes, None, memoryview]
_Parameters = Union[Sequence[_SQLiteParam], Dict[str, _SQLiteParam]]
_RowFactory = Callable[["Cursor", Tuple[_SQLiteValue, ...]], Any]

T = TypeVar("T")

# Date/time constructors
def Date(year: int, month: int, day: int) -> date: ...
def Time(hour: int, minute: int, second: int) -> time: ...
def Timestamp(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> datetime: ...
def DateFromTicks(ticks: float) -> date: ...
def TimeFromTicks(ticks: float) -> time: ...
def TimestampFromTicks(ticks: float) -> datetime: ...

# Type converters
Binary = memoryview

class OptimizedUnicode:
    """Text factory that optimizes between str and bytes."""
    def __call__(self, data: bytes) -> Union[str, bytes]: ...

# Exception hierarchy
class Warning(Exception):
    """Base class for warnings."""
    pass

class Error(Exception):
    """Base class for all exceptions."""
    pass

class InterfaceError(Error):
    """Interface error."""
    pass

class DatabaseError(Error):
    """Database error."""
    pass

class DataError(DatabaseError):
    """Data error."""
    pass

class OperationalError(DatabaseError):
    """Operational error."""
    pass

class IntegrityError(DatabaseError):
    """Integrity error."""
    pass

class InternalError(DatabaseError):
    """Internal error."""
    pass

class ProgrammingError(DatabaseError):
    """Programming error."""
    pass

class NotSupportedError(DatabaseError):
    """Not supported error."""
    pass

# Authorization and progress callback constants
SQLITE_OK: int
SQLITE_DENY: int
SQLITE_IGNORE: int
SQLITE_CREATE_INDEX: int
SQLITE_CREATE_TABLE: int
SQLITE_CREATE_TEMP_INDEX: int
SQLITE_CREATE_TEMP_TABLE: int
SQLITE_CREATE_TEMP_TRIGGER: int
SQLITE_CREATE_TEMP_VIEW: int
SQLITE_CREATE_TRIGGER: int
SQLITE_CREATE_VIEW: int
SQLITE_DELETE: int
SQLITE_DROP_INDEX: int
SQLITE_DROP_TABLE: int
SQLITE_DROP_TEMP_INDEX: int
SQLITE_DROP_TEMP_TABLE: int
SQLITE_DROP_TEMP_TRIGGER: int
SQLITE_DROP_TEMP_VIEW: int
SQLITE_DROP_TRIGGER: int
SQLITE_DROP_VIEW: int
SQLITE_INSERT: int
SQLITE_PRAGMA: int
SQLITE_READ: int
SQLITE_SELECT: int
SQLITE_TRANSACTION: int
SQLITE_UPDATE: int
SQLITE_ATTACH: int
SQLITE_DETACH: int
SQLITE_REINDEX: int
SQLITE_ANALYZE: int
SQLITE_CREATE_VTABLE: int
SQLITE_DROP_VTABLE: int
SQLITE_FUNCTION: int
SQLITE_SAVEPOINT: int
SQLITE_RECURSIVE: int

# Adapter/converter registration
def register_adapter(type_: Type[Any], adapter: Callable[[Any], _SQLiteValue]) -> None:
    """Register an adapter for a custom type."""
    ...

def register_converter(
    typename: str, converter: Callable[[bytes], Any]
) -> None:
    """Register a converter for a custom type."""
    ...

class Row:
    """Represents a row from a database query result."""
    
    def __init__(self, cursor: Cursor, data: Tuple[_SQLiteValue, ...]) -> None: ...
    
    @overload
    def __getitem__(self, key: int) -> _SQLiteValue: ...
    @overload
    def __getitem__(self, key: str) -> _SQLiteValue: ...
    @overload
    def __getitem__(self, key: slice) -> Tuple[_SQLiteValue, ...]: ...
    
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_SQLiteValue]: ...
    def __contains__(self, item: Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __reversed__(self) -> Iterator[_SQLiteValue]: ...
    
    def keys(self) -> List[str]: ...

class Cursor:
    """Database cursor for executing SQL queries."""
    
    connection: Connection
    description: Optional[List[Tuple[str, Optional[str], None, None, None, None, Optional[int]]]]
    rowcount: int
    lastrowid: int
    arraysize: int
    
    def __init__(self, connection: Connection) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __next__(self) -> Any: ...
    
    @overload
    def execute(
        self, sql: str
    ) -> Cursor: ...
    @overload
    def execute(
        self, sql: str, parameters: Sequence[_SQLiteParam]
    ) -> Cursor: ...
    @overload
    def execute(
        self, sql: str, parameters: Dict[str, _SQLiteParam]
    ) -> Cursor: ...
    
    def executemany(
        self, sql: str, parameters: Sequence[Sequence[_SQLiteParam]]
    ) -> Cursor: ...
    
    def executescript(self, sql_script: str) -> Cursor: ...
    
    def fetchone(self) -> Optional[Any]: ...
    def fetchall(self) -> List[Any]: ...
    def fetchmany(self, size: int = 2) -> List[Any]: ...
    
    def close(self) -> None: ...
    def setinputsizes(self, sizes: Sequence[Optional[int]]) -> None: ...
    def setoutputsize(self, size: int, column: Optional[int] = None) -> None: ...

class Connection:
    """Database connection."""
    
    isolation_level: Optional[str]
    in_transaction: bool
    row_factory: Optional[_RowFactory]
    text_factory: Union[Type[str], Type[bytes], Type[bytearray], Callable[[bytes], Any]]
    total_changes: int
    
    def __init__(
        self,
        database: Union[str, bytes],
        timeout: float = 5.0,
        isolation_level: Optional[str] = "DEFERRED",
        check_same_thread: bool = True,
        factory: Type[Connection] = ...,
        cached_statements: int = 100,
        uri: bool = False,
    ) -> None: ...
    
    def __enter__(self) -> Connection: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __next__(self) -> Any: ...
    def __call__(self) -> Cursor: ...
    
    def cursor(
        self,
        factory: Union[Type[Cursor], Callable[[Connection], Cursor], None] = None,
    ) -> Cursor: ...
    
    @overload
    def execute(
        self, sql: str
    ) -> Cursor: ...
    @overload
    def execute(
        self, sql: str, parameters: Sequence[_SQLiteParam]
    ) -> Cursor: ...
    @overload
    def execute(
        self, sql: str, parameters: Dict[str, _SQLiteParam]
    ) -> Cursor: ...
    
    def executemany(
        self, sql: str, parameters: Sequence[Sequence[_SQLiteParam]]
    ) -> Cursor: ...
    
    def executescript(self, sql_script: str) -> Cursor: ...
    
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...
    
    def create_function(
        self,
        name: str,
        num_params: int,
        func: Callable[..., Optional[_SQLiteValue]],
        *,
        deterministic: bool = False,
    ) -> None: ...
    
    def create_aggregate(
        self,
        name: str,
        num_params: int,
        aggregate_class: Type[Any],
    ) -> None: ...
    
    def create_window_function(
        self,
        name: str,
        num_params: int,
        aggregate_class: Type[Any],
    ) -> None: ...
    
    def create_collation(
        self,
        name: str,
        callable: Optional[Callable[[str, str], int]],
    ) -> None: ...
    
    def set_authorizer(
        self,
        authorizer: Optional[Callable[[int, str, str, str, str], int]],
    ) -> None: ...
    
    def set_progress_handler(
        self,
        progress_handler: Optional[Callable[[], int]],
        n: int,
    ) -> None: ...
    
    def set_trace_callback(
        self,
        trace_callback: Optional[Callable[[str], None]],
    ) -> None: ...
    
    def set_busy_handler(
        self,
        handler: Optional[Callable[[int], int]],
    ) -> None: ...
    
    def set_busy_timeout(self, timeout: float) -> None: ...
    
    def interrupt(self) -> None: ...
    
    def open_blob(
        self,
        table: str,
        column: str,
        row: int,
        readonly: bool = False,
    ) -> Blob: ...
    
    def backup(
        self,
        target: Connection,
        *,
        pages: int = -1,
        progress: Optional[Callable[[int, int, int], None]] = None,
        name: str = "main",
        sleep: float = 0.25,
    ) -> None: ...
    
    def enable_load_extension(self, enabled: bool) -> None: ...
    def load_extension(self, path: str, entry_point: Optional[str] = None) -> None: ...
    
    @property
    def schema(self) -> Optional[str]: ...

class Blob:
    """BLOB object for reading and writing."""
    
    def read(self, n: int = -1) -> bytes: ...
    def write(self, data: bytes) -> None: ...
    def close(self) -> None: ...
    def seek(self, offset: int, origin: int = 0) -> int: ...
    def tell(self) -> int: ...
    
    def __enter__(self) -> Blob: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

def connect(
    database: Union[str, bytes],
    timeout: float = 5.0,
    isolation_level: Optional[str] = "DEFERRED",
    check_same_thread: bool = True,
    factory: Type[Connection] = Connection,
    cached_statements: int = 100,
    uri: bool = False,
) -> Connection:
    """Create a connection to a SQLite database."""
    ...
