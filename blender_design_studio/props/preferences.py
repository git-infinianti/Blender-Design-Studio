"""Addon preferences for Blender Design Studio."""
import bpy
from bpy.props import (
    IntProperty, BoolProperty, EnumProperty, StringProperty,
)


class BDS_Preferences(bpy.types.AddonPreferences):
    """User preferences for Blender Design Studio."""
    bl_idname = "blender_design_studio"

    default_resolution: IntProperty(
        name="Default Resolution",
        description="Default texture resolution for new layers",
        default=2048,
        min=256,
        max=8192,
    )
    auto_save_textures: BoolProperty(
        name="Auto Save Textures",
        description="Automatically save textures when saving the blend file",
        default=True,
    )
    sim_quality: EnumProperty(
        name="Simulation Quality",
        items=[
            ('LOW', 'Low', 'Fast but less accurate'),
            ('MEDIUM', 'Medium', 'Balanced quality'),
            ('HIGH', 'High', 'High quality, slower'),
        ],
        default='MEDIUM',
    )
    default_fabric: EnumProperty(
        name="Default Fabric",
        items=[
            ('cotton', 'Cotton', ''),
            ('silk', 'Silk', ''),
            ('denim', 'Denim', ''),
            ('leather', 'Leather', ''),
        ],
        default='cotton',
    )
    texture_export_path: StringProperty(
        name="Export Path",
        description="Default path for texture export",
        default="//textures/",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout

        layout.label(text="General Settings:")
        layout.prop(self, "default_resolution")
        layout.prop(self, "auto_save_textures")
        layout.prop(self, "texture_export_path")

        layout.separator()
        layout.label(text="Simulation:")
        layout.prop(self, "sim_quality")
        layout.prop(self, "default_fabric")
