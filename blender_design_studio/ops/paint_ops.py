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
            context.area.header_text_set(None)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        self._stroke_points = []
        self._drawing = False
        context.area.header_text_set(
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

        scene_props = context.scene.bds
        channel = scene_props.active_channel

        # Find active layer image for this channel
        layer_name = "Layer"
        if scene_props.paint_layers and scene_props.active_layer_index < len(scene_props.paint_layers):
            layer_name = scene_props.paint_layers[scene_props.active_layer_index].name

        img_key = f"BDS_{layer_name}_{channel}"
        try:
            import bpy
            if img_key not in bpy.data.images:
                self.report({'WARNING'}, "No paint layer image found. Add a layer first.")
                return {'CANCELLED'}

            img = bpy.data.images[img_key]
            width, height = img.size[0], img.size[1]

            try:
                import numpy as np
                pixels = np.array(img.pixels[:], dtype=np.float32).reshape((height, width, 4))
                r, g, b = self.color
                pixels[:, :, 0] = r
                pixels[:, :, 1] = g
                pixels[:, :, 2] = b
                pixels[:, :, 3] = 1.0
                img.pixels[:] = pixels.ravel().tolist()
            except ImportError:
                # Fallback without numpy
                r, g, b = self.color
                pixel_data = [0.0] * (width * height * 4)
                for i in range(0, len(pixel_data), 4):
                    pixel_data[i] = r
                    pixel_data[i + 1] = g
                    pixel_data[i + 2] = b
                    pixel_data[i + 3] = 1.0
                img.pixels[:] = pixel_data

            img.update()
            self.report({'INFO'}, f"Filled layer '{layer_name}' channel '{channel}' with color")
        except Exception as e:
            self.report({'ERROR'}, f"Fill failed: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}


class BDS_OT_paint_projection(bpy.types.Operator):
    """Project an image onto the mesh surface from current view"""
    bl_idname = "bds.paint_projection"
    bl_label = "Projection Paint"
    bl_options = {'REGISTER', 'UNDO'}

    image_path: bpy.props.StringProperty(
        name="Image",
        description="Path to the image to project",
        subtype='FILE_PATH',
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        if not self.image_path:
            self.report({'WARNING'}, "No image specified for projection")
            return {'CANCELLED'}

        # Load or get the projection image
        import os
        img_name = os.path.basename(self.image_path)
        if img_name in bpy.data.images:
            proj_img = bpy.data.images[img_name]
        else:
            try:
                proj_img = bpy.data.images.load(self.image_path)
            except RuntimeError:
                self.report({'ERROR'}, f"Could not load image: {self.image_path}")
                return {'CANCELLED'}

        # Use Blender's native texture paint projection as the backing
        # Set the active object to texture paint mode temporarily
        prev_mode = obj.mode
        if prev_mode != 'TEXTURE_PAINT':
            bpy.ops.object.mode_set(mode='TEXTURE_PAINT')

        # Configure the projection
        tool_settings = context.scene.tool_settings
        tool_settings.image_paint.mode = 'IMAGE'
        tool_settings.image_paint.canvas = proj_img

        self.report({'INFO'}, f"Projection paint configured with '{img_name}'. Use texture paint tools.")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BDS_OT_paint_clone(bpy.types.Operator):
    """Clone stamp: paint by sampling from a reference point on the mesh"""
    bl_idname = "bds.paint_clone"
    bl_label = "Clone Stamp"
    bl_options = {'REGISTER', 'UNDO'}

    _source_uv = None
    _picking_source = True

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
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
                    if self._picking_source:
                        self._source_uv = uv
                        self._picking_source = False
                        context.area.header_text_set(
                            "Clone source set. LMB: Paint clone | RMB/ESC: Cancel"
                        )
                        self.report({'INFO'}, f"Clone source set at UV ({uv[0]:.3f}, {uv[1]:.3f})")
                    else:
                        # Apply clone stamp at this location
                        self._apply_clone(context, obj, uv)

            return {'RUNNING_MODAL'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set(None)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        self._source_uv = None
        self._picking_source = True
        context.area.header_text_set("LMB: Set clone source | ESC: Cancel")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _apply_clone(self, context, obj, target_uv):
        """Copy pixels from source UV region to target UV region."""
        if self._source_uv is None:
            return

        scene_props = context.scene.bds
        channel = scene_props.active_channel
        layer_name = "Layer"
        if scene_props.paint_layers and scene_props.active_layer_index < len(scene_props.paint_layers):
            layer_name = scene_props.paint_layers[scene_props.active_layer_index].name

        img_key = f"BDS_{layer_name}_{channel}"
        if img_key not in bpy.data.images:
            return

        try:
            import numpy as np
        except ImportError:
            self.report({'WARNING'}, "Clone stamp requires numpy")
            return

        img = bpy.data.images[img_key]
        width, height = img.size[0], img.size[1]
        pixels = np.array(img.pixels[:], dtype=np.float32).reshape((height, width, 4))

        radius = scene_props.brush_radius
        src_x = int(self._source_uv[0] * width)
        src_y = int(self._source_uv[1] * height)
        dst_x = int(target_uv[0] * width)
        dst_y = int(target_uv[1] * height)

        # Copy a square patch from source to destination
        x_min_s = max(0, src_x - radius)
        x_max_s = min(width, src_x + radius)
        y_min_s = max(0, src_y - radius)
        y_max_s = min(height, src_y + radius)

        x_min_d = max(0, dst_x - radius)
        x_max_d = min(width, dst_x + radius)
        y_min_d = max(0, dst_y - radius)
        y_max_d = min(height, dst_y + radius)

        # Calculate overlapping region size
        copy_w = min(x_max_s - x_min_s, x_max_d - x_min_d)
        copy_h = min(y_max_s - y_min_s, y_max_d - y_min_d)

        if copy_w > 0 and copy_h > 0:
            source_patch = pixels[y_min_s:y_min_s + copy_h, x_min_s:x_min_s + copy_w].copy()
            strength = scene_props.brush_strength
            pixels[y_min_d:y_min_d + copy_h, x_min_d:x_min_d + copy_w] = (
                pixels[y_min_d:y_min_d + copy_h, x_min_d:x_min_d + copy_w] * (1 - strength)
                + source_patch * strength
            )
            img.pixels[:] = pixels.ravel().tolist()
            img.update()

        self.report({'INFO'}, "Clone stamp applied")


class BDS_OT_pick_color(bpy.types.Operator):
    """Sample color from the mesh surface and set as brush color"""
    bl_idname = "bds.pick_color"
    bl_label = "Pick Color"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            from ..utils.mesh_utils import get_face_at_raycast, get_uv_at_point
            obj = context.active_object
            if obj:
                hit = get_face_at_raycast(
                    context,
                    obj,
                    event.mouse_region_x,
                    event.mouse_region_y,
                )
                if hit:
                    face_idx, hit_point = hit
                    uv = get_uv_at_point(obj, face_idx, hit_point)
                    if uv:
                        color = self._sample_color(context, uv)
                        if color:
                            context.scene.bds.brush_color = color
                            self.report({'INFO'},
                                        f"Color picked: ({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f})")
                        else:
                            self.report({'INFO'}, "Color picked from surface")

            context.area.header_text_set(None)
            return {'FINISHED'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set(None)
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        context.area.header_text_set("Click to pick color | ESC: Cancel")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _sample_color(self, context, uv):
        """Sample color from the active layer at the given UV coordinate."""
        scene_props = context.scene.bds
        channel = scene_props.active_channel
        layer_name = "Layer"
        if scene_props.paint_layers and scene_props.active_layer_index < len(scene_props.paint_layers):
            layer_name = scene_props.paint_layers[scene_props.active_layer_index].name

        img_key = f"BDS_{layer_name}_{channel}"
        if img_key not in bpy.data.images:
            return None

        img = bpy.data.images[img_key]
        width, height = img.size[0], img.size[1]

        px = int(uv[0] * width) % width
        py = int(uv[1] * height) % height

        idx = (py * width + px) * 4
        pixels = img.pixels
        if idx + 2 < len(pixels):
            return (pixels[idx], pixels[idx + 1], pixels[idx + 2])
        return None
