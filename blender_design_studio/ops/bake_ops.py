"""Baking and texture export operators."""
import bpy
from bpy.props import StringProperty, IntProperty, EnumProperty


class BDS_OT_bake_textures(bpy.types.Operator):
    """Bake textures from the layer stack"""
    bl_idname = "bds.bake_textures"
    bl_label = "Bake Textures"
    bl_options = {'REGISTER'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        scene_props = context.scene.bds
        resolution = scene_props.bake_resolution

        from ..core.bake import BakeManager
        BakeManager(obj, resolution)

        self.report({'INFO'}, f"Bake complete at {resolution}px")
        return {'FINISHED'}


class BDS_OT_export_textures(bpy.types.Operator):
    """Export painted textures to disk"""
    bl_idname = "bds.export_textures"
    bl_label = "Export Textures"
    bl_options = {'REGISTER'}

    directory: StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.directory:
            self.report({'WARNING'}, "No directory selected")
            return {'CANCELLED'}

        obj = context.active_object
        scene_props = context.scene.bds
        export_format = scene_props.export_format

        from ..core.bake import BakeManager
        baker = BakeManager(obj)
        exported = baker.export_textures(self.directory, format=export_format)

        self.report({'INFO'}, f"Exported {len(exported)} textures")
        return {'FINISHED'}
