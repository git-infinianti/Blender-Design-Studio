"""Pattern creation, editing, and management operators."""
import bpy
from bpy.props import FloatProperty, StringProperty, EnumProperty, IntProperty


class BDS_OT_create_pattern(bpy.types.Operator):
    """Create a new pattern piece"""
    bl_idname = "bds.create_pattern"
    bl_label = "Create Pattern"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty(name="Name", default="Pattern_Piece")
    width: FloatProperty(name="Width", default=1.0, min=0.1, max=10.0)
    height: FloatProperty(name="Height", default=1.0, min=0.1, max=10.0)

    def execute(self, context):
        mesh = bpy.data.meshes.new(self.name)
        obj = bpy.data.objects.new(self.name, mesh)
        context.collection.objects.link(obj)

        w, h = self.width, self.height
        verts = [(0, 0, 0), (w, 0, 0), (w, h, 0), (0, h, 0)]
        faces = [(0, 1, 2, 3)]
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        if not mesh.uv_layers:
            mesh.uv_layers.new(name="UVMap")

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        scene_props = context.scene.bds
        piece = scene_props.pattern_pieces.add()
        piece.name = self.name

        self.report({'INFO'}, f"Pattern piece '{self.name}' created")
        return {'FINISHED'}


class BDS_OT_add_pattern_point(bpy.types.Operator):
    """Add a vertex to the active pattern piece at the mouse position"""
    bl_idname = "bds.add_pattern_point"
    bl_label = "Add Pattern Point"
    bl_options = {'REGISTER', 'UNDO'}

    x: FloatProperty(name="X", default=0.0)
    y: FloatProperty(name="Y", default=0.0)

    def invoke(self, context, event):
        from bpy_extras import view3d_utils
        region = context.region
        rv3d = context.space_data.region_3d
        coord = (event.mouse_region_x, event.mouse_region_y)
        loc = view3d_utils.region_2d_to_location_3d(
            region, rv3d, coord, (0, 0, 0)
        )
        self.x = loc.x
        self.y = loc.y
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.new((self.x, self.y, 0.0))
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        self.report({'INFO'}, f"Point added at ({self.x:.2f}, {self.y:.2f})")
        return {'FINISHED'}


class BDS_OT_move_pattern_point(bpy.types.Operator):
    """Move selected pattern vertices"""
    bl_idname = "bds.move_pattern_point"
    bl_label = "Move Pattern Point"
    bl_options = {'REGISTER', 'UNDO'}

    offset_x: FloatProperty(name="Offset X", default=0.0)
    offset_y: FloatProperty(name="Offset Y", default=0.0)

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.from_edit_mesh(obj.data) if obj.mode == 'EDIT' else None
        if bm is None:
            self.report({'WARNING'}, "Must be in edit mode")
            return {'CANCELLED'}

        for v in bm.verts:
            if v.select:
                v.co.x += self.offset_x
                v.co.y += self.offset_y

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


class BDS_OT_delete_pattern_element(bpy.types.Operator):
    """Delete selected pattern vertices or edges"""
    bl_idname = "bds.delete_pattern_element"
    bl_label = "Delete Pattern Element"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
            self.report({'WARNING'}, "Must be in edit mode on a mesh")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)

        selected_verts = [v for v in bm.verts if v.select]
        if selected_verts:
            bmesh.ops.delete(bm, geom=selected_verts, context='VERTS')

        bmesh.update_edit_mesh(obj.data)
        self.report({'INFO'}, f"Deleted {len(selected_verts)} vertices")
        return {'FINISHED'}


class BDS_OT_mirror_pattern(bpy.types.Operator):
    """Mirror the active pattern piece across an axis"""
    bl_idname = "bds.mirror_pattern"
    bl_label = "Mirror Pattern"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        items=[('X', 'X', 'Mirror across X axis'),
               ('Y', 'Y', 'Mirror across Y axis')],
        default='X',
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        result = bmesh.ops.duplicate(bm, geom=geom)

        for vert in result['geom']:
            if isinstance(vert, bmesh.types.BMVert):
                if self.axis == 'X':
                    vert.co.x = -vert.co.x
                else:
                    vert.co.y = -vert.co.y

        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        self.report({'INFO'}, f"Pattern mirrored across {self.axis} axis")
        return {'FINISHED'}


class BDS_OT_triangulate_pattern(bpy.types.Operator):
    """Triangulate the active pattern piece"""
    bl_idname = "bds.triangulate_pattern"
    bl_label = "Triangulate Pattern"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object")
            return {'CANCELLED'}

        import bmesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        bmesh.ops.triangulate(bm, faces=bm.faces[:])

        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        self.report({'INFO'}, "Pattern triangulated")
        return {'FINISHED'}


class BDS_OT_import_pattern(bpy.types.Operator):
    """Import a pattern from SVG or DXF file"""
    bl_idname = "bds.import_pattern"
    bl_label = "Import Pattern"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(subtype='FILE_PATH')
    filter_glob: StringProperty(default="*.svg;*.dxf", options={'HIDDEN'})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.filepath:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}

        if self.filepath.lower().endswith('.svg'):
            return self._import_svg(context)
        if self.filepath.lower().endswith('.dxf'):
            return self._import_dxf(context)

        self.report({'WARNING'}, "Unsupported file format")
        return {'CANCELLED'}

    def _import_svg(self, context):
        """Parse SVG path elements into pattern geometry."""
        import xml.etree.ElementTree as ET

        try:
            tree = ET.parse(self.filepath)
        except ET.ParseError as e:
            self.report({'ERROR'}, f"Failed to parse SVG: {e}")
            return {'CANCELLED'}

        root = tree.getroot()

        verts = []
        edges = []

        for path_elem in root.iter('{http://www.w3.org/2000/svg}path'):
            d = path_elem.get('d', '')
            points = self._parse_svg_path(d)
            start_idx = len(verts)
            for px, py in points:
                verts.append((px, -py, 0.0))
            for i in range(len(points) - 1):
                edges.append((start_idx + i, start_idx + i + 1))
            if len(points) > 2:
                edges.append((start_idx + len(points) - 1, start_idx))

        for poly in root.iter('{http://www.w3.org/2000/svg}polygon'):
            points_str = poly.get('points', '')
            points = self._parse_svg_points(points_str)
            start_idx = len(verts)
            for px, py in points:
                verts.append((px, -py, 0.0))
            for i in range(len(points) - 1):
                edges.append((start_idx + i, start_idx + i + 1))
            if len(points) > 2:
                edges.append((start_idx + len(points) - 1, start_idx))

        if not verts:
            self.report({'WARNING'}, "No geometry found in SVG")
            return {'CANCELLED'}

        mesh = bpy.data.meshes.new("Imported_Pattern")
        obj = bpy.data.objects.new("Imported_Pattern", mesh)
        context.collection.objects.link(obj)
        mesh.from_pydata(verts, edges, [])
        mesh.update()

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        self.report({'INFO'}, f"Imported {len(verts)} vertices from SVG")
        return {'FINISHED'}

    def _import_dxf(self, context):
        """Parse DXF entities (LINE, LWPOLYLINE) into pattern geometry."""
        verts = []
        edges = []

        try:
            with open(self.filepath, 'r') as f:
                lines = f.readlines()
        except OSError as e:
            self.report({'ERROR'}, f"Failed to read DXF: {e}")
            return {'CANCELLED'}

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line == 'LINE':
                x1 = y1 = x2 = y2 = 0.0
                i += 1
                while i < len(lines) and lines[i].strip() != '0':
                    code = lines[i].strip()
                    if i + 1 < len(lines):
                        val = lines[i + 1].strip()
                        if code == '10':
                            x1 = float(val)
                        elif code == '20':
                            y1 = float(val)
                        elif code == '11':
                            x2 = float(val)
                        elif code == '21':
                            y2 = float(val)
                    i += 2
                idx = len(verts)
                verts.extend([(x1, y1, 0), (x2, y2, 0)])
                edges.append((idx, idx + 1))

            elif line == 'LWPOLYLINE':
                poly_verts = []
                i += 1
                while i < len(lines) and lines[i].strip() != '0':
                    code = lines[i].strip()
                    if code == '10' and i + 1 < len(lines):
                        x = float(lines[i + 1].strip())
                        poly_verts.append([x, 0.0])
                    elif code == '20' and i + 1 < len(lines) and poly_verts:
                        poly_verts[-1][1] = float(lines[i + 1].strip())
                    i += 2
                start_idx = len(verts)
                for px, py in poly_verts:
                    verts.append((px, py, 0.0))
                for j in range(len(poly_verts) - 1):
                    edges.append((start_idx + j, start_idx + j + 1))
            else:
                i += 1

        if not verts:
            self.report({'WARNING'}, "No geometry found in DXF")
            return {'CANCELLED'}

        mesh = bpy.data.meshes.new("Imported_Pattern")
        obj = bpy.data.objects.new("Imported_Pattern", mesh)
        context.collection.objects.link(obj)
        mesh.from_pydata(verts, edges, [])
        mesh.update()

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        self.report({'INFO'}, f"Imported {len(verts)} vertices from DXF")
        return {'FINISHED'}

    @staticmethod
    def _parse_svg_path(d: str):
        """Parse a simple SVG path 'd' attribute into coordinate pairs."""
        import re

        points = []
        tokens = re.findall(r'[MLHVCSTQAZmlhvcstqaz]|[-+]?[0-9]*\.?[0-9]+', d)
        x, y = 0.0, 0.0
        cmd = 'M'
        i = 0
        while i < len(tokens):
            if tokens[i].isalpha():
                cmd = tokens[i]
                i += 1
                continue

            if cmd in ('M', 'L'):
                x = float(tokens[i])
                y = float(tokens[i + 1]) if i + 1 < len(tokens) else 0
                points.append((x, y))
                i += 2
            elif cmd in ('m', 'l'):
                x += float(tokens[i])
                y += float(tokens[i + 1]) if i + 1 < len(tokens) else 0
                points.append((x, y))
                i += 2
            elif cmd == 'H':
                x = float(tokens[i])
                points.append((x, y))
                i += 1
            elif cmd == 'h':
                x += float(tokens[i])
                points.append((x, y))
                i += 1
            elif cmd == 'V':
                y = float(tokens[i])
                points.append((x, y))
                i += 1
            elif cmd == 'v':
                y += float(tokens[i])
                points.append((x, y))
                i += 1
            elif cmd in ('Z', 'z'):
                i += 1
            else:
                i += 1

        return points

    @staticmethod
    def _parse_svg_points(points_str: str):
        """Parse SVG points attribute (space or comma separated x,y pairs)."""
        import re

        coords = re.findall(r'[-+]?[0-9]*\.?[0-9]+', points_str)
        points = []
        for i in range(0, len(coords) - 1, 2):
            points.append((float(coords[i]), float(coords[i + 1])))
        return points
