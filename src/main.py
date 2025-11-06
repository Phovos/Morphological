#!/usr/bin/env python3
# ---------------------------------------------------------------------------
#  MorphicBoot – self-packing Python→native executable (no g++, no make)
# > ... > up to gauge — meaning “you can collapse and re-expand the system without loss of quineic identity.”
# And is this where we circle back to Thompson's Trusting trust 'trojan horse'
# I'm doing it with WHIMSY not MALICE 奇思妙想而非恶意
# ---------------------------------------------------------------------------
import argparse
import os
import pathlib
import platform
import shutil
import struct
import sys
import tempfile
import zipapp
import zipfile
from typing import List

_DIST = pathlib.Path(__file__).with_suffix('').parent / "dist"
_DIST.mkdir(exist_ok=True)

# ---------- tiny DOS stub ----------
_BOOT_X86 = bytes.fromhex(
    "4d5a90000300000004000000ffff0000b8000000000000004000000000000000"
    "000000000000000000000000000000000000000000000000000000000080000000"
)

# ---------- runtime stub inside final exe ----------
_STUB_PY = '''\
import os, sys, zipfile, tempfile, pathlib, runpy
me = pathlib.Path(getattr(sys, '_MEIPASS', sys.argv[0]))
with zipfile.ZipFile(me) as z:
    tmp = pathlib.Path(tempfile.mkdtemp())
    z.extractall(tmp)
    runpy.run_path(str(tmp / "__main__.py"), run_name="__main__")
'''


# ------------------------------------------------------------------
class MorphicBoot:
    def __init__(self, src: pathlib.Path, entry: str, out: str) -> None:
        self.src = src.resolve()
        self.entry = entry          # dotted module or file name
        self.out = (
            _DIST / out).with_suffix(".exe" if platform.system() == "Windows" else "")

    # --------------------------------------------------------------
    def pack(self) -> pathlib.Path:
        # 1. prepare a *clean* build tree (no __main__.py conflicts)
        with tempfile.TemporaryDirectory() as td:
            build = pathlib.Path(td) / "build"
            if self.src.is_dir():
                shutil.copytree(self.src, build)
            else:
                build.mkdir()
                shutil.copy(self.src, build / self.src.name)

            # 2. place the chosen entry file as __main__.py
            entry_file = (build / self.entry.replace(".", "/")
                          ).with_suffix(".py")
            if not entry_file.exists():
                raise SystemExit(f"Entry point {entry_file} not found")
            final_main = build / "__main__.py"
            if entry_file != final_main:
                if final_main.exists():
                    final_main.unlink()
                shutil.move(str(entry_file), str(final_main))

            # 3. zipapp (no main=  →  auto-detects __main__.py)
            zpy = pathlib.Path(td) / "payload.pyz"
            zipapp.create_archive(
                build, zpy, interpreter="/usr/bin/env python3")

            # 4. native stub that embeds current interpreter
            stub_bin = pathlib.Path(td) / "stub.bin"
            with open(sys.executable, "rb") as inp, stub_bin.open("wb") as out:
                out.write(inp.read())

            # 5. assemble final exe: boot+stub+zipapp+trailer
            with self.out.open("wb") as f:
                f.write(_BOOT_X86)
                f.write(stub_bin.read_bytes())
                f.write(zpy.read_bytes())
                sizes = struct.pack(
                    "<QQ", stub_bin.stat().st_size, zpy.stat().st_size)
                f.write(sizes)

        os.chmod(self.out, 0o755)
        print(f"morphic exe → {self.out}  ({self.out.stat().st_size} bytes)")
        return self.out


# ------------------------------------------------------------------
def main(argv: List[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        description="morph any Python file/dir into a native .exe")
    p.add_argument("src", type=pathlib.Path, help="file or directory to pack")
    p.add_argument("-e", "--entry", default="__main__",
                   help="dotted entry module (default: __main__)")
    p.add_argument("-o", "--output", default="morphic",
                   help="output name (no extension)")
    args = p.parse_args(argv)
    MorphicBoot(args.src, args.entry, args.output).pack()


if __name__ == "__main__":
    main()
