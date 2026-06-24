from .pattern import PatternPiece, PatternCollection
from .seam import SeamSegment, SeamCollection
from .garment import Garment
from .fabric import FabricMaterial, FABRIC_PRESETS
from .simulation import SimulationController
from .paint_engine import BrushSettings, PaintStroke
from .layer_stack import PaintLayer, LayerStack
from .bake import BakeManager
from .udim import UDIMTileSet
from .smart_material import SmartMaterial, SmartMaterialLibrary

__all__ = (
    "PatternPiece",
    "PatternCollection",
    "SeamSegment",
    "SeamCollection",
    "Garment",
    "FabricMaterial",
    "FABRIC_PRESETS",
    "SimulationController",
    "BrushSettings",
    "PaintStroke",
    "PaintLayer",
    "LayerStack",
    "BakeManager",
    "UDIMTileSet",
    "SmartMaterial",
    "SmartMaterialLibrary",
)
