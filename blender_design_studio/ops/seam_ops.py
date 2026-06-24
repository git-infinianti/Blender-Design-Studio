"""Seam stitching operators for garment assembly."""
import bpy
from bpy.props import IntProperty, EnumProperty, FloatProperty


class BDS_OT_select_seam_edge(bpy.types.Operator):
    """Select edges on pattern pieces to define seam pairs"""
    bl_idname = "bds.select_seam_edge"
    bl_label = "Select Seam Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
            self.report({'WARNING'}, "Select edges in edit mode")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
        selected = [e.index for e in bm.edges if e.select]

        if not selected:
            self.report({'WARNING'}, "No edges selected")
            return {'CANCELLED'}

        if "bds_seam_edges_a" not in obj:
            obj["bds_seam_edges_a"] = selected
            self.report(
                {'INFO'},
                f"Seam side A: {len(selected)} edges selected. "
                "Now select side B and run again.",
            )
        else:
            obj["bds_seam_edges_b"] = selected
            self.report(
                {'INFO'},
                f"Seam side B: {len(selected)} edges. "
                "Use 'Stitch Seams' to join.",
            )

        return {'FINISHED'}


class BDS_OT_stitch_seams(bpy.types.Operator):
    """Merge seam-paired vertices into a single mesh"""
    bl_idname = "bds.stitch_seams"
    bl_label = "Stitch Seams"
    bl_options = {'REGISTER', 'UNDO'}

    merge_distance: FloatProperty(
        name="Merge Distance",
        default=0.001,
        min=0.0001,
        max=0.1,
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        bmesh.ops.remove_doubles(
            bm, verts=bm.verts[:], dist=self.merge_distance
        )

        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        if "bds_seam_edges_a" in obj:
            del obj["bds_seam_edges_a"]
        if "bds_seam_edges_b" in obj:
            del obj["bds_seam_edges_b"]

        self.report({'INFO'}, "Seams stitched")
        return {'FINISHED'}


class BDS_OT_auto_seam(bpy.types.Operator):
    """Auto-match edges by proximity and length for seam stitching"""
    bl_idname = "bds.auto_seam"
    bl_label = "Auto Seam"
    bl_options = {'REGISTER', 'UNDO'}

    threshold: FloatProperty(
        name="Match Threshold",
        default=0.05,
        min=0.001,
        max=1.0,
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.edges.ensure_lookup_table()

        boundary_edges = [e for e in bm.edges if e.is_boundary]

        if len(boundary_edges) < 2:
            bm.free()
            self.report({'WARNING'}, "Not enough boundary edges to auto-seam")
            return {'CANCELLED'}

        matched = 0
        used = set()

        for i, e1 in enumerate(boundary_edges):
            if i in used:
                continue
            l1 = e1.calc_length()
            mid1 = (e1.verts[0].co + e1.verts[1].co) / 2

            best_match = None
            best_dist = self.threshold

            for j, e2 in enumerate(boundary_edges):
                if j <= i or j in used:
                    continue
                l2 = e2.calc_length()
                if abs(l1 - l2) > self.threshold:
                    continue
                mid2 = (e2.verts[0].co + e2.verts[1].co) / 2
                dist = (mid1 - mid2).length
                if dist < best_dist:
                    best_dist = dist
                    best_match = j

            if best_match is not None:
                used.add(i)
                used.add(best_match)
                matched += 1

        bm.free()
        self.report({'INFO'}, f"Auto-matched {matched} seam pairs")
        return {'FINISHED'}


class BDS_OT_remove_seam(bpy.types.Operator):
    """Remove seam pair data from the active object"""
    bl_idname = "bds.remove_seam"
    bl_label = "Remove Seam"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        removed = False
        if "bds_seam_edges_a" in obj:
            del obj["bds_seam_edges_a"]
            removed = True
        if "bds_seam_edges_b" in obj:
            del obj["bds_seam_edges_b"]
            removed = True

        if removed:
            self.report({'INFO'}, "Seam data removed")
        else:
            self.report({'INFO'}, "No seam data to remove")
        return {'FINISHED'}
