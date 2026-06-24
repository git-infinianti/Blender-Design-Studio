"""Custom node tree for smart material definitions."""

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False


if HAS_BPY:
    class BDS_SmartMaterialTree(bpy.types.NodeTree):
        """Custom node tree type for BDS Smart Materials"""

        bl_idname = 'BDSSmartMaterialTree'
        bl_label = 'BDS Smart Material'
        bl_icon = 'MATERIAL'


    class BDS_NT_CurvatureMask(bpy.types.Node):
        """Generate a mask based on mesh curvature"""

        bl_idname = 'BDS_NT_CurvatureMask'
        bl_label = 'Curvature Mask'
        bl_icon = 'MOD_SMOOTH'

        def init(self, context):
            self.inputs.new('NodeSocketFloat', 'Intensity').default_value = 1.0
            self.inputs.new('NodeSocketFloat', 'Radius').default_value = 0.1
            self.outputs.new('NodeSocketColor', 'Mask')

        def draw_buttons(self, context, layout):
            layout.label(text="Curvature-based mask")


    class BDS_NT_AOMask(bpy.types.Node):
        """Generate a mask based on ambient occlusion"""

        bl_idname = 'BDS_NT_AOMask'
        bl_label = 'Ambient Occlusion Mask'
        bl_icon = 'SHADING_RENDERED'

        def init(self, context):
            self.inputs.new('NodeSocketFloat', 'Intensity').default_value = 1.0
            self.inputs.new('NodeSocketFloat', 'Distance').default_value = 0.5
            self.outputs.new('NodeSocketColor', 'Mask')

        def draw_buttons(self, context, layout):
            layout.label(text="AO-based mask")


    class BDS_NT_PositionGradient(bpy.types.Node):
        """Generate a gradient mask based on world-space position"""

        bl_idname = 'BDS_NT_PositionGradient'
        bl_label = 'Position Gradient'
        bl_icon = 'ORIENTATION_GLOBAL'

        def init(self, context):
            self.inputs.new('NodeSocketFloat', 'Height Min').default_value = 0.0
            self.inputs.new('NodeSocketFloat', 'Height Max').default_value = 1.0
            self.outputs.new('NodeSocketColor', 'Mask')

        def draw_buttons(self, context, layout):
            layout.label(text="Position-based gradient")

else:
    class BDS_SmartMaterialTree:
        bl_idname = 'BDSSmartMaterialTree'


    class BDS_NT_CurvatureMask:
        bl_idname = 'BDS_NT_CurvatureMask'


    class BDS_NT_AOMask:
        bl_idname = 'BDS_NT_AOMask'


    class BDS_NT_PositionGradient:
        bl_idname = 'BDS_NT_PositionGradient'
