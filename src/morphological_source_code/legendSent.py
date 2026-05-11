#!/usr/bin/env -S uv run
# -*- coding: utf-8 -*-
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
# Hermitian Dual Legendre Sentinels: MSC&QSD Atomic Update Protocol

- The quine is the trojan horse that verifies its own morphology.

More formally;

F: A -> A-hat such that * is MorphologicalComposition and . is pointwise multiplication
    - Convolution in the base domain: `*`
    - Pointwise multiplication in the spectral domain: `.`
    - F(a*b) = F(a).F(b)

## Integration/future

1. Manifold Coordination
   Use one sentinel pair per major morphological region:
   ```python
   HEADER_SENTINEL = HermitianSentinel(
       _SELF.with_suffix('.header.json'),
       _SELF.with_suffix('.shape.json')
   )
   ```

2. Quine Bootstrap Hook
   ```python
   def self_verify() -> None:
       valid, msg = HEADER_SENTINEL.verify()
       if not valid:
           logger.warning("Hermitian duality broken: %s — attempting recovery", msg)
           recovered, rmsg = HEADER_SENTINEL.recover()
           logger.info("Recovery: %s — %s", recovered, rmsg)
   ```

3. ByteWord / DoF / TVC Tie-in
   Each `ByteWord` atom can carry a lightweight sentinel hash for its local morphology. The captain bit (C) flips on verification events and feeding/feedbacking w/ the microcanonical ghost ensemble.

4. Update Pattern** (example)
   ```python
   success, msg = sentinel.update({"manifold_region": "[6,42]", "dof_count": 137})
   if success:
       logger.info("Morphology advanced: %s", msg)
   ```
"""
import hashlib
import json
import os
import time
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Platform-aware locking
if os.name == "posix":
    import fcntl
    def _acquire_lock(path: Path, exclusive: bool = True) -> Optional[object]:
        lock_path = path.with_suffix('.lock')
        try:
            lf = open(lock_path, 'w')
            fcntl.flock(lf.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
            return lf
        except OSError:
            return None
else:  # Windows
    import msvcrt
    def _acquire_lock(path: Path, exclusive: bool = True) -> Optional[object]:
        lock_path = path.with_suffix('.lock')
        try:
            lf = open(lock_path, 'w')
            msvcrt.locking(lf.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_RLCK, 1)
            return lf
        except OSError:
            return None

def _release_lock(lock_handle: Optional[object]) -> None:
    if not lock_handle:
        return
    try:
        if os.name == "posix":
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
        else:
            msvcrt.locking(lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
        lock_handle.close()
    except Exception:
        pass


class HermitianSentinel:
    """
    Hermitian Dual Sentinels (A ↔ B)
    Each file contains the cryptographic hash of the other.
    This enforces a fixed-point involution: f(A) = B ∧ f(B) = A.
    Updates are atomic across the pair. Corruption in one is immediately
    detectable by the other. Perfect for quine self-verification and
    Machian-Noetherian nominative invariance.
    """

    def __init__(self, path_a: Path, path_b: Path, max_drift: float = 2.0):
        self.path_a = path_a.resolve()
        self.path_b = path_b.resolve()
        self.max_drift = max_drift

    def _hash(self, p: Path) -> Optional[str]:
        if not p.exists():
            return None
        return hashlib.sha256(p.read_bytes()).hexdigest()

    def _read(self, p: Path) -> Optional[Dict[str, Any]]:
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _write_atomic(self, p: Path, data: Dict[str, Any]) -> bool:
        tmp = p.with_suffix(f".tmp.{os.getpid()}.{int(time.time())}")
        try:
            tmp.write_text(json.dumps(data, sort_keys=True, indent=2), encoding="utf-8")
            tmp.rename(p)
            return True
        except Exception:
            tmp.unlink(missing_ok=True)
            return False

    def verify(self) -> Tuple[bool, str]:
        """Verify the Hermitian relation holds."""
        lock_a = _acquire_lock(self.path_a, exclusive=False)
        lock_b = _acquire_lock(self.path_b, exclusive=False)
        try:
            da = self._read(self.path_a)
            db = self._read(self.path_b)

            if da is None and db is None:
                return True, "First run — empty pair valid"
            if da is None or db is None:
                return False, "One sentinel missing"

            ha = self._hash(self.path_a)
            hb = self._hash(self.path_b)
            if ha is None or hb is None:
                return False, "Hash computation failed"

            if da.get("hash_of_b") != hb or db.get("hash_of_a") != ha:
                return False, "Cross-hash mismatch"

            if abs(da.get("timestamp", 0) - db.get("timestamp", 0)) > self.max_drift:
                return False, "Timestamp drift violation"

            if da.get("version") != db.get("version"):
                return False, "Version mismatch"

            return True, "Hermitian duality verified"
        finally:
            _release_lock(lock_a)
            _release_lock(lock_b)

    def update(self, metadata: Optional[Dict] = None) -> Tuple[bool, str]:
        """Atomically update the pair while preserving the involution."""
        lock_a = _acquire_lock(self.path_a)
        if not lock_a:
            return False, "Failed to lock A"
        lock_b = _acquire_lock(self.path_b)
        if not lock_b:
            _release_lock(lock_a)
            return False, "Failed to lock B"

        try:
            ca = self._read(self.path_a) or {}
            cb = self._read(self.path_b) or {}

            version = max(ca.get("version", 0), cb.get("version", 0)) + 1
            ts = time.time()
            meta = metadata or {}

            # Stage 1: Tentative writes (placeholders)
            tmp_a = self.path_a.with_suffix(f".newa.{os.getpid()}")
            tmp_b = self.path_b.with_suffix(f".newb.{os.getpid()}")

            tent_a = {"version": version, "timestamp": ts, "hash_of_b": "PLACEHOLDER", "metadata": meta}
            tent_b = {"version": version, "timestamp": ts, "hash_of_a": "PLACEHOLDER", "metadata": meta}

            tmp_a.write_text(json.dumps(tent_a, sort_keys=True, indent=2), encoding="utf-8")
            tmp_b.write_text(json.dumps(tent_b, sort_keys=True, indent=2), encoding="utf-8")

            # Stage 2: Compute real hashes of tentative content
            real_ha = hashlib.sha256(tmp_a.read_bytes()).hexdigest()
            real_hb = hashlib.sha256(tmp_b.read_bytes()).hexdigest()

            # Stage 3: Final data with correct cross-hashes
            final_a = {**tent_a, "hash_of_b": real_hb}
            final_b = {**tent_b, "hash_of_a": real_ha}

            tmp_a.write_text(json.dumps(final_a, sort_keys=True, indent=2), encoding="utf-8")
            tmp_b.write_text(json.dumps(final_b, sort_keys=True, indent=2), encoding="utf-8")

            # Final safety check
            if (hashlib.sha256(tmp_a.read_bytes()).hexdigest() != real_ha or
                final_a["hash_of_b"] != hashlib.sha256(tmp_b.read_bytes()).hexdigest()):
                return False, "Internal cross-hash consistency failed"

            # Atomic commit
            tmp_a.rename(self.path_a)
            tmp_b.rename(self.path_b)

            return True, f"Atomic update to version {version} successful"
        except Exception as e:
            return False, f"Update failed: {e}"
        finally:
            _release_lock(lock_b)
            _release_lock(lock_a)

    def recover(self) -> Tuple[bool, str]:
        """Best-effort recovery using newer sentinel as truth."""
        valid, msg = self.verify()
        if valid:
            return True, msg

        da = self._read(self.path_a)
        db = self._read(self.path_b)

        if da and not db:
            ha = self._hash(self.path_a)
            if ha and self._write_atomic(self.path_b, {
                "version": da["version"], "timestamp": da["timestamp"],
                "hash_of_a": ha, "metadata": da.get("metadata", {})
            }):
                return True, "Recovered B from A"
        elif db and not da:
            # symmetric
            hb = self._hash(self.path_b)
            if hb and self._write_atomic(self.path_a, {
                "version": db["version"], "timestamp": db["timestamp"],
                "hash_of_b": hb, "metadata": db.get("metadata", {})
            }):
                return True, "Recovered A from B"

        # Both exist but inconsistent — newer wins
        if da and db:
            if da.get("timestamp", 0) >= db.get("timestamp", 0):
                ha = self._hash(self.path_a)
                if ha and self._write_atomic(self.path_b, {**da, "hash_of_a": ha}):
                    return True, "Recovered from newer A"
            else:
                hb = self._hash(self.path_b)
                if hb and self._write_atomic(self.path_a, {**db, "hash_of_b": hb}):
                    return True, "Recovered from newer B"

        return False, "Recovery failed — manual intervention required"
