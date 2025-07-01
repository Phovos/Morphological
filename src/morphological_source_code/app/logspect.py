from __future__ import annotations
import logging
import logging.config
from pathlib import Path
import inspect
import sys
from types import ModuleType
from importlib.metadata import distributions
"""`importlib.metadata` is part of Python's standard library (since 3.8) and is used to access package metadata,
including entry points, version info, and other package-specific data that resides in `.dist-info`."""
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Add a NullHandler by default
for dist in distributions():
    print(
        f"Package: {dist.metadata['Name']}, Version: {dist.metadata['Version']}")
"""This provides a way to dynamically generate modules and inject code into them at runtime. This is useful for creating a
module from a source code string or AST and then executing the module in the runtime. Runtime module (main)
is the module that the source code is injected into."""


def create_module(module_name: str, module_code: str, main_module_path: str) -> ModuleType | None:
    """
    Dynamically creates a module with the specified name, injects code into it,
    and adds it to sys.modules.

    Args:
        module_name (str): Name of the module to create.
        module_code (str): Source code to inject into the module.
        main_module_path (str): File path of the main module.

    Returns:
        ModuleType | None: The dynamically created module, or None if an error occurs.
    """
    dynamic_module = ModuleType(module_name)
    dynamic_module.__file__ = main_module_path or "runtime_generated"
    dynamic_module.__package__ = module_name
    dynamic_module.__path__ = None
    dynamic_module.__doc__ = None
    try:
        exec(module_code, dynamic_module.__dict__)
        sys.modules[module_name] = dynamic_module
        return dynamic_module
    except Exception as e:
        print(f"Error injecting code into module {module_name}: {e}")
        return None


def setup_logging(log_dir="logs", log_file="app.log", level=logging.INFO):
    """Sets up logging configuration and returns a logger for the calling module."""
    logs_path = Path(log_dir)
    logs_path.mkdir(parents=True, exist_ok=True)
    log_filepath = logs_path / log_file
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': level,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(log_filepath),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            },
        },
        'loggers': {
            __name__: {
                'level': level,
                'handlers': ['console', 'file'],
                'propagate': False
            }
        },
        'root': {
            'level': level,
            'handlers': ['console', 'file']
        }
    }
    logging.config.dictConfig(logging_config)
    frame = inspect.currentframe().f_back    # Get the name of the calling module
    module_name = frame.f_globals['__name__']
    return logging.getLogger(module_name)


# Example usage
module_name = "quine"
module_code = """
def greet():
    print("Hello from the Morphological Source Code module! This is Replicator-code ('Quine-like behavior')!")
"""
main_module_path = getattr(
    sys.modules['__main__'], '__file__', 'runtime_generated')

dynamic_module = create_module(module_name, module_code, main_module_path)
if dynamic_module:
    sys.exit(dynamic_module.greet())
