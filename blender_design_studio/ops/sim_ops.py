"""Simulation control operators for cloth draping."""
import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty


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

        from ..core.fabric import FabricMaterial, FABRIC_PRESETS
        from ..core.simulation import SimulationController

        if preset == 'custom':
            # Use custom fabric properties from scene
            fabric = FabricMaterial.__new__(FabricMaterial)
            fabric.preset_name = 'custom'
            fabric.mass = scene_props.sim_custom_mass
            fabric.structural_stiffness = scene_props.sim_custom_stiffness
            fabric.damping = scene_props.sim_custom_damping
            fabric.bending_stiffness = scene_props.sim_custom_bending
        else:
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
    _is_paused = False

    def modal(self, context, event):
        scene_props = context.scene.bds

        # Check if pause was requested
        if scene_props.sim_is_paused:
            if not self._is_paused:
                # Transition to paused state: remove timer
                self._is_paused = True
                if self._timer:
                    context.window_manager.event_timer_remove(self._timer)
                    self._timer = None
                context.area.header_text_set(
                    "Simulation Paused | ESC: Stop"
                )
            return {'PASS_THROUGH'}
        else:
            if self._is_paused:
                # Resume from paused state: re-add timer
                self._is_paused = False
                self._timer = context.window_manager.event_timer_add(
                    1.0 / 30.0, window=context.window
                )
                context.area.header_text_set(
                    "Simulation Running | ESC: Stop"
                )

        if event.type == 'TIMER':
            context.scene.frame_set(context.scene.frame_current + 1)
            context.area.tag_redraw()
        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            self.cancel(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        scene_props = context.scene.bds
        scene_props.sim_is_paused = False
        scene_props.sim_is_running = True

        context.area.header_text_set(
            "Simulation Running | ESC: Stop"
        )
        self._timer = context.window_manager.event_timer_add(
            1.0 / 30.0, window=context.window
        )
        context.window_manager.modal_handler_add(self)
        self._is_paused = False
        self.report({'INFO'}, "Simulation started")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        context.area.header_text_set(None)
        context.scene.bds.sim_is_running = False
        context.scene.bds.sim_is_paused = False
        self.report({'INFO'}, "Simulation stopped")


class BDS_OT_sim_pause(bpy.types.Operator):
    """Pause or resume the cloth simulation"""
    bl_idname = "bds.sim_pause"
    bl_label = "Pause Simulation"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene_props = context.scene.bds
        if not scene_props.sim_is_running:
            self.report({'WARNING'}, "No simulation is running")
            return {'CANCELLED'}

        scene_props.sim_is_paused = not scene_props.sim_is_paused
        if scene_props.sim_is_paused:
            self.report({'INFO'}, "Simulation paused")
        else:
            self.report({'INFO'}, "Simulation resumed")
        return {'FINISHED'}


class BDS_OT_sim_reset(bpy.types.Operator):
    """Reset simulation to the start frame"""
    bl_idname = "bds.sim_reset"
    bl_label = "Reset Simulation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.frame_set(1)
        context.scene.bds.sim_is_running = False
        context.scene.bds.sim_is_paused = False

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
