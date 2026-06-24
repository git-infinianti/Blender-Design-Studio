"""Cloth simulation wrapper and real-time stepping controller."""
try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False

from .fabric import FabricMaterial


class SimulationController:
    """Manages the cloth simulation lifecycle for a garment object."""

    def __init__(self, garment_obj=None):
        self.obj = garment_obj
        self._timer = None
        self._is_running: bool = False
        self._start_frame: int = 1

    def setup(self, fabric: FabricMaterial, avatar=None) -> None:
        """Add Cloth modifier to garment and Collision modifier to avatar."""
        if not HAS_BPY or self.obj is None:
            return

        cloth_mod = None
        for mod in self.obj.modifiers:
            if mod.type == 'CLOTH' and mod.name.startswith("BDS_"):
                cloth_mod = mod
                break

        if cloth_mod is None:
            cloth_mod = self.obj.modifiers.new("BDS_Cloth", 'CLOTH')

        fabric.apply_to_cloth_modifier(cloth_mod)

        if avatar is not None:
            has_collision = any(m.type == 'COLLISION' for m in avatar.modifiers)
            if not has_collision:
                avatar.modifiers.new("BDS_Collision", 'COLLISION')

        self._setup_pin_groups()

    def _setup_pin_groups(self) -> None:
        """Configure pin groups for seam constraints."""
        if not HAS_BPY or self.obj is None:
            return

        cloth_mod = self._get_cloth_modifier()
        if cloth_mod is None:
            return

        if "bds_seams" in self.obj.vertex_groups:
            cloth_mod.settings.vertex_group_mass = "bds_seams"

    def _get_cloth_modifier(self):
        """Get the BDS cloth modifier from the object."""
        if self.obj is None:
            return None
        for mod in self.obj.modifiers:
            if mod.type == 'CLOTH' and mod.name.startswith("BDS_"):
                return mod
        return None

    def step(self, context) -> None:
        """Advance sim by one frame."""
        if not HAS_BPY:
            return
        context.scene.frame_set(context.scene.frame_current + 1)

    def start_realtime(self, context) -> None:
        """Register a timer for interactive draping at ~30fps."""
        if not HAS_BPY or self._is_running:
            return
        self._start_frame = context.scene.frame_current
        self._timer = context.window_manager.event_timer_add(
            time_step=1.0 / 30.0,
            window=context.window,
        )
        self._is_running = True

    def stop_realtime(self, context) -> None:
        """Stop the real-time simulation timer."""
        if not HAS_BPY:
            return
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        self._is_running = False

    def reset(self, context) -> None:
        """Reset simulation to the start frame."""
        if not HAS_BPY:
            return
        self.stop_realtime(context)
        context.scene.frame_set(self._start_frame)

        cloth_mod = self._get_cloth_modifier()
        if cloth_mod is not None:
            cloth_mod.point_cache.frame_start = self._start_frame

    def bake(self, context, start: int = 1, end: int = 250) -> None:
        """Bake the cloth simulation to cache."""
        if not HAS_BPY or self.obj is None:
            return

        cloth_mod = self._get_cloth_modifier()
        if cloth_mod is None:
            return

        cloth_mod.point_cache.frame_start = start
        cloth_mod.point_cache.frame_end = end

        context.view_layer.objects.active = self.obj
        bpy.ops.ptcache.bake(bake=True)

    def apply_drape(self) -> None:
        """Apply the cloth modifier to finalize the mesh shape."""
        if not HAS_BPY or self.obj is None:
            return

        cloth_mod = self._get_cloth_modifier()
        if cloth_mod is not None:
            bpy.ops.object.modifier_apply(modifier=cloth_mod.name)

    @property
    def is_running(self) -> bool:
        return self._is_running
