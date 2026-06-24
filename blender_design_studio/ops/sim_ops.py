"""Simulation control operators for cloth draping."""
import bpy
from bpy.props import EnumProperty, IntProperty


class BDS_OT_sim_setup(bpy.types.Operator):
    """Configure cloth simulation on the active garment"""
    bl_idname = "bds.sim_setup"
    bl_label = "Setup Simulation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        scene_props = context.scene.bds
        preset = scene_props.sim_fabric_preset

        from ..core.fabric import FabricMaterial
        from ..core.simulation import SimulationController

        fabric = FabricMaterial(preset)
        sim = SimulationController(obj)

        avatar = None
        for other_obj in context.scene.objects:
            if other_obj.type == 'MESH' and other_obj != obj:
                obj_props = other_obj.bds_object
                if obj_props.is_avatar:
                    avatar = other_obj
                    break

        sim.setup(fabric, avatar)
        self.report({'INFO'}, f"Simulation setup with {preset} fabric")
        return {'FINISHED'}


class BDS_OT_sim_start(bpy.types.Operator):
    """Start real-time cloth simulation"""
    bl_idname = "bds.sim_start"
    bl_label = "Start Simulation"
    bl_options = {'REGISTER'}

    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            context.scene.frame_set(context.scene.frame_current + 1)
            context.area.tag_redraw()
        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            self.cancel(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.workspace.status_text_set(
            "Simulation Running | ESC: Stop"
        )
        self._timer = context.window_manager.event_timer_add(
            1.0 / 30.0, window=context.window
        )
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Simulation started")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        context.workspace.status_text_set(None)
        self.report({'INFO'}, "Simulation stopped")


class BDS_OT_sim_pause(bpy.types.Operator):
    """Pause the cloth simulation"""
    bl_idname = "bds.sim_pause"
    bl_label = "Pause Simulation"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.report({'INFO'}, "Simulation paused")
        return {'FINISHED'}


class BDS_OT_sim_reset(bpy.types.Operator):
    """Reset simulation to the start frame"""
    bl_idname = "bds.sim_reset"
    bl_label = "Reset Simulation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.frame_set(1)

        obj = context.active_object
        if obj is not None and obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'CLOTH':
                    mod.point_cache.frame_start = 1

        self.report({'INFO'}, "Simulation reset")
        return {'FINISHED'}


class BDS_OT_sim_bake(bpy.types.Operator):
    """Bake cloth simulation to cache"""
    bl_idname = "bds.sim_bake"
    bl_label = "Bake Simulation"
    bl_options = {'REGISTER'}

    frame_end: IntProperty(name="End Frame", default=250, min=1)

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        cloth_mod = None
        for mod in obj.modifiers:
            if mod.type == 'CLOTH':
                cloth_mod = mod
                break

        if cloth_mod is None:
            self.report({'WARNING'}, "No cloth modifier found")
            return {'CANCELLED'}

        cloth_mod.point_cache.frame_end = self.frame_end
        context.view_layer.objects.active = obj

        try:
            bpy.ops.ptcache.bake(bake=True)
            self.report({'INFO'}, "Simulation baked")
        except RuntimeError as e:
            self.report({'ERROR'}, f"Bake failed: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}


class BDS_OT_apply_drape(bpy.types.Operator):
    """Apply cloth modifier to finalize the draped mesh"""
    bl_idname = "bds.apply_drape"
    bl_label = "Apply Drape"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Select a mesh object")
            return {'CANCELLED'}

        for mod in obj.modifiers:
            if mod.type == 'CLOTH' and mod.name.startswith("BDS_"):
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                    self.report({'INFO'}, "Drape applied")
                    return {'FINISHED'}
                except RuntimeError as e:
                    self.report({'ERROR'}, f"Apply failed: {e}")
                    return {'CANCELLED'}

        self.report({'WARNING'}, "No BDS cloth modifier found")
        return {'CANCELLED'}
