"""Procedural mask generator nodes for the smart material system."""

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


if HAS_BPY:
    class BDS_NT_EdgeWear(bpy.types.Node):
        """Generate edge wear mask from curvature data"""

        bl_idname = 'BDS_NT_EdgeWear'
        bl_label = 'Edge Wear'
        bl_icon = 'MOD_EDGESPLIT'

        def init(self, context):
            self.inputs.new('NodeSocketFloat', 'Amount').default_value = 0.5
            self.inputs.new('NodeSocketFloat', 'Contrast').default_value = 1.0
            self.inputs.new('NodeSocketColor', 'Curvature Input')
            self.outputs.new('NodeSocketColor', 'Wear Mask')

        def draw_buttons(self, context, layout):
            layout.label(text="Edge wear effect")


    class BDS_NT_ColorRamp(bpy.types.Node):
        """Remap values through a color ramp"""

        bl_idname = 'BDS_NT_ColorRamp'
        bl_label = 'BDS Color Ramp'
        bl_icon = 'COLOR'

        def init(self, context):
            self.inputs.new('NodeSocketColor', 'Input')
            self.outputs.new('NodeSocketColor', 'Output')

        def draw_buttons(self, context, layout):
            layout.label(text="Color remapping")

else:
    class BDS_NT_EdgeWear:
        bl_idname = 'BDS_NT_EdgeWear'


    class BDS_NT_ColorRamp:
        bl_idname = 'BDS_NT_ColorRamp'
