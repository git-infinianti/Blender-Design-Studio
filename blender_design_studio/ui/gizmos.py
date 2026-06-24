"""Custom gizmos for seam handles and pattern control points."""
import bpy

try:
    from mathutils import Matrix
    HAS_MATHUTILS = True
except ImportError:
    HAS_MATHUTILS = False


class BDS_GT_seam_handle(bpy.types.Gizmo):
    """A single gizmo for a seam handle point"""

    bl_idname = "BDS_GT_seam_handle"

    def draw(self, context):
        self.draw_preset_circle(self.matrix_basis, axis='Z')

    def draw_select(self, context, select_id):
        self.draw_preset_circle(self.matrix_basis, axis='Z',
                                select_id=select_id)

    def test_select(self, context, location):
        return -1


class BDS_GGT_seam_handles(bpy.types.GizmoGroup):
    """Gizmo group for displaying seam connection handles"""

    bl_idname = "BDS_GGT_seam_handles"
    bl_label = "Seam Handles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        return (hasattr(context.scene, 'bds') and
                context.scene.bds.mode == 'PATTERN')

    def setup(self, context):
        pass

    def refresh(self, context):
        pass

    def draw_prepare(self, context):
        pass
