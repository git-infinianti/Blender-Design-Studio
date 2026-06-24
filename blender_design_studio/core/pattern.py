"""Core pattern data model for Blender Design Studio"""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from mathutils import Vector
import math


@dataclass
class PatternPiece:
    name: str
    verts: List[Vector] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)
    internal_lines: List[Tuple[int, int]] = field(default_factory=list)
    seam_allowance: float = 0.01
    fabric_id: str = "default"
    uv_island_index: int = -1

    def add_vertex(self, x: float, y: float) -> int:
        self.verts.append(Vector((x, y)))
        return len(self.verts) - 1

    def add_edge(self, a: int, b: int):
        self.edges.append((a, b))

    def add_internal_line(self, a: int, b: int):
        self.internal_lines.append((a, b))

    def remove_vertex(self, index: int):
        """Remove vertex and all edges referencing it."""
        if 0 <= index < len(self.verts):
            self.verts.pop(index)
            self.edges = [
                (a - (1 if a > index else 0), b - (1 if b > index else 0))
                for a, b in self.edges
                if a != index and b != index
            ]
            self.internal_lines = [
                (a - (1 if a > index else 0), b - (1 if b > index else 0))
                for a, b in self.internal_lines
                if a != index and b != index
            ]

    def remove_edge(self, a: int, b: int):
        """Remove edge between vertices a and b."""
        self.edges = [
            (ea, eb) for ea, eb in self.edges
            if not ((ea == a and eb == b) or (ea == b and eb == a))
        ]

    def get_boundary_verts(self) -> List[Vector]:
        """Return ordered boundary vertices."""
        if not self.edges:
            return list(self.verts)
        adj: Dict[int, List[int]] = {}
        for a, b in self.edges:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        if not adj:
            return []
        visited = set()
        ordered = []
        current = self.edges[0][0]
        while current not in visited:
            visited.add(current)
            ordered.append(self.verts[current])
            neighbors = adj.get(current, [])
            next_v = None
            for n in neighbors:
                if n not in visited:
                    next_v = n
                    break
            if next_v is None:
                break
            current = next_v
        return ordered

    def triangulate(self) -> Tuple[List[Vector], List[Tuple[int, int, int]]]:
        """Constrained Delaunay triangulation of the pattern piece.

        Uses ear-clipping as a fallback when the triangle library is not available.
        """
        boundary = self.get_boundary_verts()
        if len(boundary) < 3:
            return list(self.verts), []

        try:
            import triangle as tr
            import numpy as np

            verts_2d = [(v.x, v.y) for v in boundary]
            segments = [(i, (i + 1) % len(verts_2d)) for i in range(len(verts_2d))]
            data = {
                'vertices': np.array(verts_2d),
                'segments': np.array(segments),
            }
            result = tr.triangulate(data, 'p')
            out_verts = [Vector((v[0], v[1])) for v in result['vertices']]
            out_tris = [tuple(tri) for tri in result['triangles']]
            return out_verts, out_tris
        except ImportError:
            return self._ear_clip_triangulate(boundary)

    def _ear_clip_triangulate(
        self,
        boundary: List[Vector],
    ) -> Tuple[List[Vector], List[Tuple[int, int, int]]]:
        """Simple ear-clipping triangulation fallback."""
        if len(boundary) < 3:
            return list(boundary), []

        tris = []
        indices = list(range(len(boundary)))

        while len(indices) > 2:
            ear_found = False
            n = len(indices)
            for i in range(n):
                prev_i = indices[(i - 1) % n]
                curr_i = indices[i]
                next_i = indices[(i + 1) % n]

                v_prev = boundary[prev_i]
                v_curr = boundary[curr_i]
                v_next = boundary[next_i]

                cross = (
                    (v_curr.x - v_prev.x) * (v_next.y - v_prev.y)
                    - (v_curr.y - v_prev.y) * (v_next.x - v_prev.x)
                )

                if cross <= 0:
                    continue

                is_ear = True
                for j in range(n):
                    if j in (i, (i - 1) % n, (i + 1) % n):
                        continue
                    p = boundary[indices[j]]
                    if self._point_in_triangle(p, v_prev, v_curr, v_next):
                        is_ear = False
                        break

                if is_ear:
                    tris.append((prev_i, curr_i, next_i))
                    indices.pop(i)
                    ear_found = True
                    break

            if not ear_found:
                break

        return list(boundary), tris

    @staticmethod
    def _point_in_triangle(p: Vector, a: Vector, b: Vector, c: Vector) -> bool:
        """Check if point p is inside triangle abc using barycentric coordinates."""
        denom = (b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)
        if abs(denom) < 1e-10:
            return False
        u = ((b.y - c.y) * (p.x - c.x) + (c.x - b.x) * (p.y - c.y)) / denom
        v = ((c.y - a.y) * (p.x - c.x) + (a.x - c.x) * (p.y - c.y)) / denom
        w = 1.0 - u - v
        return u >= 0 and v >= 0 and w >= 0

    def offset_boundary(self, distance: float) -> 'PatternPiece':
        """Generate seam-allowance offset curve."""
        boundary = self.get_boundary_verts()
        if len(boundary) < 3:
            return PatternPiece(name=f"{self.name}_offset")

        offset_verts = []
        n = len(boundary)
        for i in range(n):
            prev_v = boundary[(i - 1) % n]
            curr_v = boundary[i]
            next_v = boundary[(i + 1) % n]

            e1 = Vector((curr_v.x - prev_v.x, curr_v.y - prev_v.y))
            e2 = Vector((next_v.x - curr_v.x, next_v.y - curr_v.y))

            n1 = Vector((-e1.y, e1.x))
            n2 = Vector((-e2.y, e2.x))

            if n1.length > 0:
                n1.normalize()
            if n2.length > 0:
                n2.normalize()

            avg_n = n1 + n2
            if avg_n.length > 0:
                avg_n.normalize()

            offset_verts.append(Vector((
                curr_v.x + avg_n.x * distance,
                curr_v.y + avg_n.y * distance,
            )))

        piece = PatternPiece(name=f"{self.name}_offset")
        piece.verts = offset_verts
        piece.edges = [(i, (i + 1) % len(offset_verts)) for i in range(len(offset_verts))]
        return piece

    def mirror(self, axis: str = 'X') -> 'PatternPiece':
        """Mirror pattern piece across the given axis."""
        mirrored = PatternPiece(
            name=f"{self.name}_mirrored",
            edges=list(self.edges),
            internal_lines=list(self.internal_lines),
            seam_allowance=self.seam_allowance,
            fabric_id=self.fabric_id,
        )
        for v in self.verts:
            if axis == 'X':
                mirrored.verts.append(Vector((-v.x, v.y)))
            else:
                mirrored.verts.append(Vector((v.x, -v.y)))
        return mirrored

    def compute_area(self) -> float:
        """Compute the area using the shoelace formula on boundary vertices."""
        boundary = self.get_boundary_verts()
        n = len(boundary)
        if n < 3:
            return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += boundary[i].x * boundary[j].y
            area -= boundary[j].x * boundary[i].y
        return abs(area) / 2.0

    def compute_perimeter(self) -> float:
        """Compute the perimeter length of the boundary."""
        boundary = self.get_boundary_verts()
        if len(boundary) < 2:
            return 0.0
        perimeter = 0.0
        for i in range(len(boundary)):
            j = (i + 1) % len(boundary)
            perimeter += (boundary[j] - boundary[i]).length
        return perimeter


@dataclass
class PatternCollection:
    pieces: List[PatternPiece] = field(default_factory=list)

    def new_piece(self, name: str) -> PatternPiece:
        p = PatternPiece(name)
        self.pieces.append(p)
        return p

    def get_piece(self, name: str) -> Optional[PatternPiece]:
        for p in self.pieces:
            if p.name == name:
                return p
        return None

    def remove_piece(self, name: str) -> bool:
        for i, p in enumerate(self.pieces):
            if p.name == name:
                self.pieces.pop(i)
                return True
        return False

    def piece_names(self) -> List[str]:
        return [p.name for p in self.pieces]
