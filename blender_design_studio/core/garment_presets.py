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
