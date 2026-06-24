bl_info = {
    "name": "Blender Design Studio",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf",
    "description": "Cloth patterning + UDIM-aware painting workflows",
    "category": "Object",
}

import bpy

from .core import pattern
from .ui import panels
from .ops import pattern_ops

classes = (
    pattern_ops.BDS_OT_create_pattern,
    panels.BDS_PT_main_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
