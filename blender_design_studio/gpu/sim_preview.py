"""Cloth simulation wireframe overlay for visualization."""

try:
    import bpy
    import gpu
    from gpu_extras.batch import batch_for_shader
    HAS_GPU = True
except ImportError:
    HAS_GPU = False


class SimPreview:
    """Renders simulation-related overlays (stress visualization, pin points)."""

    def __init__(self):
        self._handle = None
        self._shader = None
        self._pin_batch = None
        self._stress_batch = None

    def enable(self) -> None:
        """Register the simulation preview draw handler."""
        if not HAS_GPU or self._handle is not None:
            return
        self._shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self._draw_callback, (), 'WINDOW', 'POST_VIEW'
        )

    def disable(self) -> None:
        """Remove the simulation preview draw handler."""
        if not HAS_GPU or self._handle is None:
            return
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._handle = None

    def update_pin_points(self, positions: list) -> None:
        """Update the display of pinned vertex positions."""
        if not HAS_GPU or not positions:
            self._pin_batch = None
            return

        self._pin_batch = batch_for_shader(
            self._shader, 'POINTS',
            {"pos": positions}
        )

    def _draw_callback(self) -> None:
        """GPU draw callback for simulation overlay."""
        if self._shader is None:
            return

        self._shader.bind()

        if self._pin_batch:
            gpu.state.point_size_set(8.0)
            self._shader.uniform_float("color", (0.2, 0.8, 0.2, 1.0))
            self._pin_batch.draw(self._shader)
            gpu.state.point_size_set(1.0)

    @property
    def is_active(self) -> bool:
        return self._handle is not None
