"""Core texture paint engine with brush settings and stroke recording."""
from typing import List, Tuple, Optional, Dict
import math

try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class BrushSettings:
    """Configuration for a paint brush."""

    def __init__(self):
        self.radius: int = 50
        self.strength: float = 1.0
        self.falloff: str = 'SMOOTH'
        self.color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
        self.texture = None
        self.spacing: float = 0.1
        self.channel: str = "base_color"

    def get_falloff_value(self, distance: float, radius: float) -> float:
        """Compute falloff intensity based on distance from center."""
        if radius <= 0:
            return 0.0
        t = min(distance / radius, 1.0)
        if self.falloff == 'CONSTANT':
            return 1.0
        if self.falloff == 'LINEAR':
            return 1.0 - t
        if self.falloff == 'SHARP':
            return (1.0 - t) ** 2
        return 0.5 * (1.0 + math.cos(math.pi * t))

    def copy(self) -> 'BrushSettings':
        """Create a copy of these brush settings."""
        b = BrushSettings()
        b.radius = self.radius
        b.strength = self.strength
        b.falloff = self.falloff
        b.color = self.color
        b.texture = self.texture
        b.spacing = self.spacing
        b.channel = self.channel
        return b


# ---------- Brush Presets ----------

BRUSH_PRESETS = {
    "default": {
        "name": "Default",
        "description": "General-purpose round brush",
        "radius": 50,
        "strength": 1.0,
        "falloff": "SMOOTH",
        "spacing": 0.1,
    },
    "soft_airbrush": {
        "name": "Soft Airbrush",
        "description": "Soft, low-opacity airbrush for subtle blending",
        "radius": 100,
        "strength": 0.15,
        "falloff": "SMOOTH",
        "spacing": 0.05,
    },
    "hard_round": {
        "name": "Hard Round",
        "description": "Crisp-edged brush for precise detail work",
        "radius": 30,
        "strength": 1.0,
        "falloff": "CONSTANT",
        "spacing": 0.08,
    },
    "fine_detail": {
        "name": "Fine Detail",
        "description": "Small, sharp brush for fine details and lines",
        "radius": 10,
        "strength": 0.9,
        "falloff": "SHARP",
        "spacing": 0.05,
    },
    "broad_fill": {
        "name": "Broad Fill",
        "description": "Large brush for filling wide areas quickly",
        "radius": 200,
        "strength": 0.8,
        "falloff": "LINEAR",
        "spacing": 0.15,
    },
    "texture_stamp": {
        "name": "Texture Stamp",
        "description": "Widely spaced stamps for textured effects",
        "radius": 60,
        "strength": 0.7,
        "falloff": "SHARP",
        "spacing": 0.5,
    },
    "smudge_blend": {
        "name": "Smudge Blend",
        "description": "Soft brush optimized for blending transitions",
        "radius": 80,
        "strength": 0.3,
        "falloff": "SMOOTH",
        "spacing": 0.04,
    },
}


def apply_brush_preset(brush: BrushSettings, preset_key: str) -> None:
    """Apply a brush preset to the given BrushSettings instance."""
    preset = BRUSH_PRESETS.get(preset_key)
    if preset is None:
        raise ValueError(f"Unknown brush preset: {preset_key}")
    brush.radius = preset["radius"]
    brush.strength = preset["strength"]
    brush.falloff = preset["falloff"]
    brush.spacing = preset["spacing"]


def get_brush_preset_names():
    """Return brush preset names formatted for Blender EnumProperty items."""
    return [(key, p["name"], p["description"])
            for key, p in BRUSH_PRESETS.items()]


class PaintStroke:
    """Records a single continuous stroke for undo/redo."""

    def __init__(self, layer, brush: BrushSettings):
        self.layer = layer
        self.brush = brush
        self.points: List[Tuple[float, float, float]] = []
        self._undo_data: Optional[Dict[str, bytes]] = None

    def add_point(self, u: float, v: float, pressure: float = 1.0) -> None:
        """Record a stroke point in UV space."""
        self.points.append((u, v, pressure))

    def apply(self) -> None:
        """Write brush stamps along self.points into layer's image buffer."""
        if not HAS_NUMPY or not HAS_BPY:
            return

        channel = self.brush.channel
        if channel not in self.layer.channels:
            return

        img = self.layer.channels[channel]
        width, height = img.size[0], img.size[1]
        pixels = np.array(img.pixels[:], dtype=np.float32).reshape((height, width, 4))

        self._undo_data = {channel: pixels.tobytes()}

        for u, v, pressure in self.points:
            self._stamp(pixels, u, v, pressure, width, height)

        img.pixels[:] = pixels.ravel().tolist()
        img.update()

    def _stamp(self, pixels, u: float, v: float, pressure: float, width: int, height: int) -> None:
        """Blend a single brush footprint into the pixel array."""
        radius = self.brush.radius
        strength = self.brush.strength * pressure

        cx = int(u * width)
        cy = int(v * height)

        x_min = max(0, cx - radius)
        x_max = min(width, cx + radius + 1)
        y_min = max(0, cy - radius)
        y_max = min(height, cy + radius + 1)

        for py in range(y_min, y_max):
            for px in range(x_min, x_max):
                dx = px - cx
                dy = py - cy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > radius:
                    continue

                falloff = self.brush.get_falloff_value(dist, radius)
                alpha = falloff * strength

                r, g, b = self.brush.color
                pixels[py, px, 0] = pixels[py, px, 0] * (1 - alpha) + r * alpha
                pixels[py, px, 1] = pixels[py, px, 1] * (1 - alpha) + g * alpha
                pixels[py, px, 2] = pixels[py, px, 2] * (1 - alpha) + b * alpha
                pixels[py, px, 3] = min(1.0, pixels[py, px, 3] + alpha)

    def undo(self) -> None:
        """Restore pixels from before this stroke was applied."""
        if not HAS_NUMPY or not HAS_BPY or self._undo_data is None:
            return

        for channel, data in self._undo_data.items():
            if channel in self.layer.channels:
                img = self.layer.channels[channel]
                width, height = img.size[0], img.size[1]
                pixels = np.frombuffer(data, dtype=np.float32).reshape((height, width, 4))
                img.pixels[:] = pixels.ravel().tolist()
                img.update()
