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
            ('worn_metal', 'Worn Metal', 'Worn metal surface with edge wear'),
            ('aged_wood', 'Aged Wood', 'Aged wood surface with grain'),
            ('clean_plastic', 'Clean Plastic', 'Clean plastic surface'),
            ('fabric', 'Fabric', 'Cloth/fabric surface'),
            ('brushed_steel', 'Brushed Steel', 'Brushed stainless steel'),
            ('rusted_iron', 'Rusted Iron', 'Corroded iron with rust patches'),
            ('polished_marble', 'Polished Marble', 'Smooth polished marble stone'),
            ('worn_leather', 'Worn Leather', 'Aged leather with creases'),
            ('concrete', 'Concrete', 'Rough concrete surface'),
            ('ceramic_tile', 'Ceramic Tile', 'Glazed ceramic tile surface'),
            ('carbon_fiber', 'Carbon Fiber', 'Woven carbon fiber composite'),
            ('velvet', 'Velvet', 'Soft velvet fabric with sheen'),
            ('hammered_copper', 'Hammered Copper', 'Hammered copper with patina'),
            ('frosted_glass', 'Frosted Glass', 'Frosted translucent glass'),
            ('raw_denim', 'Raw Denim', 'Unwashed raw denim texture'),
            ('patent_leather', 'Patent Leather', 'High-gloss patent leather'),
        ],
        default='NONE',
    )
