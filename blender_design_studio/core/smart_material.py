"""Procedural smart material system for automatic texture generation."""
from typing import List, Dict, Optional

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


class SmartMaterial:
    """A smart material that auto-generates textures from mesh data."""

    def __init__(self, name: str):
        self.name = name
        self.base_color: tuple = (0.8, 0.8, 0.8)
        self.metallic: float = 0.0
        self.roughness: float = 0.5
        self.use_curvature_mask: bool = False
        self.use_ao_mask: bool = False
        self.use_position_gradient: bool = False
        self.curvature_intensity: float = 1.0
        self.ao_intensity: float = 1.0
        self.edge_wear_color: tuple = (0.9, 0.9, 0.9)
        self.cavity_color: tuple = (0.2, 0.2, 0.2)

    def apply_to_layer_stack(self, layer_stack, obj=None) -> None:
        """Generate layers in the layer stack from this smart material."""
        base = layer_stack.add_layer(f"{self.name}_base")

        if HAS_BPY and 'base_color' in base.channels:
            img = base.channels['base_color']
            self._fill_image(img, self.base_color)

        if self.use_curvature_mask and obj is not None:
            wear_layer = layer_stack.add_layer(f"{self.name}_edge_wear")
            wear_layer.blend_mode = 'SCREEN'
            wear_layer.opacity = self.curvature_intensity
            if HAS_BPY and 'base_color' in wear_layer.channels:
                self._fill_image(wear_layer.channels['base_color'], self.edge_wear_color)

        if self.use_ao_mask and obj is not None:
            cavity_layer = layer_stack.add_layer(f"{self.name}_cavity")
            cavity_layer.blend_mode = 'MULTIPLY'
            cavity_layer.opacity = self.ao_intensity
            if HAS_BPY and 'base_color' in cavity_layer.channels:
                self._fill_image(cavity_layer.channels['base_color'], self.cavity_color)

    @staticmethod
    def _fill_image(img, color: tuple) -> None:
        """Fill an image with a solid color."""
        if not HAS_BPY:
            return
        width, height = img.size[0], img.size[1]
        r, g, b = color
        pixels = [0.0] * (width * height * 4)
        for i in range(0, len(pixels), 4):
            pixels[i] = r
            pixels[i + 1] = g
            pixels[i + 2] = b
            pixels[i + 3] = 1.0
        img.pixels[:] = pixels
        img.update()


class SmartMaterialLibrary:
    """Collection of pre-built smart materials."""

    def __init__(self):
        self.materials: Dict[str, SmartMaterial] = {}
        self._init_defaults()

    def _init_defaults(self) -> None:
        """Initialize built-in smart material presets."""
        worn_metal = SmartMaterial("Worn Metal")
        worn_metal.base_color = (0.3, 0.3, 0.35)
        worn_metal.metallic = 0.9
        worn_metal.roughness = 0.4
        worn_metal.use_curvature_mask = True
        worn_metal.use_ao_mask = True
        worn_metal.edge_wear_color = (0.8, 0.8, 0.85)
        worn_metal.cavity_color = (0.1, 0.1, 0.12)
        self.materials["worn_metal"] = worn_metal

        aged_wood = SmartMaterial("Aged Wood")
        aged_wood.base_color = (0.4, 0.25, 0.12)
        aged_wood.metallic = 0.0
        aged_wood.roughness = 0.7
        aged_wood.use_curvature_mask = True
        aged_wood.use_ao_mask = True
        aged_wood.edge_wear_color = (0.5, 0.35, 0.2)
        aged_wood.cavity_color = (0.15, 0.08, 0.03)
        self.materials["aged_wood"] = aged_wood

        clean_plastic = SmartMaterial("Clean Plastic")
        clean_plastic.base_color = (0.8, 0.1, 0.1)
        clean_plastic.metallic = 0.0
        clean_plastic.roughness = 0.3
        clean_plastic.use_ao_mask = True
        clean_plastic.cavity_color = (0.4, 0.05, 0.05)
        self.materials["clean_plastic"] = clean_plastic

        fabric_cloth = SmartMaterial("Fabric")
        fabric_cloth.base_color = (0.6, 0.6, 0.65)
        fabric_cloth.metallic = 0.0
        fabric_cloth.roughness = 0.85
        fabric_cloth.use_curvature_mask = True
        fabric_cloth.edge_wear_color = (0.7, 0.7, 0.75)
        self.materials["fabric"] = fabric_cloth

        brushed_steel = SmartMaterial("Brushed Steel")
        brushed_steel.base_color = (0.55, 0.56, 0.58)
        brushed_steel.metallic = 1.0
        brushed_steel.roughness = 0.35
        brushed_steel.use_curvature_mask = True
        brushed_steel.use_ao_mask = True
        brushed_steel.edge_wear_color = (0.7, 0.72, 0.75)
        brushed_steel.cavity_color = (0.2, 0.2, 0.22)
        self.materials["brushed_steel"] = brushed_steel

        rusted_iron = SmartMaterial("Rusted Iron")
        rusted_iron.base_color = (0.35, 0.18, 0.08)
        rusted_iron.metallic = 0.6
        rusted_iron.roughness = 0.8
        rusted_iron.use_curvature_mask = True
        rusted_iron.use_ao_mask = True
        rusted_iron.edge_wear_color = (0.5, 0.25, 0.1)
        rusted_iron.cavity_color = (0.12, 0.06, 0.02)
        self.materials["rusted_iron"] = rusted_iron

        polished_marble = SmartMaterial("Polished Marble")
        polished_marble.base_color = (0.9, 0.88, 0.85)
        polished_marble.metallic = 0.0
        polished_marble.roughness = 0.1
        polished_marble.use_ao_mask = True
        polished_marble.cavity_color = (0.6, 0.58, 0.55)
        self.materials["polished_marble"] = polished_marble

        worn_leather = SmartMaterial("Worn Leather")
        worn_leather.base_color = (0.35, 0.2, 0.1)
        worn_leather.metallic = 0.0
        worn_leather.roughness = 0.6
        worn_leather.use_curvature_mask = True
        worn_leather.use_ao_mask = True
        worn_leather.edge_wear_color = (0.5, 0.35, 0.2)
        worn_leather.cavity_color = (0.15, 0.08, 0.04)
        self.materials["worn_leather"] = worn_leather

        concrete = SmartMaterial("Concrete")
        concrete.base_color = (0.55, 0.53, 0.5)
        concrete.metallic = 0.0
        concrete.roughness = 0.9
        concrete.use_ao_mask = True
        concrete.use_curvature_mask = True
        concrete.edge_wear_color = (0.65, 0.63, 0.6)
        concrete.cavity_color = (0.3, 0.28, 0.25)
        self.materials["concrete"] = concrete

        ceramic_tile = SmartMaterial("Ceramic Tile")
        ceramic_tile.base_color = (0.85, 0.85, 0.9)
        ceramic_tile.metallic = 0.0
        ceramic_tile.roughness = 0.15
        ceramic_tile.use_ao_mask = True
        ceramic_tile.cavity_color = (0.4, 0.4, 0.42)
        self.materials["ceramic_tile"] = ceramic_tile

        carbon_fiber = SmartMaterial("Carbon Fiber")
        carbon_fiber.base_color = (0.02, 0.02, 0.02)
        carbon_fiber.metallic = 0.3
        carbon_fiber.roughness = 0.35
        carbon_fiber.use_curvature_mask = True
        carbon_fiber.edge_wear_color = (0.15, 0.15, 0.15)
        self.materials["carbon_fiber"] = carbon_fiber

        velvet = SmartMaterial("Velvet")
        velvet.base_color = (0.25, 0.05, 0.1)
        velvet.metallic = 0.0
        velvet.roughness = 0.95
        velvet.use_curvature_mask = True
        velvet.edge_wear_color = (0.4, 0.15, 0.2)
        self.materials["velvet"] = velvet

        hammered_copper = SmartMaterial("Hammered Copper")
        hammered_copper.base_color = (0.7, 0.4, 0.2)
        hammered_copper.metallic = 1.0
        hammered_copper.roughness = 0.5
        hammered_copper.use_curvature_mask = True
        hammered_copper.use_ao_mask = True
        hammered_copper.edge_wear_color = (0.3, 0.5, 0.35)
        hammered_copper.cavity_color = (0.3, 0.15, 0.05)
        self.materials["hammered_copper"] = hammered_copper

        frosted_glass = SmartMaterial("Frosted Glass")
        frosted_glass.base_color = (0.9, 0.92, 0.95)
        frosted_glass.metallic = 0.0
        frosted_glass.roughness = 0.4
        frosted_glass.use_ao_mask = True
        frosted_glass.cavity_color = (0.7, 0.72, 0.75)
        self.materials["frosted_glass"] = frosted_glass

        raw_denim = SmartMaterial("Raw Denim")
        raw_denim.base_color = (0.1, 0.12, 0.25)
        raw_denim.metallic = 0.0
        raw_denim.roughness = 0.8
        raw_denim.use_curvature_mask = True
        raw_denim.use_ao_mask = True
        raw_denim.edge_wear_color = (0.3, 0.35, 0.5)
        raw_denim.cavity_color = (0.05, 0.05, 0.12)
        self.materials["raw_denim"] = raw_denim

        patent_leather = SmartMaterial("Patent Leather")
        patent_leather.base_color = (0.01, 0.01, 0.01)
        patent_leather.metallic = 0.0
        patent_leather.roughness = 0.05
        patent_leather.use_curvature_mask = True
        patent_leather.use_ao_mask = True
        patent_leather.edge_wear_color = (0.15, 0.15, 0.15)
        patent_leather.cavity_color = (0.0, 0.0, 0.0)
        self.materials["patent_leather"] = patent_leather

    def get(self, name: str) -> Optional[SmartMaterial]:
        """Get a smart material by name."""
        return self.materials.get(name)

    def add(self, key: str, material: SmartMaterial) -> None:
        """Add a smart material to the library."""
        self.materials[key] = material

    def list_names(self) -> List[str]:
        """Return list of available smart material names."""
        return list(self.materials.keys())
