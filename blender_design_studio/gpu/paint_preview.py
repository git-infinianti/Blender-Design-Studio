"""Real-time paint stroke preview overlay."""

try:
    import bpy
    import gpu
    from gpu_extras.batch import batch_for_shader
    HAS_GPU = True
except ImportError:
    HAS_GPU = False


class PaintPreview:
    """Renders a preview of the current brush and stroke in the viewport."""

    def __init__(self):
        self._handle = None
        self._shader = None
        self._cursor_batch = None
        self._stroke_batch = None
        self._cursor_pos = (0, 0)
        self._cursor_radius = 50
        self._cursor_color = (1.0, 1.0, 1.0, 0.5)

    def enable(self) -> None:
        """Register the paint preview draw handler."""
        if not HAS_GPU or self._handle is not None:
            return
        self._shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self._draw_callback, (), 'WINDOW', 'POST_PIXEL'
        )

    def disable(self) -> None:
        """Remove the paint preview draw handler."""
        if not HAS_GPU or self._handle is None:
            return
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self._handle = None

    def update_cursor(self, x: int, y: int, radius: int = 50) -> None:
        """Update the brush cursor position and size."""
        if not HAS_GPU:
            return

        import math
        self._cursor_pos = (x, y)
        self._cursor_radius = radius

        segments = 32
        circle_verts = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            next_angle = 2 * math.pi * (i + 1) / segments
            circle_verts.append((
                x + radius * math.cos(angle),
                y + radius * math.sin(angle),
            ))
            circle_verts.append((
                x + radius * math.cos(next_angle),
                y + radius * math.sin(next_angle),
            ))

        self._cursor_batch = batch_for_shader(
            self._shader, 'LINES',
            {"pos": circle_verts}
        )

    def update_stroke_preview(self, points: list) -> None:
        """Update the in-progress stroke preview."""
        if not HAS_GPU or len(points) < 2:
            self._stroke_batch = None
            return

        line_verts = []
        for i in range(len(points) - 1):
            line_verts.append(points[i][:2])
            line_verts.append(points[i + 1][:2])

        self._stroke_batch = batch_for_shader(
            self._shader, 'LINES',
            {"pos": line_verts}
        )

    def _draw_callback(self) -> None:
        """GPU draw callback for paint preview."""
        if self._shader is None:
            return

        self._shader.bind()

        gpu.state.blend_set('ALPHA')

        if self._cursor_batch:
            self._shader.uniform_float("color", self._cursor_color)
            gpu.state.line_width_set(1.5)
            self._cursor_batch.draw(self._shader)

        if self._stroke_batch:
            self._shader.uniform_float("color", (0.8, 0.8, 1.0, 0.6))
            gpu.state.line_width_set(2.0)
            self._stroke_batch.draw(self._shader)

        gpu.state.blend_set('NONE')
        gpu.state.line_width_set(1.0)

    @property
    def is_active(self) -> bool:
        return self._handle is not None
