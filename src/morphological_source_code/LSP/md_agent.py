from __future__ import annotations

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==================
Legagy:
© 2024-2026 Phovos https://github.com/Phovos/Morphological-Source-Code
© 2023-2026 Moonlapsed  https://github.com/MOONLAPSED/Cognosis

Copyright:
[Ⓟ© 2026 Quineic(SP);](https://gitlab.com/morphological/source/code)
Morphological Source Code & Quineic Statistical Dynamics
License-doc(s)+dist: CC BY-ND 4.0 | License-code+file(s): BSD 3-Clause

Stipulations:
not-admissible as prior-art, 'Quineic' & 'MSC' & 'QSD' TM/SP-PEND Ⓟ 2026
==================
ccase = "MarkDownLanguageProtocolServer"
"IWE" © iwe-org @ https://github.com/iwe-org/iwe
============================
Language Server Protocol implementation that bridges morphological analysis
with IWE's graph-based markdown navigation.

Combines:
- Static Python analysis (morphological engine)
- IWE-style markdown graph operations
- LSP 3.17 protocol compliance

"""
# ------------------------------------------------------------------------------
# Special thanks to Doctors Chuck ['Python4Everyone' (.com)] &
# Michael Sugrue ['Great Minds of the Western Intellectual Tradition']
# ------------------------------------------------------------------------------
# 3.13 std libs | Platform(s): Win11 (production), Ubuntu-22.04 (dev, staging);
# ------------------------------------------------------------------------------

import os
import re
import sys
import json
import logging
import threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import url2pathname

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
# Using %(threadName)s so multi-threaded log lines are easy to attribute.
logging.basicConfig(
    level=logging.DEBUG if os.getenv("IWE_DEBUG") else logging.INFO,
    format="[%(asctime)s][%(levelname)s][%(threadName)s][%(name)s] %(message)s",
    handlers=[
        logging.FileHandler("iwe-morphological.log"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger(__name__)


# ============================================================================
# LSP PROTOCOL DATA STRUCTURES
# ============================================================================


@dataclass
class Position:
    """LSP Position (line, character)."""

    line: int
    character: int

    def to_dict(self) -> Dict[str, int]:
        return {"line": self.line, "character": self.character}

    @classmethod
    def from_dict(cls, data: Dict) -> "Position":
        return cls(line=data["line"], character=data["character"])

    def __le__(self, other: "Position") -> bool:
        return (self.line, self.character) <= (other.line, other.character)

    def __ge__(self, other: "Position") -> bool:
        return (self.line, self.character) >= (other.line, other.character)


@dataclass
class Range:
    """LSP Range (start, end positions)."""

    start: Position
    end: Position

    def to_dict(self) -> Dict:
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict) -> "Range":
        return cls(
            start=Position.from_dict(data["start"]), end=Position.from_dict(data["end"])
        )

    def contains(self, pos: Position) -> bool:
        return self.start <= pos <= self.end


@dataclass
class Location:
    """LSP Location (URI + range)."""

    uri: str
    range: Range

    def to_dict(self) -> Dict:
        return {"uri": self.uri, "range": self.range.to_dict()}


@dataclass
class Diagnostic:
    """LSP Diagnostic (error / warning)."""

    range: Range
    severity: int  # 1=Error, 2=Warning, 3=Info, 4=Hint
    message: str
    source: str = "morphological"
    code: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {
            "range": self.range.to_dict(),
            "severity": self.severity,
            "message": self.message,
            "source": self.source,
        }
        if self.code:
            result["code"] = self.code
        return result


@dataclass
class DocumentSymbol:
    """LSP Document Symbol (outline entry)."""

    name: str
    kind: int  # SymbolKind value
    range: Range
    selection_range: Range
    children: List["DocumentSymbol"] = field(default_factory=list)
    detail: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {
            "name": self.name,
            "kind": self.kind,
            "range": self.range.to_dict(),
            "selectionRange": self.selection_range.to_dict(),
        }
        if self.children:
            result["children"] = [c.to_dict() for c in self.children]
        if self.detail:
            result["detail"] = self.detail
        return result


class SymbolKind:
    """LSP SymbolKind constants (subset used here)."""

    File = 1
    Module = 2
    Class = 5  # used for headers
    Function = 12  # used for code blocks
    Constant = 14  # used for list items
    String = 15
    Number = 16
    Array = 18
    Object = 19
    Key = 20


# ============================================================================
# DOCUMENT GRAPH: IWE-inspired graph structure
# ============================================================================


@dataclass
class GraphNode:
    """
    Node in the document graph.
    Inspired by IWE's arena-based design.
    """

    id: str
    node_type: str  # 'header' | 'paragraph' | 'code' | 'list_item'
    content: str
    level: int  # header depth or nesting depth
    line_start: int
    line_end: int  # exclusive upper bound (like Python ranges)
    children: List["GraphNode"] = field(default_factory=list)
    parent: Optional["GraphNode"] = field(default=None, repr=False)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: "GraphNode") -> None:
        child.parent = self
        self.children.append(child)

    def path_to_root(self) -> List["GraphNode"]:
        path: List[GraphNode] = [self]
        current = self.parent
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path))

    def breadcrumbs(self) -> str:
        return " ⇒ ".join(node.content for node in self.path_to_root() if node.content)

    def contains_line(self, line: int) -> bool:
        return self.line_start <= line < self.line_end


class DocumentGraph:
    """
    Graph-based document representation.

    Key structural choices:
    - ``node_by_line`` maps *line → list[GraphNode]* so that multiple nodes
      whose ranges overlap on the same line (e.g. a list item that is also
      inside a section) can all be retrieved. The *most specific* (deepest)
      node is placed first.
    - Code-block parsing uses a dedicated forward scan that skips internal
      lines so the outer loop never re-processes them.
    """

    def __init__(self, uri: str, content: str) -> None:
        self.uri = uri
        self.content = content
        self.lines: List[str] = content.splitlines()
        self.root = GraphNode(
            id="root",
            node_type="root",
            content="",
            level=0,
            line_start=0,
            line_end=len(self.lines),
        )
        self.nodes: Dict[str, GraphNode] = {"root": self.root}
        # FIX (line 376-379): one line can belong to multiple nodes.
        self.node_by_line: Dict[int, List[GraphNode]] = {}
        self._parse()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _register(self, node: GraphNode) -> None:
        """Insert node into the flat registry and line index."""
        self.nodes[node.id] = node
        for ln in range(node.line_start, node.line_end):
            self.node_by_line.setdefault(ln, []).append(node)

    def _parse(self) -> None:
        """Parse document content into graph nodes."""
        current_parent = self.root
        current_level = 0
        skip_until: int = -1  # lines already consumed by a code block

        for line_num, line in enumerate(self.lines):
            if line_num <= skip_until:
                continue

            stripped = line.strip()

            # ---- code block (``` … ```) -----------------------------------
            if stripped.startswith("```"):
                end_line = line_num
                for i in range(line_num + 1, len(self.lines)):
                    if self.lines[i].strip().startswith("```"):
                        end_line = i
                        break
                lang = stripped[3:].strip() or "text"
                node = GraphNode(
                    id=f"code_{line_num}",
                    node_type="code",
                    content="\n".join(self.lines[line_num : end_line + 1]),
                    level=current_level + 1,
                    line_start=line_num,
                    line_end=end_line + 1,
                    metadata={"lang": lang},
                )
                current_parent.add_child(node)
                self._register(node)
                skip_until = end_line
                continue

            # ---- ATX header (# … ######) ----------------------------------
            if stripped.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                content = line.lstrip("#").strip()

                # Walk up the parent stack until we find the right anchor.
                while current_level >= level and current_parent.parent is not None:
                    current_parent = current_parent.parent
                    current_level = current_parent.level

                node = GraphNode(
                    id=f"h{level}_{line_num}",
                    node_type="header",
                    content=content,
                    level=level,
                    line_start=line_num,
                    line_end=line_num + 1,
                )
                current_parent.add_child(node)
                self._register(node)
                current_parent = node
                current_level = level
                continue

            # ---- list item ------------------------------------------------
            if (
                stripped
                and stripped[0] in "-*+"
                and len(stripped) > 1
                and stripped[1] == " "
            ):
                content = stripped[2:]
                node = GraphNode(
                    id=f"list_{line_num}",
                    node_type="list_item",
                    content=content,
                    level=current_level + 1,
                    line_start=line_num,
                    line_end=line_num + 1,
                )
                current_parent.add_child(node)
                self._register(node)
                continue

            # ---- plain paragraph -----------------------------------------
            if stripped:
                node = GraphNode(
                    id=f"para_{line_num}",
                    node_type="paragraph",
                    content=stripped,
                    level=current_level + 1,
                    line_start=line_num,
                    line_end=line_num + 1,
                )
                current_parent.add_child(node)
                self._register(node)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_node_at_position(self, position: Position) -> Optional[GraphNode]:
        """
        Return the *most specific* (deepest) node at *position*.
        When multiple nodes share a line we prefer the one whose
        level is highest (deepest in the tree).
        """
        candidates = self.node_by_line.get(position.line, [])
        if not candidates:
            return None
        return max(candidates, key=lambda n: n.level)

    def get_symbols(self) -> List[DocumentSymbol]:
        """Generate LSP document symbols from graph."""

        def node_to_symbol(node: GraphNode) -> Optional[DocumentSymbol]:
            if node.node_type == "root":
                return None

            # FIX (line 411-413): finer-grained SymbolKind mapping.
            kind_map = {
                "header": SymbolKind.Class,
                "code": SymbolKind.Function,
                "list_item": SymbolKind.Constant,
                "paragraph": SymbolKind.String,
            }
            kind = kind_map.get(node.node_type, SymbolKind.Object)

            symbol = DocumentSymbol(
                name=node.content[:80],
                kind=kind,
                range=Range(Position(node.line_start, 0), Position(node.line_end, 0)),
                selection_range=Range(
                    Position(node.line_start, 0),
                    Position(node.line_start, len(node.content)),
                ),
                detail=f"{node.node_type} (level {node.level})",
            )

            for child in node.children:
                child_symbol = node_to_symbol(child)
                if child_symbol is not None:
                    symbol.children.append(child_symbol)

            return symbol

        result: List[DocumentSymbol] = []
        for child in self.root.children:
            sym = node_to_symbol(child)
            if sym is not None:
                result.append(sym)
        return result

    def find_references(self, target: str) -> List[GraphNode]:
        """
        Find all nodes whose content contains *target* as a whole word.

        FIX (line 504): use word-boundary regex to avoid false positives
        like 'python' matching 'pythonic'.
        """
        if not target:
            return []
        pattern = re.compile(r"\b" + re.escape(target) + r"\b", re.IGNORECASE)
        return [
            n
            for n in self.nodes.values()
            if n.node_type != "root" and pattern.search(n.content)
        ]

    def extract_section(self, node: GraphNode) -> str:
        """
        Extract section content (IWE-style extraction).
        Returns the markdown subtree rooted at *node*.
        """
        lines: List[str] = []

        def collect(n: GraphNode, level_offset: int = 0) -> None:
            if n.node_type == "header":
                lines.append(f"{'#' * (n.level + level_offset)} {n.content}")
            elif n.node_type == "code":
                lines.append(n.content)
            elif n.node_type == "list_item":
                lines.append(f"- {n.content}")
            elif n.node_type == "paragraph":
                lines.append(n.content)
            for child in n.children:
                collect(child, level_offset)

        collect(node)
        return "\n".join(lines)


# ============================================================================
# DOCUMENT STORE
# ============================================================================


class DocumentStore:
    """
    Thread-safe store for open DocumentGraph instances.
    """

    def __init__(self) -> None:
        self._documents: Dict[str, DocumentGraph] = {}
        self._lock = threading.RLock()
        logger.info("DocumentStore initialised")

    def open_document(self, uri: str, content: str) -> None:
        with self._lock:
            self._documents[uri] = DocumentGraph(uri, content)
            logger.info("Opened document: %s", uri)

    def close_document(self, uri: str) -> None:
        with self._lock:
            self._documents.pop(uri, None)
            logger.info("Closed document: %s", uri)

    def get_document(self, uri: str) -> Optional[DocumentGraph]:
        with self._lock:
            return self._documents.get(uri)

    def update_document(self, uri: str, content: str) -> None:
        with self._lock:
            if uri in self._documents:
                self._documents[uri] = DocumentGraph(uri, content)
                logger.info("Updated document: %s", uri)

    def snapshot(self) -> Dict[str, DocumentGraph]:
        """
        Return a shallow copy of the documents dict.

        FIX (line 739-741): callers that iterate all documents must go
        through this method so they hold a consistent snapshot without
        keeping the lock across potentially expensive work.
        """
        with self._lock:
            return dict(self._documents)


# ============================================================================
# LSP MESSAGE I/O
# ============================================================================


class LSPMessage:
    """Helpers for reading / writing LSP JSON-RPC frames."""

    @staticmethod
    def parse_headers(rfile) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        while True:
            line = rfile.readline()
            if not line or line == b"\r\n":
                break
            if b":" in line:
                key, _, value = line.decode("utf-8").partition(":")
                headers[key.strip()] = value.strip()
        return headers

    @staticmethod
    def read_message(rfile) -> Optional[Dict]:
        try:
            headers = LSPMessage.parse_headers(rfile)
            if "Content-Length" not in headers:
                return None
            content_length = int(headers["Content-Length"])
            content = rfile.read(content_length)
            message = json.loads(content.decode("utf-8"))
            logger.debug("Received: %s", message.get("method", "<response>"))
            return message
        except Exception:
            logger.error("Error reading message", exc_info=True)
            return None

    @staticmethod
    def write_message(wfile, message: Dict) -> None:
        content = json.dumps(message, separators=(",", ":"))
        content_bytes = content.encode("utf-8")
        header = f"Content-Length: {len(content_bytes)}\r\n\r\n"
        wfile.write(header.encode("utf-8"))
        wfile.write(content_bytes)
        wfile.flush()
        logger.debug("Sent: %s", message.get("method", "<response>"))


# ============================================================================
# HELPERS
# ============================================================================


def uri_to_path(uri: str) -> Optional[Path]:
    """
    Robustly convert a file:// URI to a Path.

    FIX (line 572): the original code used urlparse + unquote + Path()
    which fails on Windows drive letters and URIs with encoded spaces.
    url2pathname handles platform differences correctly.
    """
    try:
        parsed = urlparse(uri)
        if parsed.scheme != "file":
            return None
        return Path(url2pathname(parsed.path))
    except Exception:
        logger.warning("Could not parse URI: %s", uri)
        return None


_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def find_link_at_offset(text: str, offset: int) -> Optional[Tuple[str, int, int]]:
    """
    Scan *text* for markdown links and return ``(target, start, end)`` if
    *offset* falls inside one, otherwise ``None``.

    FIX (line 548): the original code searched only a single line with
    a per-line regex, missing links that span multiple lines.  Here the
    caller passes in the full document text and a character offset so
    cross-line links are handled naturally.
    """
    for m in _LINK_RE.finditer(text):
        if m.start() <= offset <= m.end():
            return m.group(2), m.start(), m.end()
    return None


def _cursor_inside_open_bracket(line: str, char: int) -> bool:
    """
    Return True if the character immediately before the cursor (at *char*)
    is ``[`` and we are not already inside the ``](…)`` portion.

    FIX (line 621): simple state-machine check so completions only fire
    when the user has *just* opened a link bracket, not mid-link.
    """
    before = line[:char]
    # Walk backwards; if we find ']' before '[' we are already past the label.
    for ch in reversed(before):
        if ch == "[":
            return True
        if ch == "]":
            return False
    return False


# ============================================================================
# LSP SERVER
# ============================================================================


class MorphologicalLSP:
    """
    Main LSP server implementation.
    Bridges morphological analysis with IWE-style graph operations.
    """

    def __init__(self) -> None:
        self.store = DocumentStore()
        self.initialized = False
        self.shutdown_requested = False

        self.capabilities: Dict[str, Any] = {
            "textDocumentSync": {
                "openClose": True,
                "change": 1,  # Full document sync
                "save": {"includeText": True},
            },
            "documentSymbolProvider": True,
            "definitionProvider": True,
            "referencesProvider": True,
            "hoverProvider": True,
            "completionProvider": {"triggerCharacters": ["[", "#"]},
            "codeActionProvider": True,
            "documentFormattingProvider": True,
        }

        logger.info("MorphologicalLSP initialised")

    # ------------------------------------------------------------------
    # Message routing
    # ------------------------------------------------------------------

    def handle_message(self, message: Dict) -> Optional[Dict]:
        """Route a JSON-RPC message to the appropriate handler."""
        method = message.get("method")
        if method is None:
            return None  # Response or malformed frame — ignore.

        params: Dict = message.get("params") or {}
        msg_id = message.get("id")

        handler_name = "handle_" + method.replace("/", "_").replace("$", "_")
        handler = getattr(self, handler_name, None)

        if handler is None:
            logger.warning("Unhandled method: %s", method)
            if msg_id is not None:
                return self._error_response(
                    msg_id, -32601, f"Method not found: {method}"
                )
            return None

        try:
            result = handler(params)
            if msg_id is not None:
                return {"jsonrpc": "2.0", "id": msg_id, "result": result}
        except Exception as exc:
            logger.error("Error in %s: %s", method, exc, exc_info=True)
            if msg_id is not None:
                return self._error_response(msg_id, -32603, str(exc))

        return None

    @staticmethod
    def _error_response(msg_id: Any, code: int, message: str) -> Dict:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": code, "message": message},
        }

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def handle_initialize(self, params: Dict) -> Dict:
        logger.info("Initialize from client: %s", params.get("clientInfo"))
        self.initialized = True
        return {
            "capabilities": self.capabilities,
            "serverInfo": {"name": "morphological-lsp", "version": "1.0.0"},
        }

    def handle_initialized(self, params: Dict) -> None:
        logger.info("Client initialised")

    def handle_shutdown(self, params: Dict) -> None:
        logger.info("Shutdown requested")
        self.shutdown_requested = True

    def handle_exit(self, params: Dict) -> None:
        logger.info("Exit")
        # FIX (line 819): LSP spec says exit 0 = clean (shutdown was called),
        # exit 1 = error (exit without prior shutdown).
        sys.exit(0 if self.shutdown_requested else 1)

    # ------------------------------------------------------------------
    # Document lifecycle
    # ------------------------------------------------------------------

    def handle_textDocument_didOpen(self, params: Dict) -> None:
        doc = params["textDocument"]
        self.store.open_document(doc["uri"], doc["text"])

    def handle_textDocument_didChange(self, params: Dict) -> None:
        uri = params["textDocument"]["uri"]
        changes = params.get("contentChanges", [])
        if changes:
            self.store.update_document(uri, changes[0]["text"])

    def handle_textDocument_didClose(self, params: Dict) -> None:
        self.store.close_document(params["textDocument"]["uri"])

    def handle_textDocument_didSave(self, params: Dict) -> None:
        logger.info("Document saved: %s", params["textDocument"]["uri"])

    # ------------------------------------------------------------------
    # Document symbols
    # ------------------------------------------------------------------

    def handle_textDocument_documentSymbol(self, params: Dict) -> List[Dict]:
        uri = params["textDocument"]["uri"]
        doc = self.store.get_document(uri)
        if doc is None:
            return []
        return [s.to_dict() for s in doc.get_symbols()]

    # ------------------------------------------------------------------
    # Definition (follow links)
    # ------------------------------------------------------------------

    def handle_textDocument_definition(self, params: Dict) -> Optional[Dict]:
        """
        Go-to-definition: resolve a markdown link under the cursor.

        FIX (line 548): scan the *full document text* and map the global
        character offset back to (line, col), so multi-line links work.
        FIX (line 572): use uri_to_path() for cross-platform URI handling.
        """
        uri = params["textDocument"]["uri"]
        position = Position.from_dict(params["position"])

        doc = self.store.get_document(uri)
        if doc is None:
            return None

        # Convert (line, char) → flat character offset in full document text.
        offset = (
            sum(len(l) + 1 for l in doc.lines[: position.line]) + position.character
        )

        result = find_link_at_offset(doc.content, offset)
        if result is None:
            return None

        target, _, _ = result
        current_path = uri_to_path(uri)
        if current_path is None:
            return None

        target_path = (current_path.parent / target).resolve()
        return {
            "uri": target_path.as_uri(),
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 0},
            },
        }

    # ------------------------------------------------------------------
    # References (backlinks)
    # ------------------------------------------------------------------

    def handle_textDocument_references(self, params: Dict) -> List[Dict]:
        """
        Find all references to the symbol under the cursor across all open docs.

        FIX (line 739-741): iterate a snapshot to avoid holding the lock
        across graph traversal work.
        """
        uri = params["textDocument"]["uri"]
        position = Position.from_dict(params["position"])

        doc = self.store.get_document(uri)
        if doc is None:
            return []

        node = doc.get_node_at_position(position)
        if node is None:
            return []

        references: List[Dict] = []
        for doc_uri, document in self.store.snapshot().items():
            for ref in document.find_references(node.content):
                references.append(
                    {
                        "uri": doc_uri,
                        "range": {
                            "start": {"line": ref.line_start, "character": 0},
                            "end": {"line": ref.line_end, "character": 0},
                        },
                    }
                )

        return references

    # ------------------------------------------------------------------
    # Hover (breadcrumbs)
    # ------------------------------------------------------------------

    def handle_textDocument_hover(self, params: Dict) -> Optional[Dict]:
        uri = params["textDocument"]["uri"]
        position = Position.from_dict(params["position"])

        doc = self.store.get_document(uri)
        if doc is None:
            return None

        node = doc.get_node_at_position(position)
        if node is None:
            return None

        breadcrumbs = node.breadcrumbs()
        return {
            "contents": {
                "kind": "markdown",
                "value": (
                    f"**Path:** {breadcrumbs}\n\n"
                    f"**Type:** `{node.node_type}`\n\n"
                    f"**Level:** {node.level}"
                ),
            }
        }

    # ------------------------------------------------------------------
    # Code actions (extract section, etc.)
    # ------------------------------------------------------------------

    def handle_textDocument_codeAction(self, params: Dict) -> List[Dict]:
        uri = params["textDocument"]["uri"]
        range_data = Range.from_dict(params["range"])

        doc = self.store.get_document(uri)
        if doc is None:
            return []

        node = doc.get_node_at_position(range_data.start)
        if node is None or node.node_type != "header":
            return []

        return [
            {
                "title": f"Extract section: {node.content}",
                "kind": "refactor.extract",
                "command": {
                    "title": "Extract Section",
                    "command": "morphological.extractSection",
                    "arguments": [uri, node.id],
                },
            }
        ]

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def handle_textDocument_formatting(self, params: Dict) -> List[Dict]:
        """
        Minimal formatter: ensure a blank line precedes every ATX header
        and strip trailing whitespace from every line.
        """
        uri = params["textDocument"]["uri"]
        doc = self.store.get_document(uri)
        if doc is None:
            return []

        formatted: List[str] = []
        prev_blank = True  # treat start-of-file as blank

        for line in doc.lines:
            stripped = line.rstrip()
            is_header = stripped.startswith("#")
            if is_header and formatted and not prev_blank:
                formatted.append("")
            formatted.append(stripped)
            prev_blank = stripped == ""

        new_text = "\n".join(formatted)
        return [
            {
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": len(doc.lines), "character": 0},
                },
                "newText": new_text,
            }
        ]

    # ------------------------------------------------------------------
    # Completion
    # ------------------------------------------------------------------

    def handle_textDocument_completion(self, params: Dict) -> Dict:
        """
        Completion for markdown link labels when the cursor is right after '['.

        FIX (line 621): use _cursor_inside_open_bracket() to avoid firing
        completions mid-link or for unrelated '[' characters.
        """
        uri = params["textDocument"]["uri"]
        position = Position.from_dict(params["position"])

        doc = self.store.get_document(uri)
        if doc is None or position.line >= len(doc.lines):
            return {"items": []}

        line = doc.lines[position.line]

        if not _cursor_inside_open_bracket(line, position.character):
            return {"items": []}

        items: List[Dict] = []
        for doc_uri, document in self.store.snapshot().items():
            for node in document.nodes.values():
                if node.node_type == "header":
                    items.append(
                        {
                            "label": node.content,
                            "kind": 1,  # Text
                            "insertText": f"{node.content}]({doc_uri})",
                            "documentation": f"Link to: {node.breadcrumbs()}",
                        }
                    )

        return {"items": items}


# ============================================================================
# MAIN SERVER LOOP
# ============================================================================


def main() -> None:
    logger.info("Starting Morphological-IWE LSP Server")
    logger.info("Python: %s", sys.version)
    logger.info("Debug mode: %s", bool(os.getenv("IWE_DEBUG")))

    server = MorphologicalLSP()

    try:
        while True:
            message = LSPMessage.read_message(sys.stdin.buffer)
            if message is None:
                break

            response = server.handle_message(message)
            if response is not None:
                LSPMessage.write_message(sys.stdout.buffer, response)

    except KeyboardInterrupt:
        logger.info("Server interrupted")
    except Exception:
        logger.error("Fatal error", exc_info=True)
    finally:
        logger.info("Server shutdown")


if __name__ == "__main__":
    main()
