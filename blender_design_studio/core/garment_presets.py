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
            collection.add_piece(piece)
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
