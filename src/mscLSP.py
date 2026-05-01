#!/usr/bin/env -S uv run
from __future__ import annotations

# /* script
# requires-python = ">=3.12"
# dependencies = [
#     "uv==*.*",
# ]
# */
# Optional dependency handling (also add to '/* script..' comment, just above)
#   "© 2026 `Phovos` (phovos@outlook.com)":
#     - "Morphological Source Code: MSC&QSD"
#     - https://gitlab.com/morphological/source/code
#     - https://github.com/Morphological-Source-Code
#     - https://reddit.com/r/morphological
# © 2024-2026 https://github.com/Phovos/Morphological-Source-Code
# © 2023-2026 https://github.com/MOONLAPSED/cognosis
try:
    import flask

    USE_FLASK = True
    # if we omit "flask==*.*", or any non-std lib from the '/* script..' comment, then this should always fail
    pass
except ImportError:
    USE_FLASK = False
    coreLSP = False
# Import standard library components
import os
import sys
import ast
import json
import uuid
import time
import logging
import inspect
import hashlib
from socketserver import ThreadingMixIn
from typing import Any, Dict, Callable, TypeVar
from types import ModuleType
from dataclasses import dataclass
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.metadata import distributions
import argparse
import base64
import logging.config
import logging.handlers
import re
import subprocess
import threading
import types as py_types
from dataclasses import field, fields
from enum import Enum, auto
from typing import (
    List,
    Optional,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    final,
)

# ---------------------------------------------------------------------------
# Dynamic module creation
# ---------------------------------------------------------------------------
"""`importlib.metadata` is part of Python's standard library (since 3.8) and is used to access package metadata,
including entry points, version info, and other package-specific data that resides in `.dist-info`."""
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Add a NullHandler by default
for dist in distributions():
    print(f"Package: {dist.metadata['Name']}, Version: {dist.metadata['Version']}")
"""This provides a way to dynamically generate modules and inject code into them at runtime. This is useful for creating a
module from a source code string or AST and then executing the module in the runtime. Runtime module (main)
is the module that the source code is injected into."""


def create_module(
    module_name: str, module_code: str, main_module_path: str | None = None
) -> Optional[ModuleType]:
    """Dynamically create a module and inject code into it.

    Warning: this executes arbitrary code.
    """
    dynamic_module = ModuleType(module_name)
    dynamic_module.__file__ = main_module_path or "runtime_generated"
    dynamic_module.__package__ = module_name.rpartition(".")[0]
    dynamic_module.__path__ = None
    dynamic_module.__doc__ = f"Dynamically generated module: {module_name}"

    try:
        sys.modules[module_name] = dynamic_module
        exec(module_code, dynamic_module.__dict__)
        logger.info(
            "Created dynamic module", extra={"context": {"module": module_name}}
        )
        return dynamic_module
    except Exception:
        logger.error(
            "Failed to create dynamic module",
            exc_info=True,
            extra={"context": {"module": module_name}},
        )
        sys.modules.pop(module_name, None)
        return None


__description__ = "Morphological Analysis Engine: stdlib-only static analysis with HTTP/RPC and LSP bridging"
# __man__ = """ ...
"""
mscModule.py Morphological Analysis Module
=================================
Stdlib-only orchestration layer for source validation, static analysis,
structured logging, HTTP/JSON RPC, and optional LSP-sidecar bridging.

This module is designed to be import-safe:
- no optional dependency assumptions
- no hidden global mutation beyond a NullHandler on the module logger

© 2023-2026 Phovos / MOONLAPSED
"""
__version__ = "0.6.90"

# ---------------------------------------------------------------------------
# Logging infrastructure
# ---------------------------------------------------------------------------


class JsonLogFormatter(logging.Formatter):
    """Formats log records as JSON for machine parsing."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "source": record.name,
            "correlation_id": getattr(record, "correlation_id", "SYSTEM"),
            "context": getattr(record, "context", {}),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


class ContextualLogger(logging.LoggerAdapter):
    """Injects a correlation identifier and optional context into every record."""

    def process(self, msg: str, kwargs: Dict[str, Any]):
        extras = dict(kwargs.get("extra", {}))
        extras.setdefault("correlation_id", self.extra.get("correlation_id", "SYSTEM"))
        extras.setdefault("context", self.extra.get("context", {}))
        kwargs["extra"] = extras
        return f"[{extras['correlation_id']}] {msg}", kwargs


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "morphological.log",
    level: int = logging.INFO,
    json_format: bool = True,
) -> logging.Logger:
    """Configure the process logging system and return a named logger."""
    logs_path = Path(log_dir)
    logs_path.mkdir(parents=True, exist_ok=True)
    log_filepath = logs_path / log_file

    formatter_class = JsonLogFormatter if json_format else logging.Formatter
    format_str = (
        "% (message)s"
        if json_format
        else "[%(levelname)s]%(asctime)s||%(name)s: %(message)s"
    )
    if json_format:
        format_str = "%(message)s"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": formatter_class,
                "format": format_str,
                "datefmt": "%Y-%m-%d~%H:%M:%S%z",
            }
        },
        "handlers": {
            "console": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "level": level,
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_filepath),
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 10,
            },
        },
        "root": {"level": level, "handlers": ["console", "file"]},
    }

    logging.config.dictConfig(logging_config)
    return logging.getLogger("MorphologicalEngine")


def get_logger(
    name: str | None = None, correlation_id: str = "SYSTEM"
) -> ContextualLogger:
    """Return a contextual logger for a component or caller module."""
    if name is None:
        frame = inspect.currentframe()
        caller = frame.f_back if frame and frame.f_back else None
        name = caller.f_globals.get("__name__", "unknown") if caller else "unknown"
    return ContextualLogger(logging.getLogger(name), {"correlation_id": correlation_id})


logger = logging.getLogger("MorphologicalEngine")
logger.addHandler(logging.NullHandler())

# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class MorphologicalError(Exception):
    """Base exception for all morphological engine errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.status_code = status_code
        super().__init__(message)


class AnalyzerError(MorphologicalError):
    """Base for analysis-specific errors."""


class ConfigurationError(AnalyzerError):
    """Invalid or insecure configuration."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class SourceError(AnalyzerError):
    """Issues with source files."""


class SourceNotFoundError(SourceError):
    """Source file does not exist."""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class SourcePermissionError(SourceError):
    """Source file access denied."""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class SourceSizeExceededError(SourceError):
    """Source file too large."""

    def __init__(self, message: str):
        super().__init__(message, status_code=413)


class ParsingError(AnalyzerError):
    """Invalid Python syntax."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InputValidationError(MorphologicalError):
    """Hostile or malformed input."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class SecurityViolationError(MorphologicalError):
    """Security policy violation."""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class ResourceLimitExceededError(MorphologicalError):
    """Resource limits exceeded."""

    def __init__(self, message: str):
        super().__init__(message, status_code=413)


class LspError(AnalyzerError):
    """LSP-specific errors."""


EngineError = MorphologicalError  # Compatibility alias (fallback)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
T = TypeVar("T")
C = TypeVar("C", bound=Callable[..., Any])


class QuantumState(Enum):
    """Quantum-inspired state representation."""

    SUPERPOSITION = auto()
    ENTANGLED = auto()
    COLLAPSED = auto()
    DECOHERENT = auto()


class RuntimeMode(Enum):
    """Runtime execution mode."""

    SUBINTERPRETER = auto()
    THREADED = auto()
    SEQUENTIAL = auto()


class Mutability(Enum):
    """Data mutability mode."""

    IMMUTABLE = auto()
    MUTABLE = auto()
    QUEINIC = auto()


class SerializationFormat(Enum):
    """Supported serialization formats."""

    JSON = "json"
    PICKLE = "pickle"
    REPR = "repr"
    CPYTHON = "python"  # mind the mangle


# ---------------------------------------------------------------------------
# BaseModel system
# ---------------------------------------------------------------------------


def _matches_type(value: Any, tp: Any) -> bool:
    """Check whether a value conforms to a type annotation."""
    if tp is Any:
        return True

    origin = get_origin(tp)
    if origin in (Union, getattr(py_types, "UnionType", object())):
        return any(_matches_type(value, arg) for arg in get_args(tp))

    if origin is list:
        if not isinstance(value, list):
            return False
        args = get_args(tp)
        if not args:
            return True
        return all(_matches_type(item, args[0]) for item in value)

    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        args = get_args(tp)
        if not args:
            return True
        if len(args) == 2 and args[1] is Ellipsis:
            return all(_matches_type(item, args[0]) for item in value)
        return len(value) == len(args) and all(
            _matches_type(item, arg) for item, arg in zip(value, args, strict=False)
        )

    if origin is dict:
        if not isinstance(value, dict):
            return False
        args = get_args(tp)
        if len(args) != 2:
            return True
        kt, vt = args
        return all(
            _matches_type(k, kt) and _matches_type(v, vt) for k, v in value.items()
        )

    if origin is set:
        if not isinstance(value, set):
            return False
        args = get_args(tp)
        if not args:
            return True
        return all(_matches_type(item, args[0]) for item in value)

    if inspect.isclass(tp):
        return isinstance(value, tp)

    return True


def _coerce(raw: Any, tp: Any) -> Any:
    """Coerce a raw value into a target type when reasonable."""
    if tp is Any:
        return raw

    origin = get_origin(tp)

    if origin in (Union, getattr(py_types, "UnionType", object())):
        for arg_type in get_args(tp):
            if arg_type is type(None) and raw is None:
                return None
            try:
                return _coerce(raw, arg_type)
            except TypeError, ValueError:
                continue
        raise TypeError(f"Cannot coerce {raw!r} to {tp}")

    if origin is list:
        if not isinstance(raw, list):
            raise TypeError(f"Expected list, got {type(raw).__name__}")
        elem_tp = get_args(tp)[0] if get_args(tp) else Any
        return [_coerce(item, elem_tp) for item in raw]

    if origin is tuple:
        if not isinstance(raw, (list, tuple)):
            raise TypeError(f"Expected tuple/list, got {type(raw).__name__}")
        args = get_args(tp)
        if not args:
            return tuple(raw)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(_coerce(item, args[0]) for item in raw)
        return tuple(_coerce(item, arg) for item, arg in zip(raw, args, strict=False))

    if origin is dict:
        if not isinstance(raw, dict):
            raise TypeError(f"Expected dict, got {type(raw).__name__}")
        args = get_args(tp)
        if len(args) == 2:
            kt, vt = args
            return {_coerce(k, kt): _coerce(v, vt) for k, v in raw.items()}
        return raw

    if inspect.isclass(tp) and issubclass(tp, BaseModel):
        if isinstance(raw, dict):
            return tp.from_dict(raw)
        if isinstance(raw, tp):
            return raw

    if inspect.isclass(tp) and issubclass(tp, Path):
        if isinstance(raw, Path):
            return raw
        if isinstance(raw, str):
            return Path(raw)

    if inspect.isclass(tp) and issubclass(tp, uuid.UUID):
        if isinstance(raw, uuid.UUID):
            return raw
        if isinstance(raw, str):
            return uuid.UUID(raw)

    if tp is bytes and isinstance(raw, str):
        return raw.encode("utf-8")

    if inspect.isclass(tp) and issubclass(tp, Enum):
        if isinstance(raw, tp):
            return raw
        try:
            return tp(raw)
        except Exception:
            return tp[str(raw)]

    return raw


def _uncoerce(value: Any) -> Any:
    """Convert values into JSON-serializable structures."""
    if isinstance(value, BaseModel):
        return value.to_dict()
    if isinstance(value, list):
        return [_uncoerce(v) for v in value]
    if isinstance(value, tuple):
        return [_uncoerce(v) for v in value]
    if isinstance(value, dict):
        return {k: _uncoerce(v) for k, v in value.items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


@dataclass(frozen=True)
class BaseModel:
    """Foundation for all data models with validation and serialization."""

    def __post_init__(self):
        annotations = get_type_hints(type(self))
        for field_def in fields(self):
            if field_def.name.startswith("_") or field_def.name not in annotations:
                continue
            value = getattr(self, field_def.name)
            expected_type = annotations[field_def.name]
            if not _matches_type(value, expected_type):
                raise TypeError(
                    f"{type(self).__name__}.{field_def.name}: expected {expected_type}, got {type(value).__name__}"
                )
        validate = getattr(self, "_validate_model", None)
        if callable(validate):
            validate()

    def _validate_model(self):
        """Override for model-level validation."""
        return None

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data).__name__}")

        field_names = {f.name for f in fields(cls)}
        init_data = {k: v for k, v in data.items() if k in field_names}
        field_types = get_type_hints(cls)

        for field_name, field_type in field_types.items():
            if field_name in init_data:
                try:
                    init_data[field_name] = _coerce(init_data[field_name], field_type)
                except (TypeError, ValueError) as e:
                    raise ValueError(f"Failed to coerce {field_name}: {e}") from e

        try:
            return cls(**init_data)
        except TypeError as e:
            raise ValueError(f"Failed to create {cls.__name__}: {e}") from e

    def to_dict(self, exclude_none: bool = False) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if exclude_none and value is None:
                continue
            result[f.name] = _uncoerce(value)
        return result

    def to_json(self, *, indent: int | None = None, sort_keys: bool = False) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            sort_keys=sort_keys,
            separators=(",", ":") if indent is None else None,
            ensure_ascii=False,
        )

    @classmethod
    def from_json(cls: Type[T], data: str | bytes) -> T:
        if isinstance(data, (bytes, bytearray)):
            data = data.decode("utf-8")
        return cls.from_dict(json.loads(data))

    def fingerprint(self) -> str:
        content = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Configuration models
# ---------------------------------------------------------------------------


@final
@dataclass(frozen=True)
class AnalyzerConfig(BaseModel):
    """Immutable configuration for the analysis engine."""

    allowed_source_roots: Tuple[Path, ...]
    max_file_size_bytes: int = 1 * 1024 * 1024
    max_request_body_size: int = 10 * 1024 * 1024
    source_encoding: str = "utf-8"
    allowed_extensions: Tuple[str, ...] = (".py", ".md", ".txt")
    hmac_secret_key: bytes = field(default_factory=lambda: os.urandom(32))

    def _validate_model(self):
        if not self.allowed_source_roots:
            raise ConfigurationError("allowed_source_roots cannot be empty")
        for p in self.allowed_source_roots:
            if not p.is_absolute():
                raise ConfigurationError(f"Path not absolute: {p}")
            if not p.exists() or not p.is_dir():
                raise ConfigurationError(
                    f"Path does not exist or is not a directory: {p}"
                )
        if self.max_file_size_bytes <= 0:
            raise ConfigurationError("max_file_size_bytes must be positive")
        if self.max_request_body_size <= 0:
            raise ConfigurationError("max_request_body_size must be positive")
        if not self.source_encoding:
            raise ConfigurationError("source_encoding cannot be empty")
        if not self.allowed_extensions:
            raise ConfigurationError("allowed_extensions cannot be empty")
        for ext in self.allowed_extensions:
            if not ext.startswith("."):
                raise ConfigurationError(f"Invalid extension: {ext}")
        if (
            not isinstance(self.hmac_secret_key, (bytes, bytearray))
            or not self.hmac_secret_key
        ):
            raise ConfigurationError("hmac_secret_key must be non-empty bytes")


@dataclass
class RuntimeConfig:
    """Configuration for runtime execution."""

    mode: RuntimeMode = RuntimeMode.THREADED
    max_workers: int = 4
    shared_memory_size: int = 8192

    def __post_init__(self):
        if self.mode == RuntimeMode.SUBINTERPRETER and not HAS_INTERPRETERS:
            logger.warning(
                "Sub-interpreters not available; falling back to THREADED mode"
            )
            self.mode = RuntimeMode.THREADED
        if self.max_workers <= 0:
            raise ConfigurationError("max_workers must be positive")
        if self.shared_memory_size <= 0:
            raise ConfigurationError("shared_memory_size must be positive")


# ---------------------------------------------------------------------------
# DTOs and result models
# ---------------------------------------------------------------------------


@final
@dataclass(frozen=True)
class InputArtifact(BaseModel):
    """Validated input artifact."""

    correlation_id: str
    source_path: str
    content: str
    content_hash_sha256: str
    size_bytes: int

    def __post_init__(self):
        super().__post_init__()
        actual_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if self.content_hash_sha256 != actual_hash:
            raise SecurityViolationError(
                "Content hash mismatch during artifact creation."
            )
        if self.size_bytes != len(self.content.encode("utf-8")):
            raise SecurityViolationError(
                "size_bytes mismatch during artifact creation."
            )


@final
@dataclass(frozen=True)
class SourceRequest(BaseModel):
    """Immutable analysis request."""

    source_path: Path
    request_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if isinstance(self.source_path, str):
            object.__setattr__(self, "source_path", Path(self.source_path))
        super().__post_init__()


@final
@dataclass(frozen=True)
class AnalysisMetadata(BaseModel):
    """Metadata for analysis results."""

    request_id: uuid.UUID
    source_path: Path
    source_hash_sha256: str
    analysis_timestamp_utc: float
    engine_version: str = "1.0.0"

    def __post_init__(self):
        if isinstance(self.source_path, str):
            object.__setattr__(self, "source_path", Path(self.source_path))
        super().__post_init__()


@final
@dataclass(frozen=True)
class SemanticGraph(BaseModel):
    """Analysis result with semantic information."""

    source_artifact_hash: str
    processed_at_unix_ts: float
    engine_version: str
    graph_data: Dict[str, Any]
    signature_hmac_sha256: str


@final
@dataclass(frozen=True)
class AnalysisResult(BaseModel):
    """Complete analysis result with metadata."""

    metadata: AnalysisMetadata
    semantic_graph: Dict[str, Any]

    def to_markdown(self) -> str:
        lines: List[str] = []
        meta = self.metadata
        sg = self.semantic_graph
        lines.append(f"# Python Module: `{meta.source_path.name}`")
        lines.append(f"- **Hash**: `{meta.source_hash_sha256[:16]}`")
        lines.append(f"- **Analyzed**: `{time.ctime(meta.analysis_timestamp_utc)}`")
        lines.append("")
        lines.append("## Functions")
        for f in sg.get("functions", []):
            args = ", ".join(f.get("args", []))
            decs = (
                f" ⟶ {', '.join(f.get('decorators', []))}"
                if f.get("decorators")
                else ""
            )
            lines.append(f"- `{f.get('name')}({args})` (line {f.get('lineno')}){decs}")
        lines.append("")
        lines.append("## Classes")
        for c in sg.get("classes", []):
            bases = f" → {', '.join(c.get('bases', []))}" if c.get("bases") else ""
            lines.append(f"- `{c.get('name')}`{bases} (line {c.get('lineno')})")
        lines.append("")
        lines.append("## Imports")
        for imp in sg.get("imports", []):
            if "name" in imp:
                lines.append(f"- `from {imp.get('module')} import {imp.get('name')}`")
            else:
                lines.append(f"- `import {imp.get('module')}`")
        lines.append("")
        lines.append(f"## Complexity Score: `{sg.get('complexity', 0)}`")
        return "\n".join(lines)


@final
@dataclass(frozen=True)
class MarkdownSection(BaseModel):
    title: str
    level: int
    start_line: int
    end_line: int
    parent_section: Optional[str] = None


@final
@dataclass(frozen=True)
class MarkdownGraph(BaseModel):
    sections: List[MarkdownSection]
    links: List[Dict[str, Any]]
    backlinks: List[str]
    path_hierarchy: List[str]


@final
@dataclass(frozen=True)
class LspMessage(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Static analysis engine
# ---------------------------------------------------------------------------


class SemanticVisitor(ast.NodeVisitor):
    """AST visitor for Python semantic analysis."""

    def __init__(self):
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []
        self.imports: List[Dict[str, Any]] = []
        self.variables: List[Dict[str, Any]] = []
        self.complexity_score = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(
            {
                "name": node.name,
                "lineno": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "decorators": [ast.unparse(d) for d in node.decorator_list],
            }
        )
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.functions.append(
            {
                "name": node.name,
                "lineno": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "decorators": [ast.unparse(d) for d in node.decorator_list],
                "async": True,
            }
        )
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.append(
            {
                "name": node.name,
                "lineno": node.lineno,
                "bases": [ast.unparse(b) for b in node.bases],
                "decorators": [ast.unparse(d) for d in node.decorator_list],
            }
        )
        self.complexity_score += 2
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(
                {"module": alias.name, "alias": alias.asname, "lineno": node.lineno}
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            self.imports.append(
                {
                    "module": node.module,
                    "name": alias.name,
                    "alias": alias.asname,
                    "lineno": node.lineno,
                }
            )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.append({"name": target.id, "lineno": node.lineno})
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self.complexity_score += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        self.complexity_score += len(node.handlers) + 1
        self.generic_visit(node)


class MarkdownVisitor:
    """Lightweight Markdown semantic visitor using stdlib regex and line scanning."""

    HEADER_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
    LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def __init__(self):
        self.sections: List[MarkdownSection] = []
        self.links: List[Dict[str, Any]] = []

    def visit(self, content: str):
        stack: List[Tuple[int, str, int]] = []
        lines = content.splitlines()
        for lineno, line in enumerate(lines, start=1):
            header = self.HEADER_RE.match(line)
            if header:
                level = len(header.group(1))
                title = header.group(2).strip()
                while stack and stack[-1][0] >= level:
                    stack.pop()
                parent = stack[-1][1] if stack else None
                self.sections.append(
                    MarkdownSection(
                        title=title,
                        level=level,
                        start_line=lineno,
                        end_line=lineno,
                        parent_section=parent,
                    )
                )
                stack.append((level, title, len(self.sections) - 1))
            for match in self.LINK_RE.finditer(line):
                self.links.append(
                    {"text": match.group(1), "target": match.group(2), "lineno": lineno}
                )

        # Fill end_line values by walking the section list from left to right.
        for idx, section in enumerate(self.sections):
            end_line = len(lines)
            for next_section in self.sections[idx + 1 :]:
                if next_section.level <= section.level:
                    end_line = next_section.start_line - 1
                    break
            self.sections[idx] = MarkdownSection(
                title=section.title,
                level=section.level,
                start_line=section.start_line,
                end_line=end_line,
                parent_section=section.parent_section,
            )

    def build_graph(self, source_path: Path) -> MarkdownGraph:
        path_hierarchy = [part for part in source_path.parts if part not in (".", "")]
        backlinks = sorted({link["target"] for link in self.links})
        return MarkdownGraph(
            sections=self.sections,
            links=self.links,
            backlinks=backlinks,
            path_hierarchy=path_hierarchy,
        )


class StaticAnalysisEngine:
    """Core static analysis engine for Python and Markdown source code."""

    def __init__(self, config: AnalyzerConfig):
        self._config = config
        self._logger = get_logger(self.__class__.__name__)
        self._logger.info(
            "Engine initialized", extra={"context": {"config": self._config.to_dict()}}
        )

    @property
    def config(self) -> AnalyzerConfig:
        return self._config

    def analyze(self, request: SourceRequest) -> AnalysisResult:
        logger_ = get_logger(self.__class__.__name__, str(request.request_id))
        logger_.info(
            "Analysis started", extra={"context": {"source": str(request.source_path)}}
        )
        start_time = time.time()

        try:
            source_path = request.source_path
            self._validate_source_path(source_path, logger_)
            content, file_hash = self._read_source_content(source_path, logger_)
            semantic_graph = self._build_semantic_graph(source_path, content, logger_)
            metadata = AnalysisMetadata(
                request_id=request.request_id,
                source_path=source_path,
                source_hash_sha256=file_hash,
                analysis_timestamp_utc=time.time(),
            )
            result = AnalysisResult(metadata=metadata, semantic_graph=semantic_graph)
            duration = time.time() - start_time
            logger_.info(
                "Analysis completed",
                extra={"context": {"duration": f"{duration:.4f}s"}},
            )
            return result
        except AnalyzerError:
            logger_.error("Analysis failed", exc_info=True)
            raise
        except Exception as e:
            logger_.critical("Unexpected error", exc_info=True)
            raise AnalyzerError(f"Unexpected internal error: {e}") from e

    def process_source_file(
        self, path: str, content: bytes, correlation_id: str
    ) -> SemanticGraph:
        """Analyze supplied content against the given path."""
        source_path = Path(path)
        logger_ = get_logger(self.__class__.__name__, correlation_id)
        self._validate_source_path(source_path, logger_)
        text, file_hash = self._validate_content(content, correlation_id)
        input_artifact = InputArtifact(
            correlation_id=correlation_id,
            source_path=str(source_path),
            content=text,
            content_hash_sha256=file_hash,
            size_bytes=len(content),
        )
        return self._analyze_artifact(input_artifact, source_path, correlation_id)

    def _analyze_artifact(
        self, input_artifact: InputArtifact, source_path: Path, correlation_id: str
    ) -> SemanticGraph:
        logger_ = get_logger(self.__class__.__name__, correlation_id)
        start_time = time.time()
        semantic_graph = self._build_semantic_graph(
            source_path, input_artifact.content, logger_
        )
        output_payload = {
            "source_artifact_hash": input_artifact.content_hash_sha256,
            "processed_at_unix_ts": time.time(),
            "engine_version": __version__,
            "graph_data": semantic_graph,
        }
        payload_bytes = json.dumps(
            output_payload, sort_keys=True, ensure_ascii=False
        ).encode("utf-8")
        signature = hashlib.pbkdf2_hmac(
            "sha256", payload_bytes, self._config.hmac_secret_key, 1, dklen=32
        ).hex()
        elapsed = (time.time() - start_time) * 1000
        logger_.info(
            "Semantic graph created and signed",
            extra={"context": {"analysis_duration_ms": round(elapsed, 2)}},
        )
        return SemanticGraph(**output_payload, signature_hmac_sha256=signature)

    def _validate_source_path(self, source_path: Path, logger_: ContextualLogger):
        logger_.info("Validating source path")
        try:
            real_path = source_path.resolve(strict=True)
        except FileNotFoundError as e:
            raise SourceNotFoundError(
                f"Source file does not exist: {source_path}"
            ) from e
        if not any(
            real_path.is_relative_to(root) for root in self._config.allowed_source_roots
        ):
            raise SourcePermissionError(f"Path outside allowed roots: {real_path}")
        if real_path.suffix not in self._config.allowed_extensions:
            raise SourceError(f"Unsupported extension: {real_path.suffix}")
        logger_.info(
            "Path validation passed", extra={"context": {"path": str(real_path)}}
        )

    def _read_source_content(
        self, source_path: Path, logger_: ContextualLogger
    ) -> Tuple[str, str]:
        logger_.info("Reading source content")
        if not os.access(source_path, os.R_OK):
            raise SourcePermissionError(f"Read permission denied: {source_path}")
        file_size = source_path.stat().st_size
        if file_size > self._config.max_file_size_bytes:
            raise SourceSizeExceededError(
                f"File size {file_size} exceeds limit of {self._config.max_file_size_bytes}"
            )
        try:
            content = source_path.read_text(encoding=self._config.source_encoding)
            content_bytes = content.encode(self._config.source_encoding)
            file_hash = hashlib.sha256(content_bytes).hexdigest()
            logger_.info(
                "Read source content",
                extra={
                    "context": {"bytes": len(content_bytes), "hash": file_hash[:12]}
                },
            )
            return content, file_hash
        except (OSError, UnicodeDecodeError) as e:
            raise SourceError(f"Failed to read source: {e}") from e

    def _validate_content(self, content: bytes, correlation_id: str) -> Tuple[str, str]:
        logger_ = get_logger(self.__class__.__name__, correlation_id)
        if len(content) > self._config.max_file_size_bytes:
            raise ResourceLimitExceededError(
                f"File size exceeds limit of {self._config.max_file_size_bytes} bytes"
            )
        try:
            decoded_content = content.decode(self._config.source_encoding)
        except UnicodeDecodeError as e:
            raise InputValidationError("File content is not valid UTF-8.") from e
        try:
            ast.parse(decoded_content)
        except SyntaxError as e:
            raise ParsingError(f"Invalid Python syntax: {e}") from e
        file_hash = hashlib.sha256(content).hexdigest()
        logger_.info(
            "Content validated", extra={"context": {"size_bytes": len(content)}}
        )
        return decoded_content, file_hash

    def _build_semantic_graph(
        self, source_path: Path, content: str, logger_: ContextualLogger
    ) -> Dict[str, Any]:
        logger_.info("Building semantic graph")
        suffix = source_path.suffix.lower()
        if suffix in {".md", ".markdown", ".txt"}:
            return self._build_markdown_graph(source_path, content, logger_)
        return self._build_python_graph(content, logger_)

    def _build_python_graph(
        self, content: str, logger_: ContextualLogger
    ) -> Dict[str, Any]:
        tree = ast.parse(content)
        visitor = SemanticVisitor()
        visitor.visit(tree)
        return {
            "ast_dump": ast.dump(tree, indent=2),
            "functions": visitor.functions,
            "classes": visitor.classes,
            "imports": visitor.imports,
            "variables": visitor.variables,
            "complexity": visitor.complexity_score,
        }

    def _build_markdown_graph(
        self, source_path: Path, content: str, logger_: ContextualLogger
    ) -> Dict[str, Any]:
        visitor = MarkdownVisitor()
        visitor.visit(content)
        graph = visitor.build_graph(source_path)
        return {
            "sections": [s.to_dict() for s in graph.sections],
            "links": graph.links,
            "backlinks": graph.backlinks,
            "path_hierarchy": graph.path_hierarchy,
            "complexity": len(graph.sections) + len(graph.links),
        }


# ---------------------------------------------------------------------------
# HTTP RPC server
# ---------------------------------------------------------------------------


class AnalysisRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for analysis RPC endpoints."""

    engine: StaticAnalysisEngine | None = None
    config: AnalyzerConfig | None = None
    logger: ContextualLogger | None = None
    protocol_version = "HTTP/1.1"

    def _send_response(self, status_code: int, content_type: str, body: bytes):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Correlation-ID", getattr(self, "correlation_id", "SYSTEM"))
        self.end_headers()
        self.wfile.write(body)

    def _handle_error(self, e: Exception):
        logger_ = self.logger or get_logger(
            self.__class__.__name__, getattr(self, "correlation_id", "SYSTEM")
        )
        if isinstance(e, MorphologicalError):
            status_code = e.status_code
            message = str(e)
        else:
            status_code = 500
            message = "Internal server error"
            logger_.error("Unhandled exception", exc_info=True)
        body = json.dumps(
            {
                "error": message,
                "correlation_id": getattr(self, "correlation_id", "SYSTEM"),
            }
        ).encode("utf-8")
        self._send_response(status_code, "application/json", body)

    def _read_json_body(self) -> Dict[str, Any]:
        content_len = int(self.headers.get("Content-Length", "0") or 0)
        if self.config and content_len > self.config.max_request_body_size:
            raise ResourceLimitExceededError("Request body too large")
        raw = self.rfile.read(content_len)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise InputValidationError("Request body must be valid JSON") from e
        if not isinstance(data, dict):
            raise InputValidationError("Request body must be a JSON object")
        return data

    def do_POST(self):
        self.correlation_id = self.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        self.logger = get_logger(self.__class__.__name__, self.correlation_id)
        self.logger.info(
            "Request received", extra={"context": {"method": "POST", "path": self.path}}
        )
        try:
            if self.path != "/analyze":
                raise InputValidationError("Endpoint not found. Use POST /analyze")
            data = self._read_json_body()
            path = data.get("path")
            content_b64 = data.get("content_b64")
            if not path or not content_b64:
                raise InputValidationError(
                    "Request body must contain 'path' and 'content_b64'"
                )
            try:
                content_bytes = base64.b64decode(content_b64, validate=True)
            except Exception as e:
                raise InputValidationError("content_b64 is not valid base64") from e
            if not self.engine:
                raise ConfigurationError("Engine not configured")
            result_graph = self.engine.process_source_file(
                path, content_bytes, self.correlation_id
            )
            body = result_graph.to_json(indent=2).encode("utf-8")
            self._send_response(200, "application/json", body)
            self.logger.info("Request processed successfully")
        except Exception as e:
            self._handle_error(e)

    def do_GET(self):
        self.correlation_id = self.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        self.logger = get_logger(self.__class__.__name__, self.correlation_id)
        if self.path == "/health":
            body = json.dumps(
                {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "correlation_id": self.correlation_id,
                    "version": __version__,
                }
            ).encode("utf-8")
            self._send_response(200, "application/json", body)
        else:
            self._handle_error(InputValidationError("Endpoint not found"))

    def log_message(self, format: str, *args):
        # Keep the server quiet; structured logging is handled explicitly.
        return


class ThreadedAnalysisServer(ThreadingHTTPServer, ThreadingMixIn):
    """Threaded HTTP server with dependency injection."""

    daemon_threads = True

    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        engine: StaticAnalysisEngine,
        config: AnalyzerConfig,
        logger_: ContextualLogger | None = None,
    ):
        bound = type("BoundAnalysisRequestHandler", (RequestHandlerClass,), {})
        bound.engine = engine
        bound.config = config
        bound.logger = logger_ or get_logger("AnalysisRequestHandler")
        super().__init__(server_address, bound)


class ThreadedEngineServer(ThreadedAnalysisServer):
    """Compatibility alias for the earlier draft."""


# Experimental compatibility hook; currently a safe alias rather than a true
# subinterpreter socket server implementation, which is not portable enough for
# a stdlib-only module that must remain robust on machines without support.
class SubinterpreterAnalysisServer(ThreadedAnalysisServer):
    pass


# ---------------------------------------------------------------------------
# LSP client (stdio sidecar bridge)
# ---------------------------------------------------------------------------


class LspClient:
    """Stdlib-only JSON-RPC/LSP client for an external sidecar process."""

    def __init__(
        self,
        iwes_path: str = "iwes",
        project_root: Path = Path.cwd(),
        logger_: ContextualLogger | None = None,
    ):
        self.logger = logger_ or get_logger(self.__class__.__name__)
        self.process = subprocess.Popen(
            [iwes_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(project_root),
            bufsize=0,
        )
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stderr_thread.start()
        self.initialize()

    def _read_stderr(self):
        if not self.process.stderr:
            return
        while True:
            line = self.process.stderr.readline()
            if not line:
                break
            try:
                self.logger.info(line.decode("utf-8", errors="replace").rstrip())
            except Exception:
                pass

    def _send_message(self, message: LspMessage):
        if not self.process.stdin:
            raise LspError("LSP stdin is not available")
        content = json.dumps(message.to_dict(), ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(content)}\r\n\r\n".encode("utf-8")
        self.process.stdin.write(header + content)
        self.process.stdin.flush()

    def _read_message(self) -> LspMessage:
        if not self.process.stdout:
            raise LspError("LSP stdout is not available")
        headers: Dict[str, str] = {}
        while True:
            line = self.process.stdout.readline()
            if not line:
                raise LspError("LSP process terminated unexpectedly")
            decoded = line.decode("utf-8", errors="replace").strip()
            if not decoded:
                break
            if ":" in decoded:
                key, value = decoded.split(":", 1)
                headers[key.strip().lower()] = value.strip()
        content_length = int(headers.get("content-length", "0"))
        body = self.process.stdout.read(content_length)
        if body is None:
            raise LspError("Failed to read LSP body")
        return LspMessage.from_dict(json.loads(body.decode("utf-8")))

    def initialize(self):
        init_id = uuid.uuid4().int & ((1 << 31) - 1)
        params = {
            "processId": os.getpid(),
            "rootUri": f"file://{Path.cwd().absolute()}",
            "capabilities": {},
        }
        self._send_message(LspMessage(id=init_id, method="initialize", params=params))
        response = self._read_message()
        if response.error:
            raise LspError(f"Initialize failed: {response.error}")
        self.logger.info("LSP initialized")

    def request(self, method: str, params: Dict[str, Any]) -> Any:
        req_id = uuid.uuid4().int & ((1 << 31) - 1)
        self._send_message(LspMessage(id=req_id, method=method, params=params))
        while True:
            response = self._read_message()
            if response.id == req_id:
                if response.error:
                    raise LspError(f"Request failed: {response.error}")
                return response.result

    def close(self):
        try:
            self._send_message(LspMessage(method="shutdown"))
            _ = self._read_message()
            self._send_message(LspMessage(method="exit"))
        finally:
            self.process.terminate()
            self.process.wait(timeout=5)


# ---------------------------------------------------------------------------
# Demo helpers
# ---------------------------------------------------------------------------


def demo_analysis():
    logger.info("=" * 70)
    logger.info("DEMO: Static Analysis Engine")
    logger.info("=" * 70)
    config = AnalyzerConfig(
        allowed_source_roots=(Path.cwd().resolve(),),
        max_file_size_bytes=10 * 1024 * 1024,
        allowed_extensions=(".py",),
    )
    engine = StaticAnalysisEngine(config)
    test_code = '''\
"""Test module for analysis"""
import os
import sys
from pathlib import Path

class TestClass:
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f"Hello, {self.name}!"

def test_function(x: int, y: int) -> int:
    return x + y
'''
    test_file = Path.cwd() / "test_analysis.py"
    test_file.write_text(test_code, encoding="utf-8")
    try:
        result = engine.analyze(SourceRequest(source_path=test_file))
        logger.info(
            "Analysis completed successfully",
            extra={
                "context": {
                    "functions": len(result.semantic_graph.get("functions", [])),
                    "classes": len(result.semantic_graph.get("classes", [])),
                }
            },
        )
    finally:
        if test_file.exists():
            test_file.unlink()


def demo_dynamic_module():
    logger.info("=" * 70)
    logger.info("DEMO: Dynamic Module Creation")
    logger.info("=" * 70)
    module_code = '''\
import inspect
import ast
import hashlib

def greet():
    return "Hello from dynamically created module!"
'''
    module = create_module("morphological_quine", module_code, __file__)
    if module:
        logger.info(
            "Created module",
            extra={"context": {"module": module.__name__, "file": module.__file__}},
        )


def demo_rpc_client():
    logger.info("=" * 70)
    logger.info("DEMO: RPC Client")
    logger.info("=" * 70)
    test_code = 'def add(a, b):\n    return a + b\n'
    content_b64 = base64.b64encode(test_code.encode("utf-8")).decode("ascii")
    payload = {"path": "test_client.py", "content_b64": content_b64}
    logger.info("RPC request payload", extra={"context": payload})


def demo_integration():
    logger.info("=" * 70)
    logger.info("DEMO: Full Integration")
    logger.info("=" * 70)
    config = AnalyzerConfig(
        allowed_source_roots=(Path.cwd().resolve(),), max_file_size_bytes=1024 * 1024
    )
    engine = StaticAnalysisEngine(config)
    test_file = Path.cwd() / "integration_test.py"
    test_file.write_text(
        """\
class DataProcessor:
    def __init__(self, data):
        self.data = data
    def process(self):
        results = []
        for item in self.data:
            if item > 0:
                results.append(item * 2)
            else:
                results.append(0)
        return results
""",
        encoding="utf-8",
    )
    try:
        result = engine.analyze(SourceRequest(source_path=test_file))
        logger.info(
            "Integration demo result",
            extra={"context": {"fingerprint": result.fingerprint()}},
        )
    finally:
        if test_file.exists():
            test_file.unlink()


# ---------------------------------------------------------------------------
# CLI / main
# ---------------------------------------------------------------------------


def main():
    """Run the server with environment-driven configuration."""
    log_level = getattr(
        logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO
    )
    json_logs = os.environ.get("JSON_LOGS", "1") not in {"0", "false", "False"}
    setup_logging(level=log_level, json_format=json_logs)

    logger.info("=" * 70)
    logger.info("Morphological Analysis Engine Starting")
    logger.info("=" * 70)

    allowed_roots_env = os.environ.get("ALLOWED_ROOTS")
    if allowed_roots_env:
        allowed_roots = [
            Path(p).expanduser().resolve()
            for p in allowed_roots_env.split(os.pathsep)
            if p.strip()
        ]
    else:
        allowed_roots = [Path.cwd().resolve()]

    analyzer_config = AnalyzerConfig(
        allowed_source_roots=tuple(allowed_roots),
        max_file_size_bytes=int(
            os.environ.get("MAX_FILE_SIZE_BYTES", str(1 * 1024 * 1024))
        ),
        max_request_body_size=int(
            os.environ.get("MAX_REQUEST_BODY_SIZE", str(10 * 1024 * 1024))
        ),
        source_encoding=os.environ.get("SOURCE_ENCODING", "utf-8"),
        allowed_extensions=tuple(
            ext.strip()
            for ext in os.environ.get("ALLOWED_EXTENSIONS", ".py,.md,.txt").split(",")
            if ext.strip()
        ),
    )

    engine = StaticAnalysisEngine(analyzer_config)
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8698"))
    server = ThreadedAnalysisServer(
        (host, port),
        AnalysisRequestHandler,
        engine,
        analyzer_config,
        get_logger("AnalysisServer"),
    )

    logger.info("Server listening", extra={"context": {"host": host, "port": port}})
    logger.info("Endpoints", extra={"context": {"POST": "/analyze", "GET": "/health"}})

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
        server.shutdown()
        server.server_close()
        logger.info("Server stopped")


def cli():
    """Command-line interface for the engine."""
    parser = argparse.ArgumentParser(
        description="Morphological Analysis Engine - Static analysis with RPC interface"
    )
    parser.add_argument(
        "command", choices=["serve", "analyze", "demo"], help="Command to execute"
    )
    parser.add_argument(
        "--file", type=Path, help="File to analyze (for analyze command)"
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="Server host (for serve command)"
    )
    parser.add_argument(
        "--port", type=int, default=8698, help="Server port (for serve command)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level",
    )
    parser.add_argument(
        "--json-logs", action="store_true", help="Output logs in JSON format"
    )
    args = parser.parse_args()

    global logger
    log_level = getattr(logging, args.log_level)
    logger = setup_logging(level=log_level, json_format=args.json_logs)

    if args.command == "serve":
        os.environ["HOST"] = args.host
        os.environ["PORT"] = str(args.port)
        main()
        return

    if args.command == "analyze":
        if not args.file:
            parser.error("--file required for analyze command")
        config = AnalyzerConfig(
            allowed_source_roots=(args.file.parent.resolve(),),
            max_file_size_bytes=10 * 1024 * 1024,
            allowed_extensions=(args.file.suffix or ".py",),
        )
        engine = StaticAnalysisEngine(config)
        result = engine.analyze(SourceRequest(source_path=args.file))
        print(result.to_json(indent=2))
        return

    if args.command == "demo":
        demo_analysis()
        demo_dynamic_module()
        demo_rpc_client()
        demo_integration()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Core classes
    "StaticAnalysisEngine",
    "SemanticVisitor",
    "MarkdownVisitor",
    # Data models
    "SourceRequest",
    "AnalysisMetadata",
    "AnalysisResult",
    "SemanticGraph",
    "MarkdownSection",
    "MarkdownGraph",
    "LspMessage",
    "InputArtifact",
    # Configuration
    "AnalyzerConfig",
    "RuntimeConfig",
    # Enums
    "QuantumState",
    "RuntimeMode",
    "Mutability",
    "SerializationFormat",
    # Exceptions
    "MorphologicalError",
    "EngineError",
    "AnalyzerError",
    "ConfigurationError",
    "SourceError",
    "SourceNotFoundError",
    "SourcePermissionError",
    "SourceSizeExceededError",
    "ParsingError",
    "InputValidationError",
    "SecurityViolationError",
    "ResourceLimitExceededError",
    "LspError",
    # Utilities
    "create_module",
    "setup_logging",
    "get_logger",
    # Server
    "ThreadedAnalysisServer",
    "ThreadedEngineServer",
    "SubinterpreterAnalysisServer",
    "AnalysisRequestHandler",
    # Base
    "BaseModel",
    "ContextualLogger",
    # LSP
    "LspClient",
    # Entrypoints
    "main",
    "cli",
    # Demos
    "demo_analysis",
    "demo_dynamic_module",
    "demo_rpc_client",
    "demo_integration",
]


HAS_INTERPRETERS = False
try:
    from concurrent.futures import InterpreterPoolExecutor  # type: ignore

    HAS_INTERPRETERS = True
except Exception:
    InterpreterPoolExecutor = None  # type: ignore


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        main()
