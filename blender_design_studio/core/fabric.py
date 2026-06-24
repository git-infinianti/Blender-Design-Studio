"""Fabric material properties database and cloth modifier configuration."""
from typing import Dict, Any, List

try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False


FABRIC_PRESETS: Dict[str, Dict[str, float]] = {
    "cotton": {"mass": 0.15, "stiffness": 15.0, "damping": 5.0, "bending": 0.5},
    "silk": {"mass": 0.06, "stiffness": 5.0, "damping": 2.0, "bending": 0.1},
    "denim": {"mass": 0.35, "stiffness": 40.0, "damping": 10.0, "bending": 5.0},
    "leather": {"mass": 0.50, "stiffness": 80.0, "damping": 15.0, "bending": 10.0},
    "chiffon": {"mass": 0.04, "stiffness": 3.0, "damping": 1.0, "bending": 0.05},
    "wool": {"mass": 0.25, "stiffness": 20.0, "damping": 8.0, "bending": 2.0},
    "polyester": {"mass": 0.12, "stiffness": 12.0, "damping": 4.0, "bending": 0.3},
    "linen": {"mass": 0.20, "stiffness": 25.0, "damping": 7.0, "bending": 1.5},
}


class FabricMaterial:
    """Represents physical cloth properties for simulation."""

    def __init__(self, preset: str = "cotton"):
        if preset not in FABRIC_PRESETS:
            raise ValueError(
                f"Unknown preset '{preset}'. "
                f"Available: {list(FABRIC_PRESETS.keys())}"
            )
        props = FABRIC_PRESETS[preset]
        self.preset_name = preset
        self.mass: float = props["mass"]
        self.structural_stiffness: float = props["stiffness"]
        self.damping: float = props["damping"]
        self.bending_stiffness: float = props["bending"]

    def apply_to_cloth_modifier(self, cloth_mod) -> None:
        """Configure a Blender ClothModifier with these fabric properties."""
        settings = cloth_mod.settings
        settings.mass = self.mass
        settings.tension_stiffness = self.structural_stiffness
        settings.compression_stiffness = self.structural_stiffness
        settings.bending_stiffness = self.bending_stiffness
        settings.tension_damping = self.damping
        settings.compression_damping = self.damping

    def to_dict(self) -> Dict[str, Any]:
        """Serialize fabric properties to a dictionary."""
        return {
            "preset": self.preset_name,
            "mass": self.mass,
            "structural_stiffness": self.structural_stiffness,
            "damping": self.damping,
            "bending_stiffness": self.bending_stiffness,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FabricMaterial':
        """Create a FabricMaterial from a dictionary."""
        mat = cls(data.get("preset", "cotton"))
        mat.mass = data.get("mass", mat.mass)
        mat.structural_stiffness = data.get(
            "structural_stiffness",
            mat.structural_stiffness,
        )
        mat.damping = data.get("damping", mat.damping)
        mat.bending_stiffness = data.get(
            "bending_stiffness",
            mat.bending_stiffness,
        )
        return mat

    @staticmethod
    def available_presets() -> List[str]:
        """Return list of available fabric preset names."""
        return list(FABRIC_PRESETS.keys())
