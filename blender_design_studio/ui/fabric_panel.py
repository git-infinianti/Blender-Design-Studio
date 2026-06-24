"""Fabric property inspector panel."""
import bpy


class BDS_PT_fabric_inspector(bpy.types.Panel):
    """Detailed fabric property inspector"""

    bl_label = "Fabric Properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BDS'
    bl_parent_id = "BDS_PT_simulation_panel"

    @classmethod
    def poll(cls, context):
        return context.scene.bds.mode == 'DRAPE'

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.bds
        preset = scene_props.sim_fabric_preset

        from ..core.fabric import FABRIC_PRESETS
        if preset in FABRIC_PRESETS:
            props = FABRIC_PRESETS[preset]
            layout.label(text=f"Mass: {props['mass']} kg/m²")
            layout.label(text=f"Stiffness: {props['stiffness']}")
            layout.label(text=f"Damping: {props['damping']}")
            layout.label(text=f"Bending: {props['bending']}")
