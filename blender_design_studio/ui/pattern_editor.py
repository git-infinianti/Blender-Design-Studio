"""2D Pattern Editor mode toggle and viewport configuration."""
import bpy
from mathutils import Quaternion


class BDS_OT_enter_pattern_mode(bpy.types.Operator):
    """Toggle pattern editing mode (orthographic top-down 2D view)"""

    bl_idname = "bds.enter_pattern_mode"
    bl_label = "Pattern Mode"
    bl_options = {'REGISTER'}

    _original_view = None

    def execute(self, context):
        space = context.space_data
        if space.type != 'VIEW_3D':
            self.report({'WARNING'}, "Must be in a 3D viewport")
            return {'CANCELLED'}

        rv3d = space.region_3d

        if rv3d.view_perspective != 'ORTHO':
            rv3d.view_perspective = 'ORTHO'
            rv3d.view_rotation = Quaternion((1, 0, 0, 0))
            context.scene.bds.mode = 'PATTERN'
            self.report({'INFO'}, "Entered Pattern Mode (2D)")
        else:
            rv3d.view_perspective = 'PERSP'
            self.report({'INFO'}, "Exited Pattern Mode")

        context.area.tag_redraw()
        return {'FINISHED'}
