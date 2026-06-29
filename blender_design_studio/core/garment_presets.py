"""Garment template presets for quick clothing construction.

Provides pre-built pattern templates for common garment types
(t-shirt, skirt, pants, dress, jacket) that can be loaded and
customized. This is a differentiating feature not found in
typical cloth simulation addons.
"""
from typing import List, Tuple, Dict
from mathutils import Vector

from .pattern import PatternPiece, PatternCollection
from .seam import SeamSegment, SeamCollection


# Each preset is defined by pattern piece outlines (2D vertices),
# edges connecting them, and seam pairings between pieces.


def _make_piece(name: str, verts: List[Tuple[float, float]],
                edges: List[Tuple[int, int]]) -> PatternPiece:
    """Helper to construct a PatternPiece from coordinate tuples."""
    piece = PatternPiece(name=name)
    piece.verts = [Vector((x, y, 0.0)) for x, y in verts]
    piece.edges = list(edges)
    return piece


# ---------- T-Shirt Template ----------

def _tshirt_front() -> PatternPiece:
    """Front panel of a basic t-shirt."""
    verts = [
        (0.0, 0.0), (0.3, 0.0), (0.3, 0.05), (0.35, 0.1),
        (0.35, 0.45), (0.3, 0.5), (0.2, 0.52), (0.15, 0.52),
        (0.1, 0.52), (0.0, 0.5), (-0.05, 0.45), (-0.05, 0.1),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("tshirt_front", verts, edges)


def _tshirt_back() -> PatternPiece:
    """Back panel of a basic t-shirt."""
    verts = [
        (0.0, 0.0), (0.3, 0.0), (0.3, 0.05), (0.35, 0.1),
        (0.35, 0.45), (0.3, 0.5), (0.2, 0.53), (0.15, 0.54),
        (0.1, 0.53), (0.0, 0.5), (-0.05, 0.45), (-0.05, 0.1),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("tshirt_back", verts, edges)


def _tshirt_sleeve() -> PatternPiece:
    """Sleeve piece for a basic t-shirt."""
    verts = [
        (0.0, 0.0), (0.2, 0.0), (0.22, 0.05), (0.2, 0.2),
        (0.15, 0.22), (0.05, 0.22), (0.0, 0.2), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("tshirt_sleeve", verts, edges)


# ---------- Skirt Template ----------

def _skirt_panel() -> PatternPiece:
    """A single panel for an A-line skirt (use 4-6 panels)."""
    verts = [
        (0.0, 0.0), (0.12, 0.0), (0.15, 0.4), (0.08, 0.42),
        (0.04, 0.42), (-0.03, 0.4),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    return _make_piece("skirt_panel", verts, edges)


# ---------- Pants Template ----------

def _pants_front_leg() -> PatternPiece:
    """Front leg panel for basic pants."""
    verts = [
        (0.0, 0.0), (0.15, 0.0), (0.16, 0.3), (0.18, 0.35),
        (0.18, 0.7), (0.14, 0.72), (0.06, 0.72), (0.0, 0.7),
        (0.0, 0.35), (-0.02, 0.3),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("pants_front_leg", verts, edges)


def _pants_back_leg() -> PatternPiece:
    """Back leg panel for basic pants."""
    verts = [
        (0.0, 0.0), (0.16, 0.0), (0.18, 0.3), (0.20, 0.35),
        (0.20, 0.7), (0.15, 0.73), (0.06, 0.73), (0.0, 0.7),
        (0.0, 0.35), (-0.02, 0.3),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("pants_back_leg", verts, edges)


# ---------- Hoodie Template ----------

def _hoodie_front() -> PatternPiece:
    """Front panel of a hoodie."""
    verts = [
        (0.0, 0.0), (0.32, 0.0), (0.32, 0.05), (0.37, 0.12),
        (0.37, 0.48), (0.32, 0.55), (0.22, 0.58), (0.15, 0.58),
        (0.1, 0.58), (0.0, 0.55), (-0.05, 0.48), (-0.05, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("hoodie_front", verts, edges)


def _hoodie_back() -> PatternPiece:
    """Back panel of a hoodie."""
    verts = [
        (0.0, 0.0), (0.32, 0.0), (0.32, 0.05), (0.37, 0.12),
        (0.37, 0.48), (0.32, 0.55), (0.22, 0.59), (0.15, 0.60),
        (0.1, 0.59), (0.0, 0.55), (-0.05, 0.48), (-0.05, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("hoodie_back", verts, edges)


def _hoodie_sleeve() -> PatternPiece:
    """Long sleeve for a hoodie."""
    verts = [
        (0.0, 0.0), (0.18, 0.0), (0.20, 0.05), (0.19, 0.35),
        (0.15, 0.38), (0.05, 0.38), (0.0, 0.35), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("hoodie_sleeve", verts, edges)


def _hoodie_hood() -> PatternPiece:
    """Hood piece for a hoodie."""
    verts = [
        (0.0, 0.0), (0.2, 0.0), (0.25, 0.1), (0.25, 0.25),
        (0.2, 0.3), (0.1, 0.32), (0.0, 0.3), (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("hoodie_hood", verts, edges)


# ---------- Tank Top Template ----------

def _tank_top_front() -> PatternPiece:
    """Front panel of a tank top."""
    verts = [
        (0.0, 0.0), (0.25, 0.0), (0.25, 0.05), (0.26, 0.1),
        (0.26, 0.35), (0.22, 0.4), (0.18, 0.42), (0.12, 0.42),
        (0.08, 0.42), (0.04, 0.4), (0.0, 0.35), (-0.01, 0.1),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("tank_top_front", verts, edges)


def _tank_top_back() -> PatternPiece:
    """Back panel of a tank top."""
    verts = [
        (0.0, 0.0), (0.25, 0.0), (0.25, 0.05), (0.26, 0.1),
        (0.26, 0.35), (0.22, 0.4), (0.18, 0.43), (0.12, 0.44),
        (0.08, 0.43), (0.04, 0.4), (0.0, 0.35), (-0.01, 0.1),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("tank_top_back", verts, edges)


# ---------- Bomber Jacket Template ----------

def _bomber_front() -> PatternPiece:
    """Front panel of a bomber jacket."""
    verts = [
        (0.0, 0.0), (0.3, 0.0), (0.3, 0.05), (0.36, 0.12),
        (0.36, 0.5), (0.3, 0.55), (0.2, 0.57), (0.15, 0.57),
        (0.1, 0.57), (0.0, 0.55), (-0.06, 0.5), (-0.06, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("bomber_front", verts, edges)


def _bomber_back() -> PatternPiece:
    """Back panel of a bomber jacket."""
    verts = [
        (0.0, 0.0), (0.34, 0.0), (0.34, 0.05), (0.38, 0.12),
        (0.38, 0.5), (0.34, 0.55), (0.22, 0.58), (0.17, 0.59),
        (0.12, 0.58), (0.0, 0.55), (-0.04, 0.5), (-0.04, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("bomber_back", verts, edges)


def _bomber_sleeve() -> PatternPiece:
    """Sleeve piece for a bomber jacket."""
    verts = [
        (0.0, 0.0), (0.2, 0.0), (0.22, 0.05), (0.21, 0.38),
        (0.16, 0.4), (0.04, 0.4), (0.0, 0.38), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("bomber_sleeve", verts, edges)


def _bomber_collar() -> PatternPiece:
    """Ribbed collar piece for a bomber jacket."""
    verts = [
        (0.0, 0.0), (0.3, 0.0), (0.3, 0.06), (0.0, 0.06),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    return _make_piece("bomber_collar", verts, edges)


# ---------- Dress Template ----------

def _dress_bodice_front() -> PatternPiece:
    """Front bodice for a simple dress."""
    verts = [
        (0.0, 0.0), (0.25, 0.0), (0.27, 0.15), (0.25, 0.3),
        (0.2, 0.32), (0.12, 0.33), (0.05, 0.32), (0.0, 0.3),
        (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("dress_bodice_front", verts, edges)


def _dress_skirt() -> PatternPiece:
    """Skirt portion of a simple dress (full circle approximation)."""
    verts = [
        (0.0, 0.0), (0.25, 0.0), (0.3, 0.2), (0.28, 0.5),
        (0.2, 0.6), (0.12, 0.62), (0.05, 0.6), (-0.03, 0.5),
        (-0.05, 0.2),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("dress_skirt", verts, edges)


# ---------- Cardigan Template ----------

def _cardigan_left_front() -> PatternPiece:
    """Left front panel of a cardigan (open-front)."""
    verts = [
        (0.0, 0.0), (0.15, 0.0), (0.15, 0.05), (0.17, 0.12),
        (0.17, 0.48), (0.13, 0.52), (0.08, 0.53), (0.0, 0.52),
        (-0.02, 0.12), (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("cardigan_left_front", verts, edges)


def _cardigan_back() -> PatternPiece:
    """Back panel of a cardigan."""
    verts = [
        (0.0, 0.0), (0.30, 0.0), (0.30, 0.05), (0.33, 0.12),
        (0.33, 0.48), (0.28, 0.52), (0.18, 0.54), (0.12, 0.54),
        (0.05, 0.52), (0.0, 0.48), (-0.03, 0.12), (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    ]
    return _make_piece("cardigan_back", verts, edges)


def _cardigan_sleeve() -> PatternPiece:
    """Long sleeve for a cardigan."""
    verts = [
        (0.0, 0.0), (0.17, 0.0), (0.19, 0.05), (0.18, 0.36),
        (0.14, 0.38), (0.04, 0.38), (0.0, 0.36), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("cardigan_sleeve", verts, edges)


# ---------- Crop Top Template ----------

def _crop_top_front() -> PatternPiece:
    """Front panel of a crop top."""
    verts = [
        (0.0, 0.0), (0.24, 0.0), (0.24, 0.04), (0.26, 0.08),
        (0.26, 0.22), (0.22, 0.26), (0.16, 0.28), (0.10, 0.28),
        (0.04, 0.26), (0.0, 0.22), (-0.02, 0.08), (0.0, 0.04),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    ]
    return _make_piece("crop_top_front", verts, edges)


def _crop_top_back() -> PatternPiece:
    """Back panel of a crop top."""
    verts = [
        (0.0, 0.0), (0.24, 0.0), (0.24, 0.04), (0.26, 0.08),
        (0.26, 0.22), (0.22, 0.26), (0.16, 0.29), (0.10, 0.29),
        (0.04, 0.26), (0.0, 0.22), (-0.02, 0.08), (0.0, 0.04),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    ]
    return _make_piece("crop_top_back", verts, edges)


# ---------- Pencil Skirt Template ----------

def _pencil_skirt_front() -> PatternPiece:
    """Front panel of a pencil skirt."""
    verts = [
        (0.0, 0.0), (0.14, 0.0), (0.15, 0.25), (0.14, 0.5),
        (0.13, 0.55), (0.07, 0.56), (0.0, 0.55), (-0.01, 0.5),
        (-0.01, 0.25),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("pencil_skirt_front", verts, edges)


def _pencil_skirt_back() -> PatternPiece:
    """Back panel of a pencil skirt."""
    verts = [
        (0.0, 0.0), (0.14, 0.0), (0.15, 0.25), (0.14, 0.5),
        (0.13, 0.56), (0.07, 0.57), (0.0, 0.56), (-0.01, 0.5),
        (-0.01, 0.25),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("pencil_skirt_back", verts, edges)


# ---------- Trench Coat Template ----------

def _trench_front() -> PatternPiece:
    """Front panel of a trench coat."""
    verts = [
        (0.0, 0.0), (0.34, 0.0), (0.34, 0.05), (0.38, 0.14),
        (0.38, 0.65), (0.34, 0.70), (0.22, 0.73), (0.17, 0.73),
        (0.10, 0.73), (0.0, 0.70), (-0.04, 0.65), (-0.04, 0.14),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("trench_front", verts, edges)


def _trench_back() -> PatternPiece:
    """Back panel of a trench coat."""
    verts = [
        (0.0, 0.0), (0.36, 0.0), (0.36, 0.05), (0.40, 0.14),
        (0.40, 0.65), (0.36, 0.70), (0.24, 0.74), (0.18, 0.75),
        (0.12, 0.74), (0.0, 0.70), (-0.04, 0.65), (-0.04, 0.14),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("trench_back", verts, edges)


def _trench_sleeve() -> PatternPiece:
    """Long sleeve for a trench coat."""
    verts = [
        (0.0, 0.0), (0.20, 0.0), (0.22, 0.05), (0.21, 0.42),
        (0.16, 0.44), (0.04, 0.44), (0.0, 0.42), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("trench_sleeve", verts, edges)


# ---------- Polo Shirt Template ----------

def _polo_front() -> PatternPiece:
    """Front panel of a polo shirt."""
    verts = [
        (0.0, 0.0), (0.28, 0.0), (0.28, 0.05), (0.32, 0.10),
        (0.32, 0.42), (0.28, 0.47), (0.18, 0.49), (0.14, 0.49),
        (0.08, 0.49), (0.0, 0.47), (-0.04, 0.42), (-0.04, 0.10),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("polo_front", verts, edges)


def _polo_back() -> PatternPiece:
    """Back panel of a polo shirt."""
    verts = [
        (0.0, 0.0), (0.28, 0.0), (0.28, 0.05), (0.32, 0.10),
        (0.32, 0.42), (0.28, 0.47), (0.18, 0.50), (0.14, 0.51),
        (0.08, 0.50), (0.0, 0.47), (-0.04, 0.42), (-0.04, 0.10),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("polo_back", verts, edges)


def _polo_sleeve() -> PatternPiece:
    """Short sleeve for a polo shirt."""
    verts = [
        (0.0, 0.0), (0.18, 0.0), (0.20, 0.05), (0.18, 0.18),
        (0.14, 0.20), (0.04, 0.20), (0.0, 0.18), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("polo_sleeve", verts, edges)


def _polo_collar() -> PatternPiece:
    """Collar piece for a polo shirt."""
    verts = [
        (0.0, 0.0), (0.28, 0.0), (0.28, 0.05), (0.0, 0.05),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    return _make_piece("polo_collar", verts, edges)


# ---------- Wrap Dress Template ----------

def _wrap_dress_left() -> PatternPiece:
    """Left wrap panel for a wrap dress."""
    verts = [
        (0.0, 0.0), (0.30, 0.0), (0.32, 0.15), (0.30, 0.55),
        (0.25, 0.60), (0.15, 0.62), (0.08, 0.60), (0.0, 0.55),
        (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("wrap_dress_left", verts, edges)


def _wrap_dress_right() -> PatternPiece:
    """Right wrap panel for a wrap dress."""
    verts = [
        (0.0, 0.0), (0.30, 0.0), (0.32, 0.15), (0.30, 0.55),
        (0.25, 0.60), (0.15, 0.63), (0.08, 0.60), (0.0, 0.55),
        (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 0),
    ]
    return _make_piece("wrap_dress_right", verts, edges)


# ---------- Cargo Shorts Template ----------

def _cargo_shorts_front() -> PatternPiece:
    """Front leg panel for cargo shorts."""
    verts = [
        (0.0, 0.0), (0.17, 0.0), (0.18, 0.15), (0.20, 0.20),
        (0.20, 0.35), (0.16, 0.37), (0.06, 0.37), (0.0, 0.35),
        (0.0, 0.20), (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("cargo_shorts_front", verts, edges)


def _cargo_shorts_back() -> PatternPiece:
    """Back leg panel for cargo shorts."""
    verts = [
        (0.0, 0.0), (0.18, 0.0), (0.20, 0.15), (0.22, 0.20),
        (0.22, 0.35), (0.17, 0.38), (0.06, 0.38), (0.0, 0.35),
        (0.0, 0.20), (-0.02, 0.15),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("cargo_shorts_back", verts, edges)


# ---------- Blazer Template ----------

def _blazer_front() -> PatternPiece:
    """Front panel of a blazer."""
    verts = [
        (0.0, 0.0), (0.30, 0.0), (0.30, 0.05), (0.35, 0.12),
        (0.35, 0.52), (0.30, 0.57), (0.20, 0.60), (0.15, 0.60),
        (0.10, 0.60), (0.0, 0.57), (-0.05, 0.52), (-0.05, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("blazer_front", verts, edges)


def _blazer_back() -> PatternPiece:
    """Back panel of a blazer."""
    verts = [
        (0.0, 0.0), (0.32, 0.0), (0.32, 0.05), (0.36, 0.12),
        (0.36, 0.52), (0.32, 0.57), (0.22, 0.61), (0.16, 0.62),
        (0.10, 0.61), (0.0, 0.57), (-0.04, 0.52), (-0.04, 0.12),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("blazer_back", verts, edges)


def _blazer_sleeve() -> PatternPiece:
    """Long sleeve for a blazer."""
    verts = [
        (0.0, 0.0), (0.19, 0.0), (0.21, 0.05), (0.20, 0.40),
        (0.15, 0.42), (0.04, 0.42), (0.0, 0.40), (-0.02, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    ]
    return _make_piece("blazer_sleeve", verts, edges)


def _blazer_lapel() -> PatternPiece:
    """Lapel piece for a blazer."""
    verts = [
        (0.0, 0.0), (0.08, 0.0), (0.10, 0.12), (0.06, 0.18),
        (0.0, 0.16),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    return _make_piece("blazer_lapel", verts, edges)


# ---------- Vest Template ----------

def _vest_front() -> PatternPiece:
    """Front panel of a vest."""
    verts = [
        (0.0, 0.0), (0.22, 0.0), (0.22, 0.05), (0.24, 0.10),
        (0.24, 0.38), (0.20, 0.42), (0.14, 0.44), (0.08, 0.44),
        (0.04, 0.42), (0.0, 0.38), (-0.02, 0.10), (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    ]
    return _make_piece("vest_front", verts, edges)


def _vest_back() -> PatternPiece:
    """Back panel of a vest."""
    verts = [
        (0.0, 0.0), (0.22, 0.0), (0.22, 0.05), (0.24, 0.10),
        (0.24, 0.38), (0.20, 0.42), (0.14, 0.45), (0.08, 0.45),
        (0.04, 0.42), (0.0, 0.38), (-0.02, 0.10), (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    ]
    return _make_piece("vest_back", verts, edges)


# ---------- Jumpsuit Template ----------

def _jumpsuit_bodice() -> PatternPiece:
    """Bodice/torso panel for a jumpsuit."""
    verts = [
        (0.0, 0.0), (0.28, 0.0), (0.28, 0.05), (0.30, 0.10),
        (0.30, 0.40), (0.26, 0.44), (0.18, 0.46), (0.14, 0.46),
        (0.08, 0.46), (0.0, 0.44), (-0.02, 0.40), (-0.02, 0.10),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("jumpsuit_bodice", verts, edges)


def _jumpsuit_leg() -> PatternPiece:
    """Leg panel for a jumpsuit."""
    verts = [
        (0.0, 0.0), (0.15, 0.0), (0.16, 0.30), (0.18, 0.35),
        (0.18, 0.65), (0.14, 0.67), (0.06, 0.67), (0.0, 0.65),
        (0.0, 0.35), (-0.02, 0.30),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 0),
    ]
    return _make_piece("jumpsuit_leg", verts, edges)


# ---------- Kimono Template ----------

def _kimono_body() -> PatternPiece:
    """Main body panel of a kimono."""
    verts = [
        (0.0, 0.0), (0.40, 0.0), (0.40, 0.05), (0.42, 0.10),
        (0.42, 0.70), (0.38, 0.75), (0.25, 0.78), (0.20, 0.78),
        (0.15, 0.78), (0.0, 0.75), (-0.02, 0.70), (-0.02, 0.10),
        (0.0, 0.05),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 0),
    ]
    return _make_piece("kimono_body", verts, edges)


def _kimono_sleeve() -> PatternPiece:
    """Wide rectangular sleeve for a kimono."""
    verts = [
        (0.0, 0.0), (0.30, 0.0), (0.30, 0.28), (0.0, 0.28),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    return _make_piece("kimono_sleeve", verts, edges)


def _kimono_obi() -> PatternPiece:
    """Obi (belt sash) for a kimono."""
    verts = [
        (0.0, 0.0), (0.50, 0.0), (0.50, 0.10), (0.0, 0.10),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    return _make_piece("kimono_obi", verts, edges)


# ---------- Preset Registry ----------

class GarmentPreset:
    """A pre-defined garment template with pieces and seam connections."""

    def __init__(self, name: str, description: str,
                 pieces_fn, seams_fn, default_fabric: str = "cotton"):
        self.name = name
        self.description = description
        self._pieces_fn = pieces_fn
        self._seams_fn = seams_fn
        self.default_fabric = default_fabric

    def build(self) -> Tuple[PatternCollection, SeamCollection]:
        """Construct the pattern collection and seam collection for this preset."""
        pieces = self._pieces_fn()
        collection = PatternCollection()
        for piece in pieces:
            collection.get_piece(piece)
        seams = self._seams_fn(collection)
        return collection, seams


def _tshirt_pieces() -> List[PatternPiece]:
    return [_tshirt_front(), _tshirt_back(), _tshirt_sleeve()]


def _tshirt_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    # Connect front and back at shoulders and sides
    seams.add_seam("tshirt_front", [4, 5], "tshirt_back", [4, 5])
    seams.add_seam("tshirt_front", [10, 11], "tshirt_back", [10, 11])
    # Connect sleeve to armhole
    seams.add_seam("tshirt_front", [3, 4], "tshirt_sleeve", [5, 6])
    return seams


def _hoodie_pieces() -> List[PatternPiece]:
    return [_hoodie_front(), _hoodie_back(), _hoodie_sleeve(), _hoodie_hood()]


def _hoodie_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    # Connect front and back at shoulders and sides
    seams.add_seam("hoodie_front", [4, 5], "hoodie_back", [4, 5])
    seams.add_seam("hoodie_front", [10, 11], "hoodie_back", [10, 11])
    # Connect sleeve to armhole
    seams.add_seam("hoodie_front", [3, 4], "hoodie_sleeve", [5, 6])
    # Connect hood to neckline
    seams.add_seam("hoodie_back", [5, 6, 7, 8], "hoodie_hood", [0, 1, 2, 3])
    return seams


def _tank_top_pieces() -> List[PatternPiece]:
    return [_tank_top_front(), _tank_top_back()]


def _tank_top_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    # Connect front and back at shoulders
    seams.add_seam("tank_top_front", [4, 5], "tank_top_back", [4, 5])
    # Connect front and back at sides
    seams.add_seam("tank_top_front", [10, 11], "tank_top_back", [10, 11])
    return seams


def _bomber_pieces() -> List[PatternPiece]:
    return [_bomber_front(), _bomber_back(), _bomber_sleeve(), _bomber_collar()]


def _bomber_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    # Connect front and back at shoulders and sides
    seams.add_seam("bomber_front", [4, 5], "bomber_back", [4, 5])
    seams.add_seam("bomber_front", [10, 11], "bomber_back", [10, 11])
    # Connect sleeve to armhole
    seams.add_seam("bomber_front", [3, 4], "bomber_sleeve", [5, 6])
    # Connect collar to neckline
    seams.add_seam("bomber_back", [5, 6, 7, 8], "bomber_collar", [0, 1, 2, 3])
    return seams


def _skirt_pieces() -> List[PatternPiece]:
    panels = []
    for i in range(4):
        panel = _skirt_panel()
        panel.name = f"skirt_panel_{i}"
        panels.append(panel)
    return panels


def _skirt_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    names = [p.name for p in collection.pieces]
    for i in range(len(names)):
        next_i = (i + 1) % len(names)
        seams.add_seam(names[i], [1, 2], names[next_i], [5, 0])
    return seams


def _pants_pieces() -> List[PatternPiece]:
    return [_pants_front_leg(), _pants_back_leg()]


def _pants_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("pants_front_leg", [1, 2, 3], "pants_back_leg", [1, 2, 3])
    seams.add_seam("pants_front_leg", [8, 9], "pants_back_leg", [8, 9])
    return seams


def _dress_pieces() -> List[PatternPiece]:
    return [_dress_bodice_front(), _dress_skirt()]


def _dress_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    # Connect bodice bottom to skirt top
    seams.add_seam("dress_bodice_front", [0, 1], "dress_skirt", [0, 1])
    return seams


def _cardigan_pieces() -> List[PatternPiece]:
    return [_cardigan_left_front(), _cardigan_back(), _cardigan_sleeve()]


def _cardigan_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("cardigan_left_front", [4, 5], "cardigan_back", [4, 5])
    seams.add_seam("cardigan_left_front", [7, 8], "cardigan_back", [9, 10])
    seams.add_seam("cardigan_back", [3, 4], "cardigan_sleeve", [5, 6])
    return seams


def _crop_top_pieces() -> List[PatternPiece]:
    return [_crop_top_front(), _crop_top_back()]


def _crop_top_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("crop_top_front", [4, 5], "crop_top_back", [4, 5])
    seams.add_seam("crop_top_front", [9, 10], "crop_top_back", [9, 10])
    return seams


def _pencil_skirt_pieces() -> List[PatternPiece]:
    return [_pencil_skirt_front(), _pencil_skirt_back()]


def _pencil_skirt_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("pencil_skirt_front", [1, 2, 3], "pencil_skirt_back", [1, 2, 3])
    seams.add_seam("pencil_skirt_front", [7, 8], "pencil_skirt_back", [7, 8])
    return seams


def _trench_pieces() -> List[PatternPiece]:
    return [_trench_front(), _trench_back(), _trench_sleeve()]


def _trench_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("trench_front", [4, 5], "trench_back", [4, 5])
    seams.add_seam("trench_front", [10, 11], "trench_back", [10, 11])
    seams.add_seam("trench_front", [3, 4], "trench_sleeve", [5, 6])
    return seams


def _polo_pieces() -> List[PatternPiece]:
    return [_polo_front(), _polo_back(), _polo_sleeve(), _polo_collar()]


def _polo_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("polo_front", [4, 5], "polo_back", [4, 5])
    seams.add_seam("polo_front", [10, 11], "polo_back", [10, 11])
    seams.add_seam("polo_front", [3, 4], "polo_sleeve", [5, 6])
    seams.add_seam("polo_back", [5, 6, 7, 8], "polo_collar", [0, 1, 2, 3])
    return seams


def _wrap_dress_pieces() -> List[PatternPiece]:
    return [_wrap_dress_left(), _wrap_dress_right()]


def _wrap_dress_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("wrap_dress_left", [3, 4], "wrap_dress_right", [3, 4])
    return seams


def _cargo_shorts_pieces() -> List[PatternPiece]:
    return [_cargo_shorts_front(), _cargo_shorts_back()]


def _cargo_shorts_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("cargo_shorts_front", [1, 2, 3], "cargo_shorts_back", [1, 2, 3])
    seams.add_seam("cargo_shorts_front", [8, 9], "cargo_shorts_back", [8, 9])
    return seams


def _blazer_pieces() -> List[PatternPiece]:
    return [_blazer_front(), _blazer_back(), _blazer_sleeve(), _blazer_lapel()]


def _blazer_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("blazer_front", [4, 5], "blazer_back", [4, 5])
    seams.add_seam("blazer_front", [10, 11], "blazer_back", [10, 11])
    seams.add_seam("blazer_front", [3, 4], "blazer_sleeve", [5, 6])
    return seams


def _vest_pieces() -> List[PatternPiece]:
    return [_vest_front(), _vest_back()]


def _vest_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("vest_front", [4, 5], "vest_back", [4, 5])
    seams.add_seam("vest_front", [9, 10], "vest_back", [9, 10])
    return seams


def _jumpsuit_pieces() -> List[PatternPiece]:
    return [_jumpsuit_bodice(), _jumpsuit_leg()]


def _jumpsuit_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("jumpsuit_bodice", [0, 1], "jumpsuit_leg", [4, 5])
    return seams


def _kimono_pieces() -> List[PatternPiece]:
    return [_kimono_body(), _kimono_sleeve(), _kimono_obi()]


def _kimono_seams(collection: PatternCollection) -> SeamCollection:
    seams = SeamCollection()
    seams.add_seam("kimono_body", [3, 4], "kimono_sleeve", [3, 0])
    return seams


# Global preset registry
GARMENT_PRESETS: Dict[str, GarmentPreset] = {
    "tshirt": GarmentPreset(
        name="T-Shirt",
        description="Basic short-sleeve t-shirt with front, back, and sleeve pieces",
        pieces_fn=_tshirt_pieces,
        seams_fn=_tshirt_seams,
        default_fabric="cotton",
    ),
    "skirt": GarmentPreset(
        name="A-Line Skirt",
        description="Four-panel A-line skirt",
        pieces_fn=_skirt_pieces,
        seams_fn=_skirt_seams,
        default_fabric="cotton",
    ),
    "pants": GarmentPreset(
        name="Basic Pants",
        description="Simple straight-leg pants with front and back leg panels",
        pieces_fn=_pants_pieces,
        seams_fn=_pants_seams,
        default_fabric="denim",
    ),
    "dress": GarmentPreset(
        name="Simple Dress",
        description="A-line dress with bodice and skirt",
        pieces_fn=_dress_pieces,
        seams_fn=_dress_seams,
        default_fabric="silk",
    ),
    "hoodie": GarmentPreset(
        name="Hoodie",
        description="Hooded sweatshirt with front, back, sleeves, and hood",
        pieces_fn=_hoodie_pieces,
        seams_fn=_hoodie_seams,
        default_fabric="cotton",
    ),
    "tank_top": GarmentPreset(
        name="Tank Top",
        description="Sleeveless tank top with front and back panels",
        pieces_fn=_tank_top_pieces,
        seams_fn=_tank_top_seams,
        default_fabric="cotton",
    ),
    "bomber": GarmentPreset(
        name="Bomber Jacket",
        description="Bomber jacket with front, back, sleeves, and ribbed collar",
        pieces_fn=_bomber_pieces,
        seams_fn=_bomber_seams,
        default_fabric="polyester",
    ),
    "cardigan": GarmentPreset(
        name="Cardigan",
        description="Open-front cardigan with back panel and long sleeves",
        pieces_fn=_cardigan_pieces,
        seams_fn=_cardigan_seams,
        default_fabric="wool",
    ),
    "crop_top": GarmentPreset(
        name="Crop Top",
        description="Short cropped top with front and back panels",
        pieces_fn=_crop_top_pieces,
        seams_fn=_crop_top_seams,
        default_fabric="cotton",
    ),
    "pencil_skirt": GarmentPreset(
        name="Pencil Skirt",
        description="Fitted pencil skirt with front and back panels",
        pieces_fn=_pencil_skirt_pieces,
        seams_fn=_pencil_skirt_seams,
        default_fabric="polyester",
    ),
    "trench_coat": GarmentPreset(
        name="Trench Coat",
        description="Long trench coat with front, back, and sleeves",
        pieces_fn=_trench_pieces,
        seams_fn=_trench_seams,
        default_fabric="cotton",
    ),
    "polo": GarmentPreset(
        name="Polo Shirt",
        description="Polo shirt with collar, short sleeves, and placket",
        pieces_fn=_polo_pieces,
        seams_fn=_polo_seams,
        default_fabric="cotton",
    ),
    "wrap_dress": GarmentPreset(
        name="Wrap Dress",
        description="Wrap-style dress with overlapping front panels",
        pieces_fn=_wrap_dress_pieces,
        seams_fn=_wrap_dress_seams,
        default_fabric="silk",
    ),
    "cargo_shorts": GarmentPreset(
        name="Cargo Shorts",
        description="Knee-length cargo shorts with front and back leg panels",
        pieces_fn=_cargo_shorts_pieces,
        seams_fn=_cargo_shorts_seams,
        default_fabric="cotton",
    ),
    "blazer": GarmentPreset(
        name="Blazer",
        description="Tailored blazer with front, back, sleeves, and lapels",
        pieces_fn=_blazer_pieces,
        seams_fn=_blazer_seams,
        default_fabric="wool",
    ),
    "vest": GarmentPreset(
        name="Vest",
        description="Sleeveless vest with front and back panels",
        pieces_fn=_vest_pieces,
        seams_fn=_vest_seams,
        default_fabric="polyester",
    ),
    "jumpsuit": GarmentPreset(
        name="Jumpsuit",
        description="One-piece jumpsuit with bodice and full-length legs",
        pieces_fn=_jumpsuit_pieces,
        seams_fn=_jumpsuit_seams,
        default_fabric="cotton",
    ),
    "kimono": GarmentPreset(
        name="Kimono",
        description="Traditional kimono with wide body, rectangular sleeves, and obi",
        pieces_fn=_kimono_pieces,
        seams_fn=_kimono_seams,
        default_fabric="silk",
    ),
}


def get_preset_names() -> List[Tuple[str, str, str]]:
    """Return preset names formatted for Blender EnumProperty items."""
    return [(key, preset.name, preset.description)
            for key, preset in GARMENT_PRESETS.items()]


def load_preset(preset_key: str) -> Tuple[PatternCollection, SeamCollection]:
    """Load a garment preset by key and return the pattern + seam collections."""
    preset = GARMENT_PRESETS.get(preset_key)
    if preset is None:
        raise ValueError(f"Unknown garment preset: {preset_key}")
    return preset.build()
