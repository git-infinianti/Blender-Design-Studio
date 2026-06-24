"""Layer context menu and additional layer UI elements."""
import bpy


class BDS_MT_layer_context_menu(bpy.types.Menu):
    """Right-click context menu for layers"""

    bl_label = "Layer Options"
    bl_idname = "BDS_MT_layer_context_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("bds.layer_duplicate", text="Duplicate Layer", icon='DUPLICATE')
        layout.operator("bds.layer_merge_down", text="Merge Down", icon='TRIA_DOWN')
        layout.separator()
        layout.operator("bds.layer_flatten", text="Flatten Visible", icon='RENDERLAYERS')
