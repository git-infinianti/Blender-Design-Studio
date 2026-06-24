"""Import/export operators for patterns and textures."""
import bpy
from bpy.props import StringProperty, EnumProperty


class BDS_OT_export_pattern(bpy.types.Operator):
    """Export pattern pieces to SVG"""
    bl_idname = "bds.export_pattern"
    bl_label = "Export Pattern"
    bl_options = {'REGISTER'}

    filepath: StringProperty(subtype='FILE_PATH')
    filter_glob: StringProperty(default="*.svg", options={'HIDDEN'})

    def invoke(self, context, event):
        self.filepath = "pattern_export.svg"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        try:
            self._export_svg(obj)
            self.report({'INFO'}, f"Pattern exported to {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

    def _export_svg(self, obj):
        """Export mesh vertices/edges as SVG paths."""
        mesh = obj.data
        verts = [(v.co.x, v.co.y) for v in mesh.vertices]
        edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]

        if not verts:
            return

        min_x = min(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_x = max(v[0] for v in verts)
        max_y = max(v[1] for v in verts)
        padding = 0.1
        width = (max_x - min_x) + padding * 2
        height = (max_y - min_y) + padding * 2

        scale = 100

        with open(self.filepath, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="{(min_x - padding) * scale} '
                f'{(min_y - padding) * scale} '
                f'{width * scale} {height * scale}">\n'
            )

            for a, b in edges:
                x1, y1 = verts[a]
                x2, y2 = verts[b]
                f.write(
                    f'  <line x1="{x1 * scale}" y1="{y1 * scale}" '
                    f'x2="{x2 * scale}" y2="{y2 * scale}" '
                    f'stroke="black" stroke-width="1"/>\n'
                )

            for x, y in verts:
                f.write(
                    f'  <circle cx="{x * scale}" cy="{y * scale}" '
                    f'r="2" fill="red"/>\n'
                )

            f.write('</svg>\n')
