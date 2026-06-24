"""Main sidebar panels for Blender Design Studio."""
import bpy


class BDS_PT_main_panel(bpy.types.Panel):
    """Main panel with mode selector"""

    bl_label = "Blender Design Studio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        layout.prop(scene_props, "mode", expand=True)


class BDS_PT_pattern_panel(bpy.types.Panel):
    """Pattern drafting tools"""

    bl_label = "Pattern Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PATTERN'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        row = layout.row()
        row.template_list(
            "BDS_UL_pattern_list", "",
            scene_props, "pattern_pieces",
            scene_props, "active_piece_index",
        )

        col = row.column(align=True)
        col.operator("bds.create_pattern", icon='ADD', text="")

        layout.separator()

        layout.label(text="Tools:")
        col = layout.column(align=True)
        col.operator("bds.add_pattern_point", text="Add Point", icon='MESH_DATA')
        col.operator("bds.mirror_pattern", text="Mirror", icon='MOD_MIRROR')
        col.operator("bds.triangulate_pattern", text="Triangulate", icon='MOD_TRIANGULATE')

        layout.separator()

        layout.label(text="Import / Export:")
        col = layout.column(align=True)
        col.operator("bds.import_pattern", text="Import SVG/DXF", icon='IMPORT')
        col.operator("bds.export_pattern", text="Export SVG", icon='EXPORT')


class BDS_UL_pattern_list(bpy.types.UIList):
    """UIList for pattern pieces"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='MESH_PLANE')
            layout.prop(item, "fabric_preset", text="")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.name, icon='MESH_PLANE')


class BDS_PT_seam_panel(bpy.types.Panel):
    """Seam definition and stitching"""

    bl_label = "Seam Stitching"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PATTERN'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("bds.select_seam_edge", text="Select Seam Edge", icon='EDGESEL')
        col.operator("bds.stitch_seams", text="Stitch Seams", icon='MOD_MESHDEFORM')
        col.operator("bds.auto_seam", text="Auto Seam", icon='SNAP_MIDPOINT')
        col.operator("bds.remove_seam", text="Remove Seam", icon='X')


class BDS_PT_simulation_panel(bpy.types.Panel):
    """Cloth simulation controls"""

    bl_label = "Simulation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'DRAPE'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        layout.prop(scene_props, "sim_fabric_preset")

        # Show custom fabric properties when custom preset is selected
        if scene_props.sim_fabric_preset == 'custom':
            box = layout.box()
            box.label(text="Custom Fabric Properties:")
            col = box.column(align=True)
            col.prop(scene_props, "sim_custom_mass")
            col.prop(scene_props, "sim_custom_stiffness")
            col.prop(scene_props, "sim_custom_damping")
            col.prop(scene_props, "sim_custom_bending")

        layout.separator()

        col = layout.column(align=True)
        col.operator("bds.sim_setup", text="Setup Simulation", icon='MOD_CLOTH')

        row = layout.row(align=True)
        if scene_props.sim_is_running and not scene_props.sim_is_paused:
            row.enabled = False
        row.operator("bds.sim_start", text="Start", icon='PLAY')

        row = layout.row(align=True)
        if not scene_props.sim_is_running:
            row.enabled = False
        pause_text = "Resume" if scene_props.sim_is_paused else "Pause"
        pause_icon = 'PLAY' if scene_props.sim_is_paused else 'PAUSE'
        row.operator("bds.sim_pause", text=pause_text, icon=pause_icon)

        col = layout.column(align=True)
        col.operator("bds.sim_reset", text="Reset", icon='REW')
        col.operator("bds.sim_bake", text="Bake", icon='REC')
        col.operator("bds.apply_drape", text="Apply Drape", icon='CHECKMARK')


class BDS_PT_garment_tools_panel(bpy.types.Panel):
    """Garment creation tools and presets"""

    bl_label = "Garment Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'DRAPE'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Garment Presets:")
        col = layout.column(align=True)
        col.operator("bds.load_garment_preset", text="Load Garment Preset", icon='OUTLINER_OB_ARMATURE')
        col.operator("bds.quick_fabric_assign", text="Quick Fabric Assign", icon='MOD_CLOTH')

        layout.separator()

        layout.label(text="Pattern Pieces:")
        col = layout.column(align=True)
        col.operator("bds.create_pattern", text="Create Pattern Piece", icon='MESH_PLANE')
        col.operator("bds.import_pattern", text="Import SVG/DXF", icon='IMPORT')

        layout.separator()

        layout.label(text="Seam Tools:")
        col = layout.column(align=True)
        col.operator("bds.select_seam_edge", text="Select Seam Edge", icon='EDGESEL')
        col.operator("bds.stitch_seams", text="Stitch Seams", icon='MOD_MESHDEFORM')
        col.operator("bds.auto_seam", text="Auto Seam", icon='SNAP_MIDPOINT')


class BDS_PT_paint_panel(bpy.types.Panel):
    """Texture painting tools"""

    bl_label = "Paint Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        layout.prop(scene_props, "active_channel")

        layout.separator()

        col = layout.column(align=True)
        col.operator("bds.paint_stroke", text="Paint", icon='BRUSH_DATA')
        col.operator("bds.paint_fill", text="Fill", icon='COLOR')
        col.operator("bds.pick_color", text="Pick Color", icon='EYEDROPPER')


class BDS_PT_brush_settings(bpy.types.Panel):
    """Brush settings sub-panel"""

    bl_label = "Brush Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_paint_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        layout.prop(scene_props, "brush_preset")
        layout.separator()
        layout.prop(scene_props, "brush_radius")
        layout.prop(scene_props, "brush_strength")
        layout.prop(scene_props, "brush_color")
        layout.prop(scene_props, "brush_falloff")


class BDS_PT_layer_panel(bpy.types.Panel):
    """Layer stack panel"""

    bl_label = "Layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        row = layout.row()
        row.template_list(
            "BDS_UL_layer_list", "",
            scene_props, "paint_layers",
            scene_props, "active_layer_index",
        )

        col = row.column(align=True)
        col.operator("bds.layer_add", icon='ADD', text="")
        col.operator("bds.layer_remove", icon='REMOVE', text="")
        col.separator()
        col.operator("bds.layer_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("bds.layer_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        layout.separator()

        row = layout.row(align=True)
        row.operator("bds.layer_duplicate", text="Duplicate")
        row.operator("bds.layer_merge_down", text="Merge Down")
        layout.operator("bds.layer_flatten", text="Flatten All")


class BDS_UL_layer_list(bpy.types.UIList):
    """UIList for paint layers (Photoshop-style)"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(
                item,
                "visible",
                text="",
                icon='HIDE_OFF' if item.visible else 'HIDE_ON',
            )
            row.prop(item, "name", text="", emboss=False)
            row.prop(item, "opacity", text="", slider=True)
            row.prop(item, "blend_mode", text="")
            if item.locked:
                row.label(text="", icon='LOCKED')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.name)


class BDS_PT_smart_material_panel(bpy.types.Panel):
    """Smart material library panel"""

    bl_label = "Smart Materials"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj and hasattr(obj, 'bds_object'):
            layout.prop(obj.bds_object, "active_smart_material")

        layout.separator()
        layout.label(text="Available Materials:")
        col = layout.column(align=True)
        col.label(text="• Worn Metal", icon='MATERIAL')
        col.label(text="• Aged Wood", icon='MATERIAL')
        col.label(text="• Clean Plastic", icon='MATERIAL')
        col.label(text="• Fabric", icon='MATERIAL')
        col.label(text="• Brushed Steel", icon='MATERIAL')
        col.label(text="• Rusted Iron", icon='MATERIAL')
        col.label(text="• Polished Marble", icon='MATERIAL')
        col.label(text="• Worn Leather", icon='MATERIAL')
        col.label(text="• Concrete", icon='MATERIAL')
        col.label(text="• Ceramic Tile", icon='MATERIAL')
        col.label(text="• Carbon Fiber", icon='MATERIAL')
        col.label(text="• Velvet", icon='MATERIAL')
        col.label(text="• Hammered Copper", icon='MATERIAL')
        col.label(text="• Frosted Glass", icon='MATERIAL')
        col.label(text="• Raw Denim", icon='MATERIAL')
        col.label(text="• Patent Leather", icon='MATERIAL')


class BDS_PT_bake_panel(bpy.types.Panel):
    """Bake settings and export"""

    bl_label = "Bake & Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds

        layout.prop(scene_props, "bake_resolution")
        layout.prop(scene_props, "export_format")

        layout.separator()

        col = layout.column(align=True)
        col.operator("bds.bake_textures", text="Bake Textures", icon='RENDER_STILL')
        col.operator("bds.export_textures", text="Export Textures", icon='EXPORT')


class BDS_PT_udim_panel(bpy.types.Panel):
    """UDIM tile management"""

    bl_label = "UDIM Tiles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'PAINT'

    def draw(self, context):
        layout = self.layout
        layout.label(text="UDIM Tile Grid")
        layout.label(text="Tiles auto-assigned from pattern pieces")
