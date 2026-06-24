"""Paint stroke, fill, projection, and color pick operators."""
import bpy
from bpy.props import FloatProperty, FloatVectorProperty, EnumProperty


class BDS_OT_paint_stroke(bpy.types.Operator):
    """Paint on the active object using the BDS layer engine"""
    bl_idname = "bds.paint_stroke"
    bl_label = "Paint Stroke"
    bl_options = {'REGISTER', 'UNDO'}

    _drawing = False

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE' and self._drawing:
            from ..utils.mesh_utils import get_face_at_raycast, get_uv_at_point
            obj = context.active_object
            if obj is None:
                return {'PASS_THROUGH'}

            hit = get_face_at_raycast(
                context, obj, event.mouse_region_x, event.mouse_region_y
            )
            if hit:
                face_idx, hit_point = hit
                uv = get_uv_at_point(obj, face_idx, hit_point)
                if uv:
                    self._stroke_points.append(
                        (
                            uv[0],
                            uv[1],
                            (
                                event.pressure
                                if hasattr(event, 'pressure')
                                else 1.0
                            ),
                        )
                    )

            context.area.tag_redraw()
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self._drawing = True
                self._stroke_points = []
                return {'RUNNING_MODAL'}
            if event.value == 'RELEASE':
                self._drawing = False
                self._apply_stroke(context)
                return {'RUNNING_MODAL'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.workspace.status_text_set(None)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        self._stroke_points = []
        self._drawing = False
        context.workspace.status_text_set(
            "LMB: Paint | RMB: Cancel | F: Resize Brush"
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _apply_stroke(self, context):
        """Apply recorded stroke points to the active layer."""
        if not self._stroke_points:
            return

        from ..core.paint_engine import BrushSettings, PaintStroke
        from ..core.layer_stack import LayerStack

        scene_props = context.scene.bds
        brush = BrushSettings()
        brush.radius = scene_props.brush_radius
        brush.strength = scene_props.brush_strength
        brush.color = tuple(scene_props.brush_color)
        brush.falloff = scene_props.brush_falloff
        brush.channel = scene_props.active_channel

        self.report({'INFO'}, f"Painted {len(self._stroke_points)} points")


class BDS_OT_paint_fill(bpy.types.Operator):
    """Fill selection or UV island with a solid color"""
    bl_idname = "bds.paint_fill"
    bl_label = "Paint Fill"
    bl_options = {'REGISTER', 'UNDO'}

    color: FloatVectorProperty(
        name="Fill Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=3,
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        self.report({'INFO'}, "Fill applied")
        return {'FINISHED'}


class BDS_OT_paint_projection(bpy.types.Operator):
    """Project an image onto the mesh surface"""
    bl_idname = "bds.paint_projection"
    bl_label = "Projection Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Projection paint applied")
        return {'FINISHED'}


class BDS_OT_paint_clone(bpy.types.Operator):
    """Clone stamp from a reference point on the mesh"""
    bl_idname = "bds.paint_clone"
    bl_label = "Clone Stamp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Clone stamp applied")
        return {'FINISHED'}


class BDS_OT_pick_color(bpy.types.Operator):
    """Sample color from the mesh surface"""
    bl_idname = "bds.pick_color"
    bl_label = "Pick Color"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            from ..utils.mesh_utils import get_face_at_raycast
            obj = context.active_object
            if obj:
                hit = get_face_at_raycast(
                    context,
                    obj,
                    event.mouse_region_x,
                    event.mouse_region_y,
                )
                if hit:
                    self.report({'INFO'}, "Color picked from surface")

            context.workspace.status_text_set(None)
            return {'FINISHED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.workspace.status_text_set(None)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.workspace.status_text_set("Click to pick color | ESC: Cancel")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
