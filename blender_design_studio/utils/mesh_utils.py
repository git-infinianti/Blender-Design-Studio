"""bmesh helpers and UV utilities for working with Blender meshes."""
from typing import Optional, Tuple

try:
    import bpy
    import bmesh
    from mathutils import Vector
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


def get_bmesh(obj) -> Optional['bmesh.types.BMesh']:
    """Get a bmesh from a mesh object. Caller must call bm.free() when done."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return None

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    return bm


def apply_bmesh(bm, obj) -> None:
    """Write bmesh back to object and free it."""
    if not HAS_BPY or bm is None or obj is None:
        return
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def get_uv_at_point(obj, face_index: int,
                    hit_point: 'Vector') -> Optional[Tuple[float, float]]:
    """Interpolate UV coordinates at a hit point on a face.
    
    Uses barycentric interpolation from the face vertices.
    """
    if not HAS_BPY or obj is None:
        return None

    mesh = obj.data
    if not mesh.uv_layers.active:
        return None

    uv_layer = mesh.uv_layers.active
    face = mesh.polygons[face_index]

    if len(face.vertices) < 3:
        return None

    # Get face vertices in world space
    verts = [obj.matrix_world @ mesh.vertices[vi].co for vi in face.vertices]

    # Compute barycentric coords for the first triangle
    v0 = verts[1] - verts[0]
    v1 = verts[2] - verts[0]
    v2 = hit_point - verts[0]

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < 1e-10:
        return None

    inv_denom = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom
    w = 1.0 - u - v

    # Get UVs for the face loop
    loop_start = face.loop_start
    uv0 = uv_layer.data[loop_start].uv
    uv1 = uv_layer.data[loop_start + 1].uv
    uv2 = uv_layer.data[loop_start + 2].uv

    # Interpolate
    result_u = w * uv0[0] + u * uv1[0] + v * uv2[0]
    result_v = w * uv0[1] + u * uv1[1] + v * uv2[1]

    return (result_u, result_v)


def get_face_at_raycast(context, obj, mouse_x: int,
                        mouse_y: int) -> Optional[Tuple[int, 'Vector']]:
    """Raycast from screen coordinates to find face index and hit point."""
    if not HAS_BPY or obj is None:
        return None

    from bpy_extras import view3d_utils

    region = context.region
    rv3d = context.space_data.region_3d

    # Get ray from mouse position
    coord = (mouse_x, mouse_y)
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    # Transform ray to object space
    mat_inv = obj.matrix_world.inverted()
    ray_origin_obj = mat_inv @ ray_origin
    ray_direction_obj = (mat_inv.to_3x3() @ view_vector).normalized()

    # Perform raycast
    result, location, normal, face_index = obj.ray_cast(
        ray_origin_obj, ray_direction_obj
    )

    if result:
        # Convert hit location back to world space
        hit_world = obj.matrix_world @ location
        return (face_index, hit_world)
    return None


def create_uv_layer(obj, name: str = "UVMap") -> bool:
    """Create a new UV layer on the object if it doesn't exist."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return False

    if name not in obj.data.uv_layers:
        obj.data.uv_layers.new(name=name)
        return True
    return False


def get_selected_vertices(obj) -> list:
    """Get indices of selected vertices in edit mode."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return []

    bm = bmesh.from_edit_mesh(obj.data)
    selected = [v.index for v in bm.verts if v.select]
    return selected


def get_selected_edges(obj) -> list:
    """Get indices of selected edges in edit mode."""
    if not HAS_BPY or obj is None or obj.type != 'MESH':
        return []

    bm = bmesh.from_edit_mesh(obj.data)
    selected = [e.index for e in bm.edges if e.select]
    return selected
