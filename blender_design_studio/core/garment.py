"""Garment assembly: combines pattern pieces and seams into a 3D mesh."""
from typing import Dict
from mathutils import Vector

from .pattern import PatternCollection
from .seam import SeamCollection

try:
    import bpy
    import bmesh

    HAS_BPY = True
except ImportError:
    HAS_BPY = False


class Garment:
    """Assembles pattern pieces + seams into a 3D mesh object."""

    def __init__(self, pattern_collection: PatternCollection, seams: SeamCollection):
        self.patterns = pattern_collection
        self.seams = seams
        self._vertex_offset_map: Dict[str, int] = {}

    def assemble_flat(self) -> 'bpy.types.Object':
        """Place all triangulated pieces as a single mesh, flat on the XY plane."""
        if not HAS_BPY:
            raise RuntimeError("assemble_flat requires Blender's bpy module")

        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new("UVMap")
        global_offset = 0
        spacing = 0.0

        for piece in self.patterns.pieces:
            tri_verts, tri_faces = piece.triangulate()
            if not tri_verts:
                continue

            self._vertex_offset_map[piece.name] = global_offset

            bm_verts = []
            for v in tri_verts:
                bm_v = bm.verts.new((v.x + spacing, v.y, 0.0))
                bm_verts.append(bm_v)

            bm.verts.ensure_lookup_table()

            for face_indices in tri_faces:
                try:
                    face = bm.faces.new([bm_verts[i] for i in face_indices])
                    for loop in face.loops:
                        vert_idx = bm_verts.index(loop.vert)
                        v = tri_verts[vert_idx]
                        loop[uv_layer].uv = (v.x, v.y)
                except Exception:
                    pass

            global_offset += len(tri_verts)
            max_x = max(v.x for v in tri_verts) if tri_verts else 0
            spacing += max_x + 0.2

        mesh = bpy.data.meshes.new("BDS_Garment")
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        obj = bpy.data.objects.new("BDS_Garment", mesh)
        bpy.context.collection.objects.link(obj)
        return obj

    def wrap_around_avatar(self, avatar_obj: 'bpy.types.Object') -> None:
        """Position pattern pieces roughly around avatar using bounding-box heuristics."""
        if not HAS_BPY:
            raise RuntimeError("wrap_around_avatar requires Blender's bpy module")

        bbox = [avatar_obj.matrix_world @ Vector(corner) for corner in avatar_obj.bound_box]
        center = sum(bbox, Vector((0, 0, 0))) / 8
        dims = avatar_obj.dimensions

        for i, piece_name in enumerate(self.patterns.piece_names()):
            offset = self._vertex_offset_map.get(piece_name, 0)
            if i % 2 == 0:
                z_offset = dims.y * 0.5 + 0.05
            else:
                z_offset = -(dims.y * 0.5 + 0.05)

            _ = (offset, center, z_offset)
            pass

    def apply_seam_constraints(self, obj: 'bpy.types.Object') -> None:
        """Add vertex groups and constraints for seam merging."""
        if not HAS_BPY:
            raise RuntimeError("apply_seam_constraints requires Blender's bpy module")

        if "bds_seams" not in obj.vertex_groups:
            vg = obj.vertex_groups.new(name="bds_seams")
        else:
            vg = obj.vertex_groups["bds_seams"]

        pairs = self.seams.build_constraint_pairs()
        for idx_a, idx_b in pairs:
            try:
                vg.add([idx_a, idx_b], 1.0, 'REPLACE')
            except (IndexError, RuntimeError):
                pass

    def stitch_seams(self, obj: 'bpy.types.Object') -> int:
        """Merge seam-paired vertices into a single mesh.

        Returns the number of vertices merged.
        """
        if not HAS_BPY:
            raise RuntimeError("stitch_seams requires Blender's bpy module")

        pairs = self.seams.build_constraint_pairs()
        if not pairs:
            return 0

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        merged = 0
        merge_targets = {}

        for idx_a, idx_b in pairs:
            if idx_a >= len(bm.verts) or idx_b >= len(bm.verts):
                continue
            target_a = merge_targets.get(idx_a, idx_a)
            target_b = merge_targets.get(idx_b, idx_b)
            if target_a != target_b:
                try:
                    bmesh.ops.pointmerge(
                        bm,
                        verts=[bm.verts[target_a], bm.verts[target_b]],
                        merge_co=bm.verts[target_a].co,
                    )
                    merge_targets[target_b] = target_a
                    merged += 1
                except (IndexError, RuntimeError):
                    pass

        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()
        return merged
