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
from __future__ import annotations
import sys
import ast
import json
import logging
import argparse
import logging.config
import logging.handlers
import re
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

"""
mscModule.py — Morphological Analysis Engine

Stdlib-first orchestration layer for:
- static analysis (Python + Markdown)
- structured logging
- HTTP/JSON RPC (stdlib)
- dynamic module creation
- plugin/capability system

© 2023-2026 Phovos / MOONLAPSED
"""
# ---------------------------------------------------------------------------
# Versioning / Metadata
# ---------------------------------------------------------------------------
__version__ = "0.0.69"
__description__ = "Morphological Analysis Engine: stdlib-only static analysis with HTTP/RPC and LSP bridging, with optional capability injection. © 2023-2026 Phovos / MOONLAPSED"
__man__ = """
mscModule.py Morphological Analysis Module
=================================
Stdlib-only orchestration layer for source validation, static analysis,
structured logging, HTTP/JSON RPC, and optional LSP-sidecar bridging.

This module is designed to be import-safe:
- no optional dependency assumptions
- no hidden global mutation beyond a NullHandler on the module logger

Design Principles:
------------------
- Import-safe (no side effects)
- Stdlib-only baseline
- Optional dependencies are injected externally (e.g. via uv in main.py)
- Graceful degradation when optional capabilities are absent
- No environment mutation (no installs, no subprocess re-exec)

© 2023-2026 Phovos / MOONLAPSED
"""
IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    from ctypes import windll
    from ctypes import wintypes
    from ctypes.wintypes import HANDLE, DWORD, LPWSTR, LPVOID, BOOL
    from pathlib import PureWindowsPath
    WINDOWS_SANDBOX = Path(PureWindowsPath(r'C:\Users\WDAGUtilityAccount\Desktop'))

# ---------------------------------------------------------------------------
# Logging (import-safe)
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class JsonLogFormatter(logging.Formatter):
    """Structured JSON logging formatter."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "time": self.formatTime(record),
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "context"):
            payload["context"] = record.context

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def setup_logging(json_format: bool = False, level: int = logging.INFO) -> None:
    """Configure logging for the module."""

    handler = logging.StreamHandler()

    if json_format:
        handler.setFormatter(JsonLogFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("[%(levelname)s] %(asctime)s || %(name)s: %(message)s")
        )

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)


# ---------------------------------------------------------------------------
# Capability Injection (Optional Dependencies)
# ---------------------------------------------------------------------------


class Deps:
    """
    Container for optional dependencies.

    These are injected externally (e.g. by main.py after uv resolution).
    """

    flask: Any = None
    pylsp: Any = None


def register_dependency(name: str, module: Any) -> None:
    """Register an optional dependency at runtime."""
    if hasattr(Deps, name):
        setattr(Deps, name, module)
        logger.debug(f"Registered dependency: {name}")


# ---------------------------------------------------------------------------
# Dynamic Module Creation
# ---------------------------------------------------------------------------


def create_module(
    module_name: str, module_code: str, main_module_path: str | None = None
) -> Optional[ModuleType]:
    """
    Dynamically create and execute a module.

    WARNING: Executes arbitrary code.
    """

    dynamic_module = ModuleType(module_name)
    dynamic_module.__file__ = main_module_path or "runtime_generated"
    dynamic_module.__package__ = module_name.rpartition(".")[0]

    try:
        sys.modules[module_name] = dynamic_module
        exec(module_code, dynamic_module.__dict__)

        logger.info(
            "Dynamic module created", extra={"context": {"module": module_name}}
        )
        return dynamic_module

    except Exception:
        logger.error(
            "Dynamic module creation failed",
            exc_info=True,
            extra={"context": {"module": module_name}},
        )
        sys.modules.pop(module_name, None)
        return None

class LogFilter(logging.Filter):
    """Filter that can exclude specific log patterns."""
    def __init__(self, exclude_patterns: List[str] = None):
        super().__init__()
        self.exclude_patterns = exclude_patterns or []
    def filter(self, record):
        message = record.getMessage()
        return not any(pattern in message for pattern in self.exclude_patterns)
class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, error_code: str = "APP_ERROR", status_code: int = 420):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.timestamp = datetime.now()
        super().__init__(message)  # 420
class ConfigError(AppError):
    """Configuration related errors."""
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")  # 500
class SecurityError(AppError):
    """Security related errors."""
    def __init__(self, message: str):
        super().__init__(message, "SECURITY_ERROR")  # 403
class ContentError(AppError):
    """Content related errors."""
    def __init__(self, message: str):
        super().__init__(message, "CONTENT_ERROR")  # 400
class NamespaceError(AppError):
    """Namespace related errors."""
    def __init__(self, message: str):
        super().__init__(message, "NAMESPACE_ERROR") # 404
def error_handler(logger):
    """Decorator for standardized error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AppError as e:
                logger.error(f"{e.__class__.__name__}: {e.message}", 
                             exc_info=True, 
                             extra={'status_code': e.status_code})
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                raise AppError(f"An unexpected error occurred: {str(e)}")
        return wrapper
    return decorator
def retry(max_attempts: int = 3, backoff_factor: float = 1.5, 
          exceptions: tuple = (Exception,), logger: Optional[logging.Logger] = None):
    """Decorator to retry functions with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    wait_time = backoff_factor ** (attempt - 1)
                    if logger:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} for {func.__name__} failed: {e}. "
                            f"Retrying in {wait_time:.2f}s."
                        )
                    if attempt == max_attempts:
                        raise
                    time.sleep(wait_time)
                    attempt += 1
        return wrapper
    return decorator

# ---------------------------------------------------------------------------
# Static Analysis (Python)
# ---------------------------------------------------------------------------


class SemanticVisitor(ast.NodeVisitor):
    """Basic semantic graph extractor."""

    def __init__(self):
        self.functions: List[str] = []
        self.classes: List[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.append(node.name)
        self.generic_visit(node)


class ParsingError(Exception):
    pass


def analyze_python(content: str) -> Dict[str, Any]:
    """Analyze Python source code."""

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        raise ParsingError(f"Invalid Python syntax: {e}") from e

    visitor = SemanticVisitor()
    visitor.visit(tree)

    return {"functions": visitor.functions, "classes": visitor.classes}


# ---------------------------------------------------------------------------
# Static Analysis (Markdown)
# ---------------------------------------------------------------------------


def analyze_markdown(content: str) -> Dict[str, Any]:
    """Extract headings and structure from Markdown."""

    headings = re.findall(r"^(#+)\s+(.*)", content, re.MULTILINE)

    return {"headings": [{"level": len(h[0]), "text": h[1]} for h in headings]}


# ---------------------------------------------------------------------------
# HTTP Server (stdlib)
# ---------------------------------------------------------------------------


class RequestHandler(BaseHTTPRequestHandler):
    """Minimal JSON RPC handler."""

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
            result = self.handle_request(data)
            self._send_json(200, result)

        except Exception as e:
            logger.exception("Request failed")
            self._send_json(500, {"error": str(e)})

    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        action = data.get("action")
        content = data.get("content", "")

        if action == "analyze_python":
            return analyze_python(content)

        if action == "analyze_markdown":
            return analyze_markdown(content)

        return {"error": "Unknown action"}

    def _send_json(self, code: int, payload: Dict[str, Any]):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))


class ThreadedHTTPServer(ThreadingHTTPServer, ThreadingMixIn):
    daemon_threads = True


def run_server(host: str = "127.0.0.1", port: int = 8080):
    server = ThreadedHTTPServer((host, port), RequestHandler)
    logger.info(f"Server running at http://{host}:{port}")
    server.serve_forever()


# ---------------------------------------------------------------------------
# Plugin System (Capability-Based)
# ---------------------------------------------------------------------------


class Plugin:
    """Base plugin interface."""

    name: str = "base"

    def setup(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError


def load_plugins() -> Dict[str, Plugin]:
    """Load plugins based on available dependencies."""

    plugins: Dict[str, Plugin] = {}

    if Deps.flask:

        class FlaskPlugin(Plugin):
            name = "flask"

        plugins["flask"] = FlaskPlugin()

    return plugins


# ---------------------------------------------------------------------------
# CLI (stdlib-only fallback)
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--analyze", type=str)

    args = parser.parse_args()

    setup_logging()

    if args.serve:
        run_server()
        return

    if args.analyze:
        path = Path(args.analyze)
        content = path.read_text()

        if path.suffix == ".py":
            print(json.dumps(analyze_python(content), indent=2))
        else:
            print(json.dumps(analyze_markdown(content), indent=2))


if __name__ == "__main__":
    main()
