"""Scene-level addon properties for Blender Design Studio."""
import bpy
from bpy.props import (
    StringProperty, FloatProperty, IntProperty, BoolProperty,
    EnumProperty, CollectionProperty, FloatVectorProperty,
)


class BDS_PatternPieceProps(bpy.types.PropertyGroup):
    """Properties for a single pattern piece."""
    name: StringProperty(name="Name", default="Pattern")
    fabric_preset: EnumProperty(
        name="Fabric",
        items=[
            ('cotton', 'Cotton', 'Lightweight cotton fabric'),
            ('silk', 'Silk', 'Lightweight silk fabric'),
            ('denim', 'Denim', 'Heavy denim fabric'),
            ('leather', 'Leather', 'Thick leather material'),
            ('chiffon', 'Chiffon', 'Very lightweight chiffon'),
            ('wool', 'Wool', 'Medium weight wool'),
            ('polyester', 'Polyester', 'Synthetic polyester'),
            ('linen', 'Linen', 'Natural linen fabric'),
        ],
        default='cotton',
    )
    seam_allowance: FloatProperty(
        name="Seam Allowance",
        default=0.01,
        min=0.0,
        max=0.1,
        unit='LENGTH',
    )


class BDS_LayerProps(bpy.types.PropertyGroup):
    """Properties for a single paint layer."""
    name: StringProperty(name="Name", default="Layer")
    visible: BoolProperty(name="Visible", default=True)
    opacity: FloatProperty(
        name="Opacity",
        default=1.0,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
    )
    blend_mode: EnumProperty(
        name="Blend Mode",
        items=[
            ('MIX', 'Mix', 'Normal mix blending'),
            ('MULTIPLY', 'Multiply', 'Multiply blending'),
            ('SCREEN', 'Screen', 'Screen blending'),
            ('OVERLAY', 'Overlay', 'Overlay blending'),
            ('ADD', 'Add', 'Additive blending'),
        ],
        default='MIX',
    )
    locked: BoolProperty(name="Locked", default=False)


class BDS_SceneProps(bpy.types.PropertyGroup):
    """Scene-level properties for the addon."""
    mode: EnumProperty(
        name="Mode",
        items=[
            ('PATTERN', 'Pattern', 'Pattern drafting mode'),
            ('DRAPE', 'Drape', 'Cloth simulation mode'),
            ('PAINT', 'Paint', 'Texture painting mode'),
        ],
        default='PATTERN',
    )
    pattern_pieces: CollectionProperty(type=BDS_PatternPieceProps)
    active_piece_index: IntProperty(name="Active Piece", default=0)
    paint_layers: CollectionProperty(type=BDS_LayerProps)
    active_layer_index: IntProperty(name="Active Layer", default=0)
    active_channel: EnumProperty(
        name="Channel",
        items=[
            ('base_color', 'Base Color', 'Albedo / diffuse color'),
            ('metallic', 'Metallic', 'Metallic map'),
            ('roughness', 'Roughness', 'Roughness map'),
            ('normal', 'Normal', 'Normal map'),
            ('height', 'Height', 'Height / displacement map'),
        ],
        default='base_color',
    )
    brush_radius: IntProperty(
        name="Brush Radius",
        default=50,
        min=1,
        max=500,
    )
    brush_strength: FloatProperty(
        name="Brush Strength",
        default=1.0,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
    )
    brush_color: FloatVectorProperty(
        name="Brush Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=3,
    )
    brush_falloff: EnumProperty(
        name="Falloff",
        items=[
            ('SMOOTH', 'Smooth', 'Smooth cosine falloff'),
            ('SHARP', 'Sharp', 'Sharp quadratic falloff'),
            ('LINEAR', 'Linear', 'Linear falloff'),
            ('CONSTANT', 'Constant', 'No falloff'),
        ],
        default='SMOOTH',
    )
    brush_preset: EnumProperty(
        name="Brush Preset",
        items=[
            ('default', 'Default', 'General-purpose round brush'),
            ('soft_airbrush', 'Soft Airbrush', 'Soft, low-opacity airbrush for subtle blending'),
            ('hard_round', 'Hard Round', 'Crisp-edged brush for precise detail work'),
            ('fine_detail', 'Fine Detail', 'Small, sharp brush for fine details and lines'),
            ('broad_fill', 'Broad Fill', 'Large brush for filling wide areas quickly'),
            ('texture_stamp', 'Texture Stamp', 'Widely spaced stamps for textured effects'),
            ('smudge_blend', 'Smudge Blend', 'Soft brush optimized for blending transitions'),
            ('dry_brush', 'Dry Brush', 'Rough textured strokes for weathering effects'),
            ('ink_pen', 'Ink Pen', 'Pressure-sensitive fine-tip pen for linework'),
            ('chalk', 'Chalk', 'Grainy, textured strokes simulating chalk on paper'),
            ('spray_can', 'Spray Can', 'Scattered particle spray for graffiti-style painting'),
            ('palette_knife', 'Palette Knife', 'Flat, directional smear for impasto effects'),
            ('stipple', 'Stipple', 'Dotted application for pointillist texturing'),
            ('splatter', 'Splatter', 'Randomized droplet pattern for organic effects'),
            ('eraser_soft', 'Soft Eraser', 'Soft-edged eraser for gradual transparency'),
            ('watercolor', 'Watercolor', 'Wet-edge brush with color bleeding and diffusion'),
            ('flat_shader', 'Flat Shader', 'Even, uniform application with no falloff variation'),
        ],
        default='default',
    )
    sim_fabric_preset: EnumProperty(
        name="Fabric Preset",
        items=[
            ('cotton', 'Cotton', 'Lightweight cotton'),
            ('silk', 'Silk', 'Lightweight silk'),
            ('denim', 'Denim', 'Heavy denim'),
            ('leather', 'Leather', 'Thick leather'),
            ('chiffon', 'Chiffon', 'Very lightweight chiffon'),
            ('wool', 'Wool', 'Medium weight wool'),
            ('polyester', 'Polyester', 'Synthetic polyester'),
            ('linen', 'Linen', 'Natural linen'),
        ],
        default='cotton',
    )
    bake_resolution: IntProperty(
        name="Bake Resolution",
        default=4096,
        min=256,
        max=8192,
    )
    export_format: EnumProperty(
        name="Export Format",
        items=[
            ('PNG', 'PNG', 'PNG format'),
            ('JPEG', 'JPEG', 'JPEG format'),
            ('TARGA', 'Targa', 'TGA format'),
            ('OPEN_EXR', 'OpenEXR', 'EXR format'),
        ],
        default='PNG',
    )
