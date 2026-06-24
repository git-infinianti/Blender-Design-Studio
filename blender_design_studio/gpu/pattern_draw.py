"""GPU-accelerated 2D pattern overlay for the viewport."""

try:
    import bpy
    import gpu
    from gpu_extras.batch import batch_for_shader
    HAS_GPU = True
except ImportError:
    HAS_GPU = False


class PatternOverlay:
    """Renders pattern outlines and vertices as a 2D overlay in the viewport."""

    def __init__(self):
        self._handle = None
        self._batch_lines = None
        self._batch_points = None
        self._shader = None
        self._line_color = (1.0, 1.0, 1.0, 1.0)
        self._point_color = (1.0, 0.3, 0.3, 1.0)

    def enable(self) -> None:
        """Register the draw handler on SpaceView3D."""
        if not HAS_GPU or self._handle is not None:
            return
        self._shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self._draw_callback, (), 'WINDOW', 'POST_VIEW'
        )

    def disable(self) -> None:
        """Remove the draw handler."""
        if not HAS_GPU or self._handle is None:
            return
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._handle = None

    def update(self, vertices: list, edges: list,
               line_color=(1.0, 1.0, 1.0, 1.0),
               point_color=(1.0, 0.3, 0.3, 1.0)) -> None:
        """Update the overlay geometry."""
        if not HAS_GPU:
            return

        self._line_color = line_color
        self._point_color = point_color
        self._batch_lines = None
        self._batch_points = None

        if edges:
            line_verts = []
            for a, b in edges:
                if a < len(vertices) and b < len(vertices):
                    line_verts.append(vertices[a])
                    line_verts.append(vertices[b])
            if line_verts:
                self._batch_lines = batch_for_shader(
                    self._shader, 'LINES',
                    {"pos": line_verts}
                )

        if vertices:
            self._batch_points = batch_for_shader(
                self._shader, 'POINTS',
                {"pos": vertices}
            )

    def _draw_callback(self) -> None:
        """GPU draw callback."""
        if self._shader is None:
            return

        self._shader.bind()

        gpu.state.line_width_set(2.0)
        gpu.state.point_size_set(6.0)

        if self._batch_lines:
            self._shader.uniform_float("color", self._line_color)
            self._batch_lines.draw(self._shader)

        if self._batch_points:
            self._shader.uniform_float("color", self._point_color)
            self._batch_points.draw(self._shader)

        gpu.state.line_width_set(1.0)
        gpu.state.point_size_set(1.0)

    @property
    def is_active(self) -> bool:
        return self._handle is not None
