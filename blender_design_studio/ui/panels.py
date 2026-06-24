import bpy


class BDS_PT_main_panel(bpy.types.Panel):
    bl_label = "Blender Design Studio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Garment & Painter Tools")
        layout.operator("bds.create_pattern", text="Create Pattern Piece")
