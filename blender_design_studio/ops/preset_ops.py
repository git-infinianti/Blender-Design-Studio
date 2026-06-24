"""Operators for garment presets and batch texture export."""
import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty


class BDS_OT_load_garment_preset(bpy.types.Operator):
    """Load a pre-built garment template with pattern pieces and seams"""
    bl_idname = "bds.load_garment_preset"
    bl_label = "Load Garment Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset: EnumProperty(
        name="Preset",
        items=[
            ('tshirt', 'T-Shirt', 'Basic short-sleeve t-shirt'),
            ('skirt', 'A-Line Skirt', 'Four-panel A-line skirt'),
            ('pants', 'Basic Pants', 'Simple straight-leg pants'),
            ('dress', 'Simple Dress', 'A-line dress with bodice and skirt'),
            ('hoodie', 'Hoodie', 'Hooded sweatshirt with sleeves and hood'),
            ('tank_top', 'Tank Top', 'Sleeveless tank top'),
            ('bomber', 'Bomber Jacket', 'Bomber jacket with ribbed collar'),
        ],
        default='tshirt',
    )

    def execute(self, context):
        from ..core.garment_presets import load_preset, GARMENT_PRESETS
        from ..core.garment import Garment

        try:
            patterns, seams = load_preset(self.preset)
        except ValueError as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        # Add pattern pieces to scene properties
        scene_props = context.scene.bds
        for piece in patterns.pieces:
            item = scene_props.pattern_pieces.add()
            item.name = piece.name
            preset_info = GARMENT_PRESETS.get(self.preset)
            if preset_info:
                item.fabric_preset = preset_info.default_fabric

        # Assemble the garment as a flat mesh
        garment = Garment(patterns, seams)
        obj = garment.assemble_flat()

        if obj:
            # Mark as garment
            obj.bds_object.is_garment = True
            obj.bds_object.garment_name = GARMENT_PRESETS[self.preset].name

            # Select and make active
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

        self.report({'INFO'},
                    f"Loaded garment preset: {GARMENT_PRESETS[self.preset].name}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset")


class BDS_OT_batch_export_textures(bpy.types.Operator):
    """Export all texture channels for all painted objects in the scene"""
    bl_idname = "bds.batch_export_textures"
    bl_label = "Batch Export Textures"
    bl_options = {'REGISTER'}

    output_dir: StringProperty(
        name="Output Directory",
        description="Directory to export textures to",
        default="//textures/",
        subtype='DIR_PATH',
    )
    format: EnumProperty(
        name="Format",
        items=[
            ('PNG', 'PNG', 'PNG format (lossless)'),
            ('JPEG', 'JPEG', 'JPEG format (lossy, smaller)'),
            ('OPEN_EXR', 'OpenEXR', 'EXR format (HDR, large)'),
            ('TARGA', 'Targa', 'TGA format'),
        ],
        default='PNG',
    )
    include_flattened: BoolProperty(
        name="Flatten Layers",
        description="Export flattened layer composites instead of individual layers",
        default=True,
    )

    def execute(self, context):
        import os

        output_path = bpy.path.abspath(self.output_dir)
        os.makedirs(output_path, exist_ok=True)

        exported_count = 0
        channels = ["base_color", "metallic", "roughness", "normal", "height"]

        # Find all BDS texture images
        for img in bpy.data.images:
            if not img.name.startswith("BDS_"):
                continue

            # Skip internal/temporary images
            if img.name.startswith("BDS_flat_") and not self.include_flattened:
                continue

            # Determine file extension
            ext_map = {'PNG': '.png', 'JPEG': '.jpg', 'OPEN_EXR': '.exr', 'TARGA': '.tga'}
            ext = ext_map.get(self.format, '.png')

            filename = img.name + ext
            filepath = os.path.join(output_path, filename)

            # Set format and save
            img.filepath_raw = filepath
            img.file_format = self.format
            try:
                img.save()
                exported_count += 1
            except RuntimeError as e:
                self.report({'WARNING'}, f"Could not save {img.name}: {e}")

        self.report({'INFO'}, f"Exported {exported_count} textures to {output_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "output_dir")
        layout.prop(self, "format")
        layout.prop(self, "include_flattened")


class BDS_OT_quick_fabric_assign(bpy.types.Operator):
    """Quickly assign fabric properties to the active garment"""
    bl_idname = "bds.quick_fabric_assign"
    bl_label = "Quick Fabric Assign"
    bl_options = {'REGISTER', 'UNDO'}

    fabric: EnumProperty(
        name="Fabric",
        items=[
            ('cotton', 'Cotton', 'Lightweight, breathable'),
            ('silk', 'Silk', 'Lightweight, flowing'),
            ('denim', 'Denim', 'Heavy, stiff'),
            ('leather', 'Leather', 'Thick, rigid'),
            ('chiffon', 'Chiffon', 'Ultra-light, transparent'),
            ('wool', 'Wool', 'Medium weight, warm'),
            ('polyester', 'Polyester', 'Synthetic, smooth'),
            ('linen', 'Linen', 'Natural, crisp'),
        ],
        default='cotton',
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        from ..core.fabric import FabricMaterial

        fabric = FabricMaterial(self.fabric)

        # Find or create cloth modifier
        cloth_mod = None
        for mod in obj.modifiers:
            if mod.type == 'CLOTH':
                cloth_mod = mod
                break

        if cloth_mod is None:
            cloth_mod = obj.modifiers.new("BDS_Cloth", 'CLOTH')

        fabric.apply_to_cloth_modifier(cloth_mod)
        self.report({'INFO'}, f"Applied {self.fabric} fabric properties")
        return {'FINISHED'}
