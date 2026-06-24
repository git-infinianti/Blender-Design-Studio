bl_info = {
    "name": "Blender Design Studio",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tool Shelf",
    "description": "Cloth patterning + UDIM-aware painting workflows",
    "category": "Object",
}

import bpy
from bpy.props import PointerProperty

from .ops import (
    BDS_OT_create_pattern,
    BDS_OT_add_pattern_point,
    BDS_OT_move_pattern_point,
    BDS_OT_delete_pattern_element,
    BDS_OT_mirror_pattern,
    BDS_OT_triangulate_pattern,
    BDS_OT_import_pattern,
    BDS_OT_select_seam_edge,
    BDS_OT_stitch_seams,
    BDS_OT_auto_seam,
    BDS_OT_remove_seam,
    BDS_OT_sim_setup,
    BDS_OT_sim_start,
    BDS_OT_sim_pause,
    BDS_OT_sim_reset,
    BDS_OT_sim_bake,
    BDS_OT_apply_drape,
    BDS_OT_paint_stroke,
    BDS_OT_paint_fill,
    BDS_OT_paint_projection,
    BDS_OT_paint_clone,
    BDS_OT_pick_color,
    BDS_OT_layer_add,
    BDS_OT_layer_remove,
    BDS_OT_layer_move,
    BDS_OT_layer_duplicate,
    BDS_OT_layer_merge_down,
    BDS_OT_layer_flatten,
    BDS_OT_bake_textures,
    BDS_OT_export_textures,
    BDS_OT_export_pattern,
)
from .props import (
    BDS_SceneProps,
    BDS_PatternPieceProps,
    BDS_LayerProps,
    BDS_ObjectProps,
    BDS_Preferences,
)
from .ui.panels import (
    BDS_PT_main_panel,
    BDS_PT_pattern_panel,
    BDS_UL_pattern_list,
    BDS_PT_seam_panel,
    BDS_PT_simulation_panel,
    BDS_PT_paint_panel,
    BDS_PT_brush_settings,
    BDS_PT_layer_panel,
    BDS_UL_layer_list,
    BDS_PT_smart_material_panel,
    BDS_PT_bake_panel,
    BDS_PT_udim_panel,
)
from .ui.pattern_editor import BDS_OT_enter_pattern_mode
from .ui.layer_panel import BDS_MT_layer_context_menu
from .ui.fabric_panel import BDS_PT_fabric_inspector
from .ui.paint_toolbar import BDS_PT_paint_toolbar
from .ui.gizmos import BDS_GT_seam_handle, BDS_GGT_seam_handles
from .nodes.smart_material_tree import (
    BDS_SmartMaterialTree,
    BDS_NT_CurvatureMask,
    BDS_NT_AOMask,
    BDS_NT_PositionGradient,
)
from .nodes.mask_nodes import (
    BDS_NT_EdgeWear,
    BDS_NT_ColorRamp,
)

classes = (
    # Property groups (must be registered before classes that use them)
    BDS_PatternPieceProps,
    BDS_LayerProps,
    BDS_SceneProps,
    BDS_ObjectProps,
    BDS_Preferences,
    # Pattern operators
    BDS_OT_create_pattern,
    BDS_OT_add_pattern_point,
    BDS_OT_move_pattern_point,
    BDS_OT_delete_pattern_element,
    BDS_OT_mirror_pattern,
    BDS_OT_triangulate_pattern,
    BDS_OT_import_pattern,
    # Seam operators
    BDS_OT_select_seam_edge,
    BDS_OT_stitch_seams,
    BDS_OT_auto_seam,
    BDS_OT_remove_seam,
    # Simulation operators
    BDS_OT_sim_setup,
    BDS_OT_sim_start,
    BDS_OT_sim_pause,
    BDS_OT_sim_reset,
    BDS_OT_sim_bake,
    BDS_OT_apply_drape,
    # Paint operators
    BDS_OT_paint_stroke,
    BDS_OT_paint_fill,
    BDS_OT_paint_projection,
    BDS_OT_paint_clone,
    BDS_OT_pick_color,
    # Layer operators
    BDS_OT_layer_add,
    BDS_OT_layer_remove,
    BDS_OT_layer_move,
    BDS_OT_layer_duplicate,
    BDS_OT_layer_merge_down,
    BDS_OT_layer_flatten,
    # Bake operators
    BDS_OT_bake_textures,
    BDS_OT_export_textures,
    BDS_OT_export_pattern,
    # UI mode operator
    BDS_OT_enter_pattern_mode,
    # UI panels (parent panels before child panels)
    BDS_PT_main_panel,
    BDS_PT_pattern_panel,
    BDS_UL_pattern_list,
    BDS_PT_seam_panel,
    BDS_PT_simulation_panel,
    BDS_PT_fabric_inspector,
    BDS_PT_paint_panel,
    BDS_PT_brush_settings,
    BDS_PT_paint_toolbar,
    BDS_PT_layer_panel,
    BDS_UL_layer_list,
    BDS_PT_smart_material_panel,
    BDS_PT_bake_panel,
    BDS_PT_udim_panel,
    # Menus
    BDS_MT_layer_context_menu,
    # Node tree and nodes
    BDS_SmartMaterialTree,
    BDS_NT_CurvatureMask,
    BDS_NT_AOMask,
    BDS_NT_PositionGradient,
    BDS_NT_EdgeWear,
    BDS_NT_ColorRamp,
    # Gizmos
    BDS_GT_seam_handle,
    BDS_GGT_seam_handles,
)


addon_keymaps = []


def register_keymaps():
    """Register custom keybindings for BDS tools."""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        return

    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    # Paint mode keys
    kmi = km.keymap_items.new("bds.paint_stroke", 'B', 'PRESS')
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("bds.pick_color", 'E', 'PRESS')
    addon_keymaps.append((km, kmi))

    # Pattern mode keys
    kmi = km.keymap_items.new("bds.add_pattern_point", 'P', 'PRESS')
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("bds.select_seam_edge", 'S', 'PRESS',
                               shift=True)
    addon_keymaps.append((km, kmi))

    # Simulation keys
    kmi = km.keymap_items.new("bds.sim_start", 'SPACE', 'PRESS',
                               ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    """Remove custom keybindings."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bds = PointerProperty(type=BDS_SceneProps)
    bpy.types.Object.bds_object = PointerProperty(type=BDS_ObjectProps)
    register_keymaps()


def unregister():
    unregister_keymaps()
    if hasattr(bpy.types.Object, "bds_object"):
        del bpy.types.Object.bds_object
    if hasattr(bpy.types.Scene, "bds"):
        del bpy.types.Scene.bds
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
