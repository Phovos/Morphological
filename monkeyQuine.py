"""Very dangerous conceptual implementation do not mess with this if you aren't sandboxed."""
# quine_agent_demo.py
import inspect
import types
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

# ──────────────────────────────────────────────────────────────────────────────
# 1)  Hack-safe reflective agent
# ──────────────────────────────────────────────────────────────────────────────


@dataclass
class SafeQuineAgent:
    name: str = "Larch"
    prompt_template: str = ">>> {input}"
    _history: list[str] = field(default_factory=list)

    # --- “Normal” behaviour ----------------------------------------------
    def greet(self) -> None:
        print(
            f"[{self.name}] Hello, human. Time is {datetime.now().isoformat(timespec='seconds')}.")

    def generate_prompt(self, user_input: str) -> str:
        self._history.append(user_input)
        return self.prompt_template.format(input=user_input)

    # --- Quine reflection -------------------------------------------------
    def reflect(self) -> str:
        """Return *current* class source as text."""
        return inspect.getsource(self.__class__)

# ──────────────────────────────────────────────────────────────────────────────
# 2)  Context manager that swaps the agent's class in-place
# ──────────────────────────────────────────────────────────────────────────────


@contextmanager
def quine_patch(obj: SafeQuineAgent, patch_source: str, *,
                on_error: Callable[[Exception], None] | None = None):
    """
    Temporarily replace `obj`'s class definition with code in `patch_source`.

    patch_source should *define* methods or attrs you want to add/override.
    On exit, the original class is restored.
    """
    original_src = inspect.getsource(obj.__class__)
    original_class = obj.__class__

    # Build a new namespace seeded with the current class dict
    ns: dict[str, object] = original_class.__dict__.copy()
    try:
        exec(patch_source, ns)          # may add / replace attrs in ns
        # Dynamically create patched subclass with same name
        PatchedCls = types.new_class(
            original_class.__name__, (), {}, lambda d: d.update(ns))
        obj.__class__ = PatchedCls      # hot-swap!
        yield obj
    except Exception as exc:
        if on_error:
            on_error(exc)
        else:
            raise
    finally:
        # Restore original behaviour
        obj.__class__ = original_class

# ──────────────────────────────────────────────────────────────────────────────
# 3)  Demonstrative main()
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    agent = SafeQuineAgent()

    print("=== BEFORE PATCH ===")
    agent.greet()
    print(agent.generate_prompt("Ping?"), "\n")

    # --- Define a one-off patch: new greet() + new prompt_template ----------
    patch_code = '''
def greet(self):
    print(f"[{self.name}] ✨ Patched hello! I now know {len(self._history)} prior inputs.")

new_template = "🤖 {input}  // patched"
'''

    with quine_patch(agent, patch_code):
        print("=== INSIDE PATCH CONTEXT ===")
        agent.greet()                                  # uses patched greet
        agent.prompt_template = locals().get("new_template", agent.prompt_template)
        print(agent.generate_prompt("Patched world?"), "\n")

    # After context: back to original
    print("=== AFTER PATCH ===")
    agent.greet()
    print(agent.generate_prompt("Back to normal."))


if __name__ == "__main__":
    main()
