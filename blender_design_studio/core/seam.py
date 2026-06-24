"""Seam and stitch definitions for garment assembly."""
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class SeamSegment:
    """Links two edge sequences across pattern pieces."""
    piece_a: str
    edge_indices_a: List[int] = field(default_factory=list)
    piece_b: str = ""
    edge_indices_b: List[int] = field(default_factory=list)
    stitch_type: str = "normal"
    strength: float = 1.0

    def is_valid(self) -> bool:
        """Check if seam has matching edge counts."""
        return (
            len(self.edge_indices_a) > 0
            and len(self.edge_indices_b) > 0
            and len(self.edge_indices_a) == len(self.edge_indices_b)
        )


@dataclass
class SeamCollection:
    """Container for all seams in a garment."""
    seams: List[SeamSegment] = field(default_factory=list)

    def add_seam(
        self,
        piece_a: str,
        edges_a: List[int],
        piece_b: str,
        edges_b: List[int],
        stitch_type: str = "normal",
        strength: float = 1.0,
    ) -> SeamSegment:
        """Create and add a new seam segment."""
        seam = SeamSegment(
            piece_a=piece_a,
            edge_indices_a=edges_a,
            piece_b=piece_b,
            edge_indices_b=edges_b,
            stitch_type=stitch_type,
            strength=strength,
        )
        self.seams.append(seam)
        return seam

    def remove_seam(self, index: int) -> bool:
        """Remove seam at given index."""
        if 0 <= index < len(self.seams):
            self.seams.pop(index)
            return True
        return False

    def find_seams_for_piece(self, piece_name: str) -> List[SeamSegment]:
        """Return all seams involving a given piece."""
        return [
            s for s in self.seams
            if s.piece_a == piece_name or s.piece_b == piece_name
        ]

    def build_constraint_pairs(self) -> List[Tuple[int, int]]:
        """Return global vertex-index pairs that must be merged.

        This maps edge indices to global vertex indices based on
        piece ordering in the assembled mesh.
        """
        pairs = []
        for seam in self.seams:
            if not seam.is_valid():
                continue
            for idx_a, idx_b in zip(seam.edge_indices_a, seam.edge_indices_b):
                pairs.append((idx_a, idx_b))
        return pairs

    def validate(self) -> List[str]:
        """Return list of validation error messages."""
        errors = []
        for i, seam in enumerate(self.seams):
            if not seam.is_valid():
                errors.append(
                    f"Seam {i}: edge count mismatch "
                    f"({len(seam.edge_indices_a)} vs {len(seam.edge_indices_b)})"
                )
        return errors
