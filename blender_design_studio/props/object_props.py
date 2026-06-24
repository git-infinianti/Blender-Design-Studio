"""Per-object addon properties for garment and paint data."""
import bpy
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, EnumProperty,
)


class BDS_ObjectProps(bpy.types.PropertyGroup):
    """Per-object properties attached to mesh objects."""
    is_garment: BoolProperty(
        name="Is Garment",
        description="Whether this object is a BDS garment",
        default=False,
    )
    is_avatar: BoolProperty(
        name="Is Avatar",
        description="Whether this object is used as an avatar for draping",
        default=False,
    )
    garment_name: StringProperty(
        name="Garment Name",
        default="",
    )
    paint_resolution: IntProperty(
        name="Paint Resolution",
        description="Resolution for paint layers on this object",
        default=2048,
        min=256,
        max=8192,
    )
    active_smart_material: EnumProperty(
        name="Smart Material",
        items=[
            ('NONE', 'None', 'No smart material'),
            ('worn_metal', 'Worn Metal', 'Worn metal surface'),
            ('aged_wood', 'Aged Wood', 'Aged wood surface'),
            ('clean_plastic', 'Clean Plastic', 'Clean plastic surface'),
            ('fabric', 'Fabric', 'Cloth/fabric surface'),
        ],
        default='NONE',
    )
