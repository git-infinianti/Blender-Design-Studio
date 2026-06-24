"""Core pattern data model for Blender Design Studio

Simple data containers to start with; will be expanded during implementation.
"""
from dataclasses import dataclass, field
from typing import List, Tuple
from mathutils import Vector


@dataclass
class PatternPiece:
    name: str
    verts: List[Vector] = field(default_factory=list)  # 2D coordinates (x, y)
    edges: List[Tuple[int, int]] = field(default_factory=list)

    def add_vertex(self, x: float, y: float):
        self.verts.append(Vector((x, y)))
        return len(self.verts) - 1

    def add_edge(self, a: int, b: int):
        self.edges.append((a, b))


@dataclass
class PatternCollection:
    pieces: List[PatternPiece] = field(default_factory=list)

    def new_piece(self, name: str) -> PatternPiece:
        p = PatternPiece(name)
        self.pieces.append(p)
        return p
