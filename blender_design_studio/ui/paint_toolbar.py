"""Paint tool bar for brush and tool selection."""
import bpy


class BDS_PT_paint_toolbar(bpy.types.Panel):
    """Toolbar for painting tools"""

    bl_label = "Paint Toolbar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_paint_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator("bds.paint_stroke", text="", icon='BRUSH_DATA')
        row.operator("bds.paint_fill", text="", icon='COLOR')
        row.operator("bds.paint_projection", text="", icon='IMAGE_DATA')
        row.operator("bds.paint_clone", text="", icon='MOD_SHRINKWRAP')
        row.operator("bds.pick_color", text="", icon='EYEDROPPER')
