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
"""
Morphological / Homoiconic runtime library
-----------------------------------------
Self-contained implementation of:
 - AsyncAtom (safe execution sandbox for user-provided async code)
 - ByteWord          (8-bit morphological atom, helpers)
 - MorphicTransformation (pattern-based morph transforms)
 - TripartiteAtom    (T/V/C triplet primitive)
 - HomoiconicRuntime (context-managed, self-serializing runtime)
 - EnhancedRuntimeSystem (local embedding + Merkle persistence)

Design goals:
 - Safe, explicit async execution model (user code must define an async entrypoint)
 - Deterministic pseudo-embeddings for offline demos (pluggable to online provider)
 - Clear lifecycle, refcounting, cleanup semantics
 - Minimal external dependence (stdlib only)
"""
# > © 2024-2025 Phovos https://github.com/Phovos/Morphologic BSD-3 & CC ND
# > © 2023-2025 Moonlapsed https://github.com/MOONLAPSED/Cognosis
from __future__ import annotations

import ast
import asyncio
import base64
import hashlib
import json
import math
import time
from abc import ABC, abstractmethod
from array import array
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    TypeVar,
    Union,
)

# ----------------------------
# Utilities
# ----------------------------


def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_repr(obj: Any, maxlen: int = 200) -> str:
    try:
        r = repr(obj)
    except Exception:
        r = f"<unrepr {type(obj).__name__}>"
    if len(r) > maxlen:
        return r[:maxlen] + "…"
    return r


# ----------------------------
# __Atom__ base (refcount + lifecycle)
# ----------------------------


class __Atom__(ABC):
    """
    Minimal reference-counted object with cleanup contract.
    Mirrors core CPython semantics lightly for lifecycle control.
    """

    __slots__ = ("_refcount",)

    def __init__(self) -> None:
        self._refcount: int = 1

    def inc_ref(self) -> None:
        self._refcount += 1

    def dec_ref(self) -> None:
        self._refcount -= 1
        if self._refcount <= 0:
            # delegate cleanup asynchronously if needed
            coro = self.cleanup()
            # if cleanup is coroutine, schedule it
            if asyncio.iscoroutine(coro):
                try:
                    asyncio.get_running_loop().create_task(coro)
                except RuntimeError:
                    # No running loop; call synchronously
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(coro)
                    loop.close()

    @abstractmethod
    def cleanup(self) -> Union[None, Awaitable[None]]:
        """Cleanup resources when the atom is no longer referenced."""
        raise NotImplementedError


# ----------------------------
# ByteWord
# ----------------------------


@dataclass(frozen=True)
class ByteWord:
    """
    A compact representation for an 8-bit morphological atom.

    Using .raw as an int 0..255. Convenience helpers for bra/ket nibble
    and `pilot` (msb of bra) semantics are included.

    This implementation keeps low-level operations explicit and fast.
    """

    raw: int

    def __post_init__(self):
        if not (0 <= self.raw <= 0xFF):
            raise ValueError("ByteWord.raw must be 0..255")

    @property
    def bra(self) -> int:
        """Left nibble (MSB nibble) - 4 bits"""
        return (self.raw >> 4) & 0x0F

    @property
    def ket(self) -> int:
        """Right nibble (LSB nibble) - 4 bits"""
        return self.raw & 0x0F

    @property
    def pilot(self) -> int:
        """The MSB bit within the bra (C bit / 'pilot wave')"""
        # If we think of bra as 4 bits b3 b2 b1 b0 (b3 is highest)
        return (self.raw >> 7) & 0x01

    def with_bra(self, nibble: int) -> "ByteWord":
        nib = nibble & 0x0F
        return ByteWord((nib << 4) | self.ket)

    def with_ket(self, nibble: int) -> "ByteWord":
        nib = nibble & 0x0F
        return ByteWord((self.bra << 4) | nib)

    def to_bytes(self) -> bytes:
        return bytes([self.raw])

    def __int__(self) -> int:
        return self.raw

    def __repr__(self) -> str:
        return f"ByteWord(0x{self.raw:02X} ⟨{self.bra:04b}|{self.ket:04b}⟩)"

    # deterministic, cheap "quantum extract" for demo
    def quantum_extract(self, strategy: str = "sha256_last") -> int:
        """
        Deterministic extraction:
          - 'sha256_last' : SHA256(raw) and take last byte
          - 'hamming'     : popcount of raw
          - 'lsb'         : least-significant bit
        """
        if strategy == "sha256_last":
            return sha256_bytes(bytes([self.raw]))[-1]
        if strategy == "hamming":
            return bin(self.raw).count("1")
        if strategy == "lsb":
            return self.raw & 1
        return sha256_bytes(bytes([self.raw]))[-1]


# ----------------------------
# MorphicTransformation
# ----------------------------


@dataclass
class MorphicTransformation:
    """
    Pattern-based morphic transformation.

    lhs/rhs can be:
      - int (interpreted as a single byte value 0..255)
      - bytes (pattern)
      - str  (encoded to utf-8 bytes before matching)

    apply() matches lhs (first occurrence) and replaces with rhs.
    This is intentionally simple (deterministic) and safe.
    """

    symmetry: str
    conservation: str
    lhs: Union[int, bytes, str]
    rhs: Union[int, bytes, str]

    def _to_bytes(self, v: Union[int, bytes, str]) -> bytes:
        if isinstance(v, bytes):
            return v
        if isinstance(v, int):
            if not (0 <= v <= 0xFF):
                raise ValueError("int pattern must be 0..255")
            return bytes([v])
        if isinstance(v, str):
            return v.encode("utf-8")
        raise TypeError("lhs/rhs must be int|bytes|str")

    def apply(self, data: bytes) -> bytes:
        l = self._to_bytes(self.lhs)
        r = self._to_bytes(self.rhs)
        idx = data.find(l)
        if idx == -1:
            return data
        return data[:idx] + r + data[idx + len(l) :]


# ----------------------------
# TripartiteAtom (T/V/C)
# ----------------------------

T = TypeVar("T")
V = TypeVar("V")


@dataclass
class TripartiteAtom(Generic[T, V]):
    """
    A minimal T/V/C container:
      - T: static 'type' (informational signature)
      - V: current value
      - C: optional callable (computation) that maps V and args -> V'
    """

    T: Any
    V: V
    C: Optional[Callable[..., V]] = None

    def __call__(self, *args: Any, **kwargs: Any) -> "TripartiteAtom":
        if self.C is None:
            raise TypeError("TripartiteAtom has no computational component")
        new_value = self.C(self.V, *args, **kwargs)
        return TripartiteAtom(self.T, new_value, self.C)

    def morph(self) -> "TripartiteAtom":
        """
        If T defines a __morph__ hook, use it to transform V.
        Otherwise return self (idempotent).
        """
        if hasattr(self.T, "__morph__") and callable(self.T.__morph__):
            new_v = self.T.__morph__(self.V)
            return TripartiteAtom(self.T, new_v, self.C)
        return self


# ----------------------------
# AsyncAtom (safe execution)
# ----------------------------

AllowedBuiltinNames = {
    "abs",
    "min",
    "max",
    "pow",
    "range",
    "len",
    "enumerate",
    "sum",
    "int",
    "float",
    "str",
    "bool",
    "bytes",
    "bytearray",
    "dict",
    "list",
    "tuple",
    "set",
}


def make_safe_builtins() -> Dict[str, Any]:
    # Determine the actual dictionary of built-ins to use for lookup
    if isinstance(__builtins__, dict):
        builtins_dict = __builtins__
    else:
        # If it's the module object, use its __dict__
        builtins_dict = vars(__builtins__)

    safe = {
        name: builtins_dict[name]
        for name in AllowedBuiltinNames
        if name in builtins_dict
    }
    # Provide a small 'safe' subset
    safe["math"] = math
    safe["sha256_hex"] = sha256_hex
    return safe


class AsyncAtom(__Atom__, Generic[T, V]):
    """
    An asynchronous atom which executes user-provided async code in a small sandbox.

    Requirements for user code:
      - Must define an async coroutine with signature:
            async def atom_entrypoint(__atom_self__, *args, **kwargs):
                ...
        The runtime will call that coroutine.

    Notes:
      - Execution namespace is restricted (small builtins).
      - Only explicit safe keys are persisted back to the atom's local env.
      - Spawned tasks are tracked for cleanup.
    """

    __slots__ = (
        "_code",
        "_value",
        "_local_env",
        "_ttl",
        "_created_at",
        "_last_access_time",
        "request_data",
        "session",
        "runtime_namespace",
        "security_context",
        "_pending_tasks",
        "_lock",
        "_buffer",
    )

    def __init__(
        self,
        code: str,
        value: Optional[V] = None,
        ttl: Optional[float] = None,
        request_data: Optional[Dict[str, Any]] = None,
        buffer_size: int = 64 * 1024,
    ):
        super().__init__()
        self._code: str = code
        self._value: Optional[V] = value
        self._local_env: Dict[str, Any] = {}
        self._ttl: Optional[float] = ttl
        self._created_at: float = time.time()
        self._last_access_time: float = self._created_at
        self.request_data: Dict[str, Any] = request_data or {}
        self.session: Dict[str, Any] = dict(self.request_data.get("session") or {})
        self.runtime_namespace: Optional[Dict[str, Any]] = None
        self.security_context: Optional[Dict[str, Any]] = None
        self._pending_tasks: Set[asyncio.Task] = set()
        self._lock: asyncio.Lock = asyncio.Lock()
        self._buffer: bytearray = bytearray(buffer_size)

    # --- context manager helpers ---
    async def __aenter__(self) -> "AsyncAtom":
        self.inc_ref()
        self._last_access_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.dec_ref()
        # do not suppress exceptions
        return False

    # --- lifecycle / cleanup ---
    async def cleanup(self) -> None:
        # cancel pending tasks and await them
        tasks = list(self._pending_tasks)
        for t in tasks:
            if not t.done():
                t.cancel()
        for t in tasks:
            try:
                await t
            except asyncio.CancelledError:
                pass
            except Exception:
                # best-effort; do not raise
                pass
        self._pending_tasks.clear()
        # clear buffer & local env
        self._buffer = bytearray(0)
        self._local_env.clear()

    # --- utilities ---
    def is_expired(self) -> bool:
        if self._ttl is None:
            return False
        return (time.time() - self._created_at) > self._ttl

    async def preload_buffer(self, data: bytes) -> None:
        async with self._lock:
            if len(data) <= len(self._buffer):
                self._buffer[: len(data)] = data
            else:
                self._buffer = bytearray(data)

    async def get_buffer(
        self, offset: int = 0, length: Optional[int] = None
    ) -> memoryview:
        async with self._lock:
            if length is None:
                return memoryview(self._buffer)[offset:]
            return memoryview(self._buffer)[offset : offset + length]

    async def spawn_task(self, coro: Awaitable) -> asyncio.Task:
        task = asyncio.create_task(coro)
        self._pending_tasks.add(task)
        task.add_done_callback(self._pending_tasks.discard)
        return task

    def _validate_user_code_is_async(self) -> bool:
        """
        Quick AST check if the provided code string contains an async def.
        This is advisory; compile/exec will confirm the function exists.
        """
        try:
            tree = ast.parse(self._code)
        except SyntaxError:
            return False
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
                return True
        return False

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the user-supplied async entrypoint.
        The code must define an async def atom_entrypoint(__atom_self__, *args, **kwargs)
        """
        self._last_access_time = time.time()
        async with self._lock:
            # create very restricted namespace
            safe_builtins = make_safe_builtins()
            execution_ns: Dict[str, Any] = {
                "__builtins__": safe_builtins,
                "_local_env": dict(self._local_env),  # snapshot
                "sha256_hex": sha256_hex,
                "math": math,
            }
            if "__atom_self__" in execution_ns:
                del execution_ns["__atom_self__"]
            # populate runtime namespace if set
            if self.runtime_namespace is not None:
                # shallow copy for safety
                execution_ns.update(self.runtime_namespace)

            # compile + exec user code
            wrapped = self._code
            # The user code must define 'async def atom_entrypoint(__atom_self__, *args, **kwargs):'
            try:
                code_obj = compile(wrapped, "<asyncatom>", "exec")
                if self.runtime_namespace is not None:
                    # Create a clean copy to manipulate
                    runtime_data = self.runtime_namespace.copy()

                    # 🔑 ACTION: Safely remove the conflicting key if it exists
                    runtime_data.pop('__atom_self__', None)

                    # Merge the cleaned data into the execution namespace
                    execution_ns.update(runtime_data)
            except Exception as e:
                raise RuntimeError(f"User code compile error: {e}") from e

            # Execute compiled code in the restricted namespace
            try:
                exec(code_obj, execution_ns)
            except Exception as e:
                raise RuntimeError(f"User code exec error: {e}") from e

            # get the entrypoint
            main_func = execution_ns.get("atom_entrypoint")
            if main_func is None or not asyncio.iscoroutinefunction(main_func):
                raise RuntimeError(
                    "User code must define async def atom_entrypoint(__atom_self__, *args, **kwargs)"
                )

            # Call the coroutine
            try:
                result = await main_func(__atom_self__=self, *args, **kwargs)
            except Exception:
                raise

            # Persist a small, explicit set of keys from execution_ns back into _local_env
            # whitelisting avoids leaking surprising values
            keys_to_persist = ("persist", "state", "memo")  # user may set these in code
            for k in keys_to_persist:
                if k in execution_ns:
                    self._local_env[k] = execution_ns[k]

            # update any values user explicitly stored in a `_out` mapping
            o = execution_ns.get("_out")
            if isinstance(o, dict):
                for k, v in o.items():
                    self._local_env[k] = v

            # attach returned result to atom value if explicit
            if result is not None:
                self._value = result

            return result


# ----------------------------
# HomoiconicRuntime
# ----------------------------


class HomoiconicRuntime:
    """
    A simple runtime that is 'homoiconic' (code+data in one).
    It can register TripartiteAtom instances, mutate them, and optionally serialize
    to a source file when exiting the dynamic context.

    Usage:
      rt = HomoiconicRuntime()
      rt.register("foo", TripartiteAtom(int, 0, lambda v,x: v+x))
      with rt:
          rt.apply_transformation(...)
    """

    def __init__(self) -> None:
        self.namespace: Dict[str, Any] = {}
        # default morphology
        self._dynamic: bool = False
        self.source_path: Optional[Path] = None
        self.transformation_history: List[Dict[str, Any]] = []

    def __enter__(self) -> "HomoiconicRuntime":
        self._dynamic = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # On normal exit, serialize if path provided
        if exc_type is None and self.source_path is not None:
            try:
                self._serialize_to_source()
            except Exception:
                # Don't allow serialization errors to propagate out of context manager
                pass
        self._dynamic = False
        return False  # do not suppress exceptions

    def register(self, name: str, atom: TripartiteAtom) -> None:
        self.namespace[name] = atom

    def apply_transformation(self, t: MorphicTransformation) -> None:
        if not self._dynamic:
            raise RuntimeError(
                "Runtime must be dynamic (use with context) to apply transformations"
            )
        # record
        self.transformation_history.append(
            {
                "symmetry": t.symmetry,
                "conservation": t.conservation,
                "lhs": safe_repr(t.lhs),
                "rhs": safe_repr(t.rhs),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        # apply to registered TripartiteAtom values if they have bytes-like V
        for k, v in list(self.namespace.items()):
            if isinstance(v, TripartiteAtom):
                if isinstance(v.V, (bytes, bytearray)):
                    new_bytes = t.apply(bytes(v.V))
                    self.namespace[k] = TripartiteAtom(v.T, new_bytes, v.C)
                elif isinstance(v.V, (int,)):
                    # interpret int as little-endian bytes
                    b = int(v.V).to_bytes((v.V.bit_length() + 7) // 8 or 1, "little")
                    nb = t.apply(b)
                    # coerce back to int
                    ni = int.from_bytes(nb, "little")
                    self.namespace[k] = TripartiteAtom(v.T, ni, v.C)
                # else: skip non-bytes values

    def execute(self, code: str) -> None:
        """
        Execute code inside runtime namespace when dynamic.
        The code must define `async def atom_entrypoint(__atom_self__, *args, **kwargs)` or be simple top-level assignments.
        For safety, this method only allows simple execs that assign into the runtime namespace; heavy async execution should be handled via AsyncAtom.
        """
        if not self._dynamic:
            raise RuntimeError("Runtime must be dynamic to execute code")
        # restricted namespace
        ns = {"__builtins__": make_safe_builtins()}
        ns.update(self.namespace)
        try:
            exec(compile(code, "<runtime_exec>", "exec"), ns)
        except Exception as e:
            raise RuntimeError(f"Execution failed: {e}") from e
        # pick back named entries into namespace (avoid arbitrary mutation)
        for k in list(ns.keys()):
            if k.startswith("__"):
                continue
            if k in ("math", "sha256_hex"):  # allowed utilities
                continue
            # persist simple types: TripartiteAtom, bytes, int, str, dict
            v = ns[k]
            if isinstance(
                v, (TripartiteAtom, bytes, bytearray, int, str, dict, list, tuple)
            ):
                self.namespace[k] = v

    def _serialize_to_source(self) -> None:
        """
        A safe and idempotent serialization that writes a JSON snapshot of the
        runtime namespace+transformations to the `source_path` with a .morphic.json suffix.
        This avoids editing Python source directly while still providing reconstitution.
        """
        if self.source_path is None:
            raise RuntimeError("No source_path defined")
        p = Path(self.source_path)
        out = p.with_suffix(p.suffix + ".morphic.json")
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "namespace": {},
            "transformation_history": self.transformation_history,
        }
        for k, v in self.namespace.items():
            if isinstance(v, TripartiteAtom):
                snapshot["namespace"][k] = {
                    "T": getattr(v.T, "__name__", str(v.T)),
                    "V": base64.b64encode(
                        json.dumps(v.V, default=lambda o: safe_repr(o)).encode()
                    ).decode(),
                    "has_C": bool(v.C),
                }
            else:
                snapshot["namespace"][k] = base64.b64encode(
                    json.dumps(v, default=lambda o: safe_repr(o)).encode()
                ).decode()
        out.write_text(json.dumps(snapshot, indent=2))
        # note: we deliberately do not try to re-create Python code; that's a higher-trust operation


# ----------------------------
# Simple deterministic embedding provider (pluggable)
# ----------------------------


class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        raise NotImplementedError


class DeterministicHasherEmbedding(EmbeddingProvider):
    """
    Deterministic pseudo-embedding generator using SHA256.
    Useful for offline/demo runs. Produces `dimensions` floats in [-1,1].
    """

    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions

    async def embed(self, text: str) -> List[float]:
        h = sha256_bytes(text.encode("utf-8"))
        # expand to required dims by repeated hashing
        vals: List[float] = []
        state = h
        while len(vals) < self.dimensions:
            state = sha256_bytes(state)
            for i in range(0, len(state), 4):
                if len(vals) >= self.dimensions:
                    break
                chunk = state[i : i + 4]
                v = int.from_bytes(chunk, "big") / (2**32 - 1)
                # map into [-1,1]
                vals.append((v * 2.0) - 1.0)
        return vals[: self.dimensions]


# ----------------------------
# MerkleNode & persistence
# ----------------------------


class MerkleNode:
    def __init__(self, data: Any, children: Optional[List["MerkleNode"]] = None):
        self.data = data
        self.children: List[MerkleNode] = children or []
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.uuid = sha256_hex(
            json.dumps({"data": safe_repr(data), "ts": self.timestamp}).encode()
        )[:16]
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        hasher = hashlib.sha256()
        hasher.update(
            json.dumps(
                self.data, sort_keys=True, default=lambda o: safe_repr(o)
            ).encode()
        )
        for child in sorted(self.children, key=lambda c: c.hash):
            hasher.update(child.hash.encode())
        return hasher.hexdigest()

    def add_child(self, child: "MerkleNode") -> None:
        self.children.append(child)
        self.hash = self._calculate_hash()


# ----------------------------
# EnhancedRuntimeSystem
# ----------------------------


class EnhancedRuntimeSystem:
    """
    Document store + deterministic embedding + merkle snapshot persistence.
    Uses deterministic hasher by default but accepts a pluggable EmbeddingProvider.
    """

    def __init__(
        self,
        embedding_provider: Optional[EmbeddingProvider] = None,
        config: Optional[dict] = None,
    ):
        self.embedding_provider = embedding_provider or DeterministicHasherEmbedding(
            dimensions=128
        )
        self.config = config or {
            "dimensions": 128,
            "store_path": "cache/documents.json",
        }
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: Dict[str, array] = {}
        self.clusters: Dict[int, List[str]] = defaultdict(list)
        self._store_path = Path(self.config.get("store_path", "cache/documents.json"))
        self.runtime_state = {"merkle_root": None, "state_history": []}
        self._load_store()

    async def add_document(
        self, content: str, metadata: Optional[dict] = None
    ) -> Dict[str, Any]:
        emb = await self.embedding_provider.embed(content)
        uid = sha256_hex(content.encode())[:32]
        doc = {
            "uuid": uid,
            "content": content,
            "metadata": metadata or {},
            "embedding": emb,
        }
        self.documents.append(doc)
        self.embeddings[uid] = array('f', emb)
        cid = self._assign_to_cluster(uid)
        self.clusters[cid].append(uid)
        await self._update_merkle_state()
        self._save_store()
        return doc

    def _save_store(self) -> None:
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        out = []
        for d in self.documents:
            out.append(
                {
                    "uuid": d["uuid"],
                    "content": d["content"],
                    "metadata": d["metadata"],
                    "embedding": list(d["embedding"]),
                }
            )
        self._store_path.write_text(json.dumps(out, indent=2))

    def _load_store(self) -> None:
        if not self._store_path.exists():
            return
        raw = json.loads(self._store_path.read_text())
        for rec in raw:
            self.documents.append(rec)
            self.embeddings[rec["uuid"]] = array('f', rec["embedding"])
            cid = self._assign_to_cluster(rec["uuid"])
            self.clusters[cid].append(rec["uuid"])

    def _assign_to_cluster(self, doc_id: str) -> int:
        if not self.clusters:
            return 0
        v = self.embeddings[doc_id]
        best_cid = 0
        best_sim = -1.0
        for cid, ids in self.clusters.items():
            centroid = self._centroid(cid)
            sim = self._cosine(v, centroid)
            if sim > best_sim:
                best_sim = sim
                best_cid = cid
        return best_cid

    def _centroid(self, cid: int) -> array:
        ids = self.clusters.get(cid, [])
        if not ids:
            return array('f', [0.0] * self.config.get("dimensions", 128))
        acc = array('f', [0.0] * self.config.get("dimensions", 128))
        for uid in ids:
            emb = self.embeddings[uid]
            for i, val in enumerate(emb):
                acc[i] += val
        n = len(ids)
        for i in range(len(acc)):
            acc[i] /= n
        return acc

    def _cosine(self, v1: array, v2: array) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(x * x for x in v1))
        n2 = math.sqrt(sum(x * x for x in v2))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    async def _update_merkle_state(self) -> None:
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "doc_count": len(self.documents),
            "cluster_count": len(self.clusters),
        }
        root = MerkleNode(state)
        for d in self.documents:
            root.add_child(MerkleNode({"uuid": d["uuid"], "content": d["content"]}))
        self.runtime_state["merkle_root"] = root
        self.runtime_state["state_history"].append(root.hash)
        # persist snapshot file
        p = Path("states") / root.hash[:2] / root.hash[2:4]
        p.mkdir(parents=True, exist_ok=True)
        (p / f"{root.hash}.json").write_text(
            json.dumps(
                {
                    "root_hash": root.hash,
                    "timestamp": state["timestamp"],
                    "doc_count": len(self.documents),
                },
                indent=2,
            )
        )

    async def query(self, text: str, top_k: int = 3) -> Dict[str, Any]:
        emb = await self.embedding_provider.embed(text)
        q_arr = array('f', emb)
        sims = [
            (d, self._cosine(q_arr, self.embeddings[d["uuid"]])) for d in self.documents
        ]
        sims.sort(key=lambda x: -x[1])
        top = sims[:top_k]
        ctx = "\n".join(d["content"] for d, _ in top)
        # deterministic "response" using hashing for demo; pluggable to an LLM
        resp = f"Top {len(top)} matches. Context snippet: {ctx[:200]!s}"
        return {
            "query": text,
            "response": resp,
            "matches": [{"uuid": d["uuid"], "score": s} for d, s in top],
        }


# ----------------------------
# Demo / Main
# ----------------------------


def create_demo_runtime() -> HomoiconicRuntime:
    rt = HomoiconicRuntime()
    # register sample atoms
    rt.register("int_adder", TripartiteAtom(int, 0, lambda v, x: v + x))
    rt.register("greet", TripartiteAtom(str, "Hello", lambda v, x: v + x))
    rt.register(
        "sem", TripartiteAtom(list, [0.1, 0.2, 0.3], lambda v, other: v + list(other))
    )
    return rt


async def demo():
    # create enhanced system and add seed doc
    ers = EnhancedRuntimeSystem()
    doc = await ers.add_document("Seed: Morphic Source Code demo", {"phase": "seed"})
    print("Added document:", doc["uuid"])

    # demo runtime usage
    rt = create_demo_runtime()
    rt.source_path = Path("demo_app.py")  # will write demo_app.py.morphic.json on exit
    with rt:
        # call tripartite atoms
        a = rt.namespace["int_adder"]
        assert isinstance(a, TripartiteAtom)
        r = a(42)
        print("int_adder ->", r.V)
        g = rt.namespace["greet"]
        print("greet ->", g(" from runtime").V)
        # apply a byte-level transform to any bytes-like atoms (none here), but we show transformation record
        trans = MorphicTransformation("flip01", "demo", lhs=b"\x01", rhs=b"\xff")
        rt.apply_transformation(trans)
        # runtime executed simple code (assign into namespace)
        rt.execute("x = 123\nrt_value = 'persisted'")
        # On exiting the with-block, runtime snapshot will be written

    # AsyncAtom demo
    code = """
async def atom_entrypoint(__atom_self__, x):
    # simple computation that persists a 'state' key
    state = getattr(__atom_self__, '_local_env', {}).get('state', 0) + x
    # mark persistable variable
    _out = {'last': state}
    return state
"""
    atom = AsyncAtom(code, value=None)
    res = await atom(7)
    print("AsyncAtom result:", res)
    print("AsyncAtom local env after run:", atom._local_env)
    # cleanup
    await atom.cleanup()

    # query demo
    out = await ers.query("Tell me about seed")
    print("Query:", out["response"])


def main():
    asyncio.run(demo())


if __name__ == "__main__":
    main()
