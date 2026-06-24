import bpy


class BDS_OT_create_pattern(bpy.types.Operator):
    """Create a simple pattern mesh (placeholder)"""
    bl_idname = "bds.create_pattern"
    bl_label = "Create Pattern"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # create a simple plane mesh as a placeholder for a pattern piece
        mesh = bpy.data.meshes.new("Pattern_Piece")
        obj = bpy.data.objects.new("Pattern_Piece", mesh)
        context.collection.objects.link(obj)

        verts = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)]
        faces = [(0, 1, 2, 3)]
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        # select the new object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        self.report({'INFO'}, "Pattern piece created")
        return {'FINISHED'}
