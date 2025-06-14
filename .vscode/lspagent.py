#!/usr/bin/env python3
"""
Markdown Agent - Bridge between LSP actions and ontological computing
Usage: md_agent.py {extract|inline|quantum_state|morphic_transform} [args...]
"""

import sys
import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Import your ontology classes (assuming they're available)
try:
    from your_ontology import BYTE, QuantumState, HilbertSpace, MorphicComplex, least_significant_unit, WordSize
    ONTOLOGY_AVAILABLE = True
except ImportError:
    ONTOLOGY_AVAILABLE = False
    print("Warning: Ontology classes not available, running in basic mode", file=sys.stderr)


class ActionType(Enum):
    EXTRACT = "extract"
    INLINE = "inline"
    QUANTUM_STATE = "quantum_state"
    MORPHIC_TRANSFORM = "morphic_transform"
    ANALYZE = "analyze"


@dataclass
class DocumentState:
    """Represents the state of a document in our ontological framework"""
    path: str
    content: str
    hash: str
    sections: List[Dict[str, Any]]
    quantum_state: Optional[Any] = None
    morphic_signature: Optional[str] = None


class MarkdownAgent:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.state_file = self.workspace_root / ".md_agent_state.json"
        self.extracted_dir = self.workspace_root / ".extracted"
        self.extracted_dir.mkdir(exist_ok=True)

        # Load or initialize persistent state
        self.state = self._load_state()

        # Initialize ontological structures if available
        if ONTOLOGY_AVAILABLE:
            self.hilbert_space = HilbertSpace(
                dimension=8)  # 8D for BYTE compatibility
            self._init_quantum_operators()

    def _load_state(self) -> Dict[str, Any]:
        """Load persistent state from JSON file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"documents": {}, "extractions": {}, "quantum_states": {}}

    def _save_state(self):
        """Save current state to JSON file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state: {e}", file=sys.stderr)

    def _init_quantum_operators(self):
        """Initialize quantum operators for document transformation"""
        if not ONTOLOGY_AVAILABLE:
            return

        # Create basic quantum operators for text manipulation
        # These could represent different types of document transformations
        self.extract_operator = self._create_extract_operator()
        self.inline_operator = self._create_inline_operator()

    def _create_extract_operator(self):
        """Create quantum operator for extraction operations"""
        if not ONTOLOGY_AVAILABLE:
            return None

        # Example: Create a simple extraction operator
        # In practice, this would be more sophisticated
        from your_ontology import QuantumOperator
        return QuantumOperator(self.hilbert_space)

    def _create_inline_operator(self):
        """Create quantum operator for inline operations"""
        if not ONTOLOGY_AVAILABLE:
            return None

        from your_ontology import QuantumOperator
        return QuantumOperator(self.hilbert_space)

    def _compute_document_hash(self, content: str) -> str:
        """Compute hash of document content"""
        return hashlib.sha256(content.encode()).hexdigest()[:8]

    def _generate_note_id(self, content: str) -> str:
        """Generate unique note ID similar to iwe's format"""
        hash_input = content + str(len(self.state["extractions"]))
        return hashlib.sha256(hash_input.encode()).hexdigest()[:8]

    def _parse_markdown_sections(self, content: str) -> List[Dict[str, Any]]:
        """Parse markdown content into sections"""
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []

        for i, line in enumerate(lines):
            if re.match(r'^#{1,6}\s+', line):
                # Save previous section if exists
                if current_section:
                    current_section['content'] = '\n'.join(current_content)
                    current_section['end_line'] = i - 1
                    sections.append(current_section)

                # Start new section
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                current_section = {
                    'level': level,
                    'title': title,
                    'start_line': i,
                    'content': '',
                    'end_line': i
                }
                current_content = [line]
            else:
                if current_section:
                    current_content.append(line)

        # Save last section
        if current_section:
            current_section['content'] = '\n'.join(current_content)
            current_section['end_line'] = len(lines) - 1
            sections.append(current_section)

        return sections

    def _compute_morphic_signature(self, content: str) -> str:
        """Compute morphic signature using ontological functions"""
        if not ONTOLOGY_AVAILABLE:
            return self._compute_document_hash(content)

        # Use your ontology to compute a more sophisticated signature
        state_hash = least_significant_unit(content, WordSize.LONG)
        byte_representation = BYTE(state_hash & 0xFF)
        return f"morphic_{byte_representation.value:02x}_{state_hash:08x}"

    def _create_quantum_state_from_content(self, content: str):
        """Create quantum state representation of document content"""
        if not ONTOLOGY_AVAILABLE:
            return None

        # Simple mapping: use content characteristics to create amplitudes
        lines = content.split('\n')
        sections = self._parse_markdown_sections(content)

        # Create amplitudes based on document structure
        amplitudes = []
        for i in range(self.hilbert_space.dimension):
            if i < len(sections):
                section = sections[i]
                # Use section characteristics to determine amplitude
                real_part = len(section['content']) / 1000.0  # Normalize
                imag_part = section['level'] / 10.0  # Use heading level
            else:
                real_part = 0.1  # Small default
                imag_part = 0.0

            amplitudes.append(MorphicComplex(real_part, imag_part))

        return QuantumState(amplitudes, self.hilbert_space)

    def extract_section(self, document_path: str, cursor_line: int = None) -> Dict[str, Any]:
        """Extract a section from a document"""
        doc_path = Path(document_path)
        if not doc_path.exists():
            return {"error": f"Document {document_path} not found"}

        with open(doc_path, 'r') as f:
            content = f.read()

        sections = self._parse_markdown_sections(content)

        # Find section to extract (by cursor line or other criteria)
        target_section = None
        if cursor_line is not None:
            for section in sections:
                if section['start_line'] <= cursor_line <= section['end_line']:
                    target_section = section
                    break

        if not target_section:
            return {"error": "No section found to extract"}

        # Generate note ID and create extracted file
        note_id = self._generate_note_id(target_section['content'])
        extracted_path = self.extracted_dir / f"{note_id}.md"

        # Write extracted content
        with open(extracted_path, 'w') as f:
            f.write(target_section['content'])

        # Create link to replace the section
        link_text = f"[{target_section['title']}]({note_id})"

        # Update original document
        lines = content.split('\n')
        new_lines = (
            lines[:target_section['start_line']] +
            [link_text] +
            lines[target_section['end_line'] + 1:]
        )
        new_content = '\n'.join(new_lines)

        with open(doc_path, 'w') as f:
            f.write(new_content)

        # Update state
        self.state["extractions"][note_id] = {
            "original_doc": str(doc_path),
            "extracted_path": str(extracted_path),
            "title": target_section['title'],
            "original_content": target_section['content']
        }

        # Compute ontological signatures
        if ONTOLOGY_AVAILABLE:
            morphic_sig = self._compute_morphic_signature(
                target_section['content'])
            quantum_state = self._create_quantum_state_from_content(
                target_section['content'])

            self.state["quantum_states"][note_id] = {
                "morphic_signature": morphic_sig,
                "dimension": self.hilbert_space.dimension,
                "amplitudes": [(amp.real, amp.imag) for amp in quantum_state.amplitudes] if quantum_state else []
            }

        self._save_state()

        return {
            "success": True,
            "note_id": note_id,
            "extracted_path": str(extracted_path),
            "link_text": link_text
        }

    def inline_section(self, document_path: str, note_id: str) -> Dict[str, Any]:
        """Inline a previously extracted section"""
        doc_path = Path(document_path)
        if not doc_path.exists():
            return {"error": f"Document {document_path} not found"}

        if note_id not in self.state["extractions"]:
            return {"error": f"No extraction record found for {note_id}"}

        extraction_info = self.state["extractions"][note_id]
        extracted_path = Path(extraction_info["extracted_path"])

        if not extracted_path.exists():
            return {"error": f"Extracted file {extracted_path} not found"}

        # Read current content of extracted file
        with open(extracted_path, 'r') as f:
            extracted_content = f.read()

        # Read original document
        with open(doc_path, 'r') as f:
            doc_content = f.read()

        # Replace link with content
        link_pattern = rf"\[{re.escape(extraction_info['title'])}\]\({re.escape(note_id)}\)"
        new_content = re.sub(link_pattern, extracted_content, doc_content)

        # Write updated document
        with open(doc_path, 'w') as f:
            f.write(new_content)

        return {
            "success": True,
            "inlined_content": extracted_content,
            "note_id": note_id,
            "message": f"Content inlined. Extracted file {extracted_path} still exists."
        }

    def analyze_document(self, document_path: str) -> Dict[str, Any]:
        """Analyze document using ontological framework"""
        doc_path = Path(document_path)
        if not doc_path.exists():
            return {"error": f"Document {document_path} not found"}

        with open(doc_path, 'r') as f:
            content = f.read()

        analysis = {
            "path": str(doc_path),
            "content_hash": self._compute_document_hash(content),
            "sections": self._parse_markdown_sections(content),
            "line_count": len(content.split('\n')),
            "char_count": len(content)
        }

        if ONTOLOGY_AVAILABLE:
            analysis["morphic_signature"] = self._compute_morphic_signature(
                content)
            quantum_state = self._create_quantum_state_from_content(content)
            if quantum_state:
                analysis["quantum_state"] = {
                    "dimension": self.hilbert_space.dimension,
                    "amplitudes": [(amp.real, amp.imag) for amp in quantum_state.amplitudes],
                    "norm": self.hilbert_space.norm(quantum_state.amplitudes)
                }

        return analysis

    def morphic_transform(self, document_path: str, transform_type: str = "identity") -> Dict[str, Any]:
        """Apply morphic transformation to document"""
        if not ONTOLOGY_AVAILABLE:
            return {"error": "Ontology not available for morphic operations"}

        doc_path = Path(document_path)
        if not doc_path.exists():
            return {"error": f"Document {document_path} not found"}

        with open(doc_path, 'r') as f:
            content = f.read()

        # Create quantum state from content
        quantum_state = self._create_quantum_state_from_content(content)
        if not quantum_state:
            return {"error": "Could not create quantum state from content"}

        # Apply transformation based on type
        if transform_type == "extract":
            operator = self.extract_operator
        elif transform_type == "inline":
            operator = self.inline_operator
        else:
            # Identity transformation
            from your_ontology import QuantumOperator
            operator = QuantumOperator(self.hilbert_space)

        # Apply operator to quantum state
        if operator:
            operator.apply_to(quantum_state)

        return {
            "success": True,
            "transform_type": transform_type,
            "final_state": {
                "amplitudes": [(amp.real, amp.imag) for amp in quantum_state.amplitudes],
                "norm": self.hilbert_space.norm(quantum_state.amplitudes)
            }
        }


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: md_agent.py {extract|inline|analyze|morphic_transform} [args...]")
        sys.exit(1)

    action = sys.argv[1]
    agent = MarkdownAgent()

    try:
        if action == "extract":
            document_path = sys.argv[2] if len(sys.argv) > 2 else "."
            cursor_line = int(sys.argv[3]) if len(sys.argv) > 3 else None
            result = agent.extract_section(document_path, cursor_line)

        elif action == "inline":
            document_path = sys.argv[2] if len(sys.argv) > 2 else "."
            note_id = sys.argv[3] if len(sys.argv) > 3 else ""
            result = agent.inline_section(document_path, note_id)

        elif action == "analyze":
            document_path = sys.argv[2] if len(sys.argv) > 2 else "."
            result = agent.analyze_document(document_path)

        elif action == "morphic_transform":
            document_path = sys.argv[2] if len(sys.argv) > 2 else "."
            transform_type = sys.argv[3] if len(sys.argv) > 3 else "identity"
            result = agent.morphic_transform(document_path, transform_type)

        else:
            result = {"error": f"Unknown action: {action}"}

        # Output result as JSON for LSP consumption
        print(json.dumps(result, indent=2))

    except Exception as e:
        error_result = {"error": str(e)}
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
