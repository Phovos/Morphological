#!/usr/bin/env python3
# scripts/app_bridge.py
import sys
import json
import textwrap
from types import ModuleType
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class ContentModule:
    """Represents a content module with metadata and wrapped content.
    'content' is non-python source code and multi-media; the knowledge base."""
    original_path: Path
    module_name: str
    content: str
    is_python: bool

    def generate_module_content(self) -> str:
        """Generate the Python module content with self-invoking functionality."""
        if self.is_python:
            return self.content

        # Fixed the string formatting and removed problematic lambda execution
        return f'''"""
Original file: {self.original_path}
Auto-generated content module
"""

ORIGINAL_PATH = "{self.original_path}"
CONTENT = """{self.content}"""

def default_behavior() -> bool:
    """Default behavior when module is loaded."""
    print(f"Loading content from: {{ORIGINAL_PATH}}")
    return True

def get_content() -> str:
    """Returns the original content."""
    return CONTENT

def get_metadata() -> dict:
    """Metadata for the original file."""
    return {{
        "original_path": ORIGINAL_PATH,
        "is_python": {self.is_python},
        "module_name": "{self.module_name}"
    }}

# Execute default behavior on import
default_behavior()
'''


def create_module(module_name: str, module_code: str, main_module_path: str) -> Optional[ModuleType]:
    """
    Dynamically creates a module with the specified name, injects code into it,
    and adds it to sys.modules.

    Args:
        module_name: Name of the module to create.
        module_code: Source code to inject into the module.
        main_module_path: File path of the main module.

    Returns:
        The dynamically created module, or None if an error occurs.
    """
    dynamic_module = ModuleType(module_name)
    dynamic_module.__file__ = main_module_path or "runtime_generated"
    dynamic_module.__package__ = module_name
    dynamic_module.__path__ = None  # type: ignore
    dynamic_module.__doc__ = None

    try:
        exec(module_code, dynamic_module.__dict__)
        sys.modules[module_name] = dynamic_module
        return dynamic_module
    except Exception as e:
        print(
            f"Error injecting code into module {module_name}: {e}", file=sys.stderr)
        return None


def validate(instance: dict) -> bool:
    """Validate instance JSON schema."""
    required_keys = ["id", "name"]
    return all(key in instance for key in required_keys)


def create_content_module_from_instance(instance: dict) -> Optional[ContentModule]:
    """Create a ContentModule from instance data."""
    try:
        instance_id = instance["id"]
        instance_name = instance.get("name", f"instance_{instance_id}")
        content = instance.get(
            "content", f"Content for instance {instance_id}")
        is_python = instance.get("is_python", False)

        # Create a path-like object for the original_path
        original_path = Path(f"runtime_generated_{instance_id}")
        module_name = f"morphological.instance_{instance_id}"

        return ContentModule(
            original_path=original_path,
            module_name=module_name,
            content=content,
            is_python=is_python
        )
    except Exception as e:
        print(f"Error creating ContentModule: {e}", file=sys.stderr)
        return None


def main() -> int:
    """
    Process instance JSON from stdin, create a dynamic module, and execute it.
    Returns an exit code (0 for success, 1 for failure).
    """
    try:
        # Read and parse stdin once
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            print("Error: No input provided", file=sys.stderr)
            return 1

        instance = json.loads(stdin_data)
        if not validate(instance):
            print("Error: Invalid instance schema", file=sys.stderr)
            return 1

        # Create ContentModule from instance
        content_module = create_content_module_from_instance(instance)
        if not content_module:
            print("Error: Failed to create ContentModule", file=sys.stderr)
            return 1

        # Generate module code using the ContentModule
        module_code = content_module.generate_module_content()

        # Get main module path
        main_module_path = getattr(
            sys.modules['__main__'], '__file__', 'runtime_generated')

        # Create and execute the dynamic module
        dynamic_module = create_module(
            content_module.module_name,
            module_code,
            main_module_path
        )

        if not dynamic_module:
            print(
                f"Error: Failed to create module {content_module.module_name}", file=sys.stderr)
            return 1

        # Optional: Call additional methods if they exist
        if hasattr(dynamic_module, 'get_metadata'):
            metadata = dynamic_module.get_metadata()
            print(f"Module metadata: {json.dumps(metadata, indent=2)}")

        print(
            f"Successfully created and executed module: {content_module.module_name}")
        return 0

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # echo '{"id": "test123", "name": "Test Instance"}' | python3 app_bridge.py
    sys.exit(main())
