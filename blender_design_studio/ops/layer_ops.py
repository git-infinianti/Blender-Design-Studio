"""Layer stack management operators."""
import bpy
from bpy.props import StringProperty, IntProperty, EnumProperty


class BDS_OT_layer_add(bpy.types.Operator):
    """Add a new paint layer"""
    bl_idname = "bds.layer_add"
    bl_label = "Add Layer"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Layer Name", default="Layer")

    def execute(self, context):
        scene_props = context.scene.bds
        layer = scene_props.paint_layers.add()
        layer.name = (
            self.name if self.name else f"Layer {len(scene_props.paint_layers)}"
        )
        scene_props.active_layer_index = len(scene_props.paint_layers) - 1

        self.report({'INFO'}, f"Layer '{layer.name}' added")
        return {'FINISHED'}


class BDS_OT_layer_remove(bpy.types.Operator):
    """Remove the active paint layer"""
    bl_idname = "bds.layer_remove"
    bl_label = "Remove Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene_props = context.scene.bds
        idx = scene_props.active_layer_index

        if idx < 0 or idx >= len(scene_props.paint_layers):
            self.report({'WARNING'}, "No layer to remove")
            return {'CANCELLED'}

        name = scene_props.paint_layers[idx].name
        scene_props.paint_layers.remove(idx)

        if scene_props.active_layer_index >= len(scene_props.paint_layers):
            scene_props.active_layer_index = max(
                0, len(scene_props.paint_layers) - 1
            )

        self.report({'INFO'}, f"Layer '{name}' removed")
        return {'FINISHED'}


class BDS_OT_layer_move(bpy.types.Operator):
    """Move the active layer up or down in the stack"""
    bl_idname = "bds.layer_move"
    bl_label = "Move Layer"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[('UP', 'Up', 'Move layer up'),
               ('DOWN', 'Down', 'Move layer down')],
        default='UP',
    )

    def execute(self, context):
        scene_props = context.scene.bds
        idx = scene_props.active_layer_index
        layers = scene_props.paint_layers

        if self.direction == 'UP' and idx > 0:
            layers.move(idx, idx - 1)
            scene_props.active_layer_index = idx - 1
        elif self.direction == 'DOWN' and idx < len(layers) - 1:
            layers.move(idx, idx + 1)
            scene_props.active_layer_index = idx + 1
        else:
            return {'CANCELLED'}

        return {'FINISHED'}


class BDS_OT_layer_duplicate(bpy.types.Operator):
    """Duplicate the active paint layer"""
    bl_idname = "bds.layer_duplicate"
    bl_label = "Duplicate Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene_props = context.scene.bds
        idx = scene_props.active_layer_index

        if idx < 0 or idx >= len(scene_props.paint_layers):
            self.report({'WARNING'}, "No layer to duplicate")
            return {'CANCELLED'}

        src = scene_props.paint_layers[idx]
        dup = scene_props.paint_layers.add()
        dup.name = f"{src.name}_copy"
        dup.visible = src.visible
        dup.opacity = src.opacity
        dup.blend_mode = src.blend_mode

        layers = scene_props.paint_layers
        layers.move(len(layers) - 1, idx + 1)
        scene_props.active_layer_index = idx + 1

        self.report({'INFO'}, f"Layer '{dup.name}' duplicated")
        return {'FINISHED'}


class BDS_OT_layer_merge_down(bpy.types.Operator):
    """Merge the active layer with the one below"""
    bl_idname = "bds.layer_merge_down"
    bl_label = "Merge Down"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene_props = context.scene.bds
        idx = scene_props.active_layer_index

        if idx <= 0 or idx >= len(scene_props.paint_layers):
            self.report({'WARNING'}, "Cannot merge down")
            return {'CANCELLED'}

        scene_props.paint_layers.remove(idx)
        scene_props.active_layer_index = idx - 1

        self.report({'INFO'}, "Layers merged")
        return {'FINISHED'}


class BDS_OT_layer_flatten(bpy.types.Operator):
    """Flatten all visible layers into one"""
    bl_idname = "bds.layer_flatten"
    bl_label = "Flatten Layers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene_props = context.scene.bds

        if len(scene_props.paint_layers) <= 1:
            self.report({'INFO'}, "Nothing to flatten")
            return {'CANCELLED'}

        while len(scene_props.paint_layers) > 1:
            scene_props.paint_layers.remove(len(scene_props.paint_layers) - 1)

        scene_props.paint_layers[0].name = "Flattened"
        scene_props.active_layer_index = 0

        self.report({'INFO'}, "Layers flattened")
        return {'FINISHED'}
