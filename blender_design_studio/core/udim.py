"""UDIM tile management for multi-tile texture workflows."""
from typing import Dict, Optional, Tuple

try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False


class UDIMTileSet:
    """Manages UDIM tiled textures for painting."""

    def __init__(self, base_name: str, resolution: int = 2048):
        self.base_name = base_name
        self.resolution = resolution
        self.tiles: Dict[int, 'bpy.types.Image'] = {}

    def add_tile(self, u_index: int, v_index: int) -> Optional['bpy.types.Image']:
        """Add a new UDIM tile at the given grid position."""
        if not HAS_BPY:
            return None

        udim_number = 1001 + u_index + v_index * 10
        name = f"{self.base_name}.{udim_number}"

        if udim_number in self.tiles:
            return self.tiles[udim_number]

        img = bpy.data.images.new(name, self.resolution, self.resolution, alpha=True)
        self.tiles[udim_number] = img
        return img

    def remove_tile(self, u_index: int, v_index: int) -> bool:
        """Remove a UDIM tile."""
        if not HAS_BPY:
            return False

        udim_number = 1001 + u_index + v_index * 10
        if udim_number in self.tiles:
            img = self.tiles.pop(udim_number)
            bpy.data.images.remove(img)
            return True
        return False

    def get_tile(self, udim_number: int) -> Optional['bpy.types.Image']:
        """Get a tile by its UDIM number."""
        return self.tiles.get(udim_number)

    def get_tile_for_uv(self, u: float, v: float) -> Optional['bpy.types.Image']:
        """Get the tile image that contains the given UV coordinate."""
        u_idx = int(u)
        v_idx = int(v)
        udim = 1001 + u_idx + v_idx * 10
        return self.tiles.get(udim)

    def uv_to_local(self, u: float, v: float) -> Tuple[float, float]:
        """Convert global UV to local tile UV coordinates."""
        return u - int(u), v - int(v)

    def tile_count(self) -> int:
        """Return the number of active tiles."""
        return len(self.tiles)

    def tile_numbers(self) -> list:
        """Return sorted list of active UDIM numbers."""
        return sorted(self.tiles.keys())

    @staticmethod
    def udim_to_grid(udim_number: int) -> Tuple[int, int]:
        """Convert UDIM number to grid position."""
        offset = udim_number - 1001
        u_index = offset % 10
        v_index = offset // 10
        return u_index, v_index
