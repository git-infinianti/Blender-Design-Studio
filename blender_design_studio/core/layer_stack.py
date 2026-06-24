"""PBR layer stack manager for texture painting."""
from typing import List, Dict, Optional

try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


BLEND_MODES = {
    'MIX': lambda a, b, t: a * (1 - t) + b * t,
    'MULTIPLY': lambda a, b, t: a * (1 - t) + (a * b) * t,
    'SCREEN': lambda a, b, t: a * (1 - t) + (1 - (1 - a) * (1 - b)) * t,
    'OVERLAY': (
        lambda a, b, t: a * (1 - t) + np.where(
            a < 0.5,
            2 * a * b,
            1 - 2 * (1 - a) * (1 - b),
        ) * t
        if HAS_NUMPY else a
    ),
    'ADD': lambda a, b, t: np.clip(a + b * t, 0, 1) if HAS_NUMPY else a,
}


class PaintLayer:
    """A single paint layer with per-channel images."""

    def __init__(self, name: str, resolution: int = 2048, blend_mode: str = 'MIX'):
        self.name = name
        self.resolution = resolution
        self.visible: bool = True
        self.opacity: float = 1.0
        self.blend_mode: str = blend_mode
        self.locked: bool = False
        self.mask: Optional['PaintLayer'] = None
        self.channels: Dict[str, 'bpy.types.Image'] = {}

    def ensure_channel(self, channel: str, resolution: int = 0, is_data: bool = False) -> None:
        """Create or get an image for a PBR channel."""
        if not HAS_BPY:
            return

        res = resolution or self.resolution
        key = f"BDS_{self.name}_{channel}"

        if key not in bpy.data.images:
            img = bpy.data.images.new(key, res, res, alpha=True, is_data=is_data)
            img.colorspace_settings.name = 'Non-Color' if is_data else 'sRGB'
        self.channels[channel] = bpy.data.images[key]

    def ensure_all_channels(self, channels: List[str]) -> None:
        """Ensure all PBR channels exist for this layer."""
        data_channels = {'metallic', 'roughness', 'normal', 'height'}
        for ch in channels:
            self.ensure_channel(ch, is_data=(ch in data_channels))

    def clear_channel(self, channel: str) -> None:
        """Fill a channel with transparent black."""
        if not HAS_BPY or not HAS_NUMPY:
            return
        if channel not in self.channels:
            return
        img = self.channels[channel]
        pixels = [0.0] * (img.size[0] * img.size[1] * 4)
        img.pixels[:] = pixels
        img.update()


class LayerStack:
    """Ordered stack of paint layers with compositing."""

    DEFAULT_CHANNELS = ["base_color", "metallic", "roughness", "normal", "height"]

    def __init__(self, obj=None):
        self.obj = obj
        self.layers: List[PaintLayer] = []
        self.active_index: int = 0
        self.channels = list(self.DEFAULT_CHANNELS)

    @property
    def active_layer(self) -> Optional[PaintLayer]:
        """Get the currently active layer."""
        if 0 <= self.active_index < len(self.layers):
            return self.layers[self.active_index]
        return None

    def add_layer(self, name: str, above: bool = True) -> PaintLayer:
        """Add a new layer to the stack."""
        layer = PaintLayer(name)
        layer.ensure_all_channels(self.channels)

        if above and self.layers:
            insert_idx = self.active_index + 1
            self.layers.insert(insert_idx, layer)
            self.active_index = insert_idx
        else:
            self.layers.append(layer)
            self.active_index = len(self.layers) - 1

        return layer

    def remove_layer(self, index: int) -> Optional[PaintLayer]:
        """Remove a layer at the given index."""
        if 0 <= index < len(self.layers):
            layer = self.layers.pop(index)
            if self.active_index >= len(self.layers):
                self.active_index = max(0, len(self.layers) - 1)
            return layer
        return None

    def move_layer(self, from_idx: int, to_idx: int) -> bool:
        """Move a layer from one position to another."""
        if 0 <= from_idx < len(self.layers) and 0 <= to_idx < len(self.layers):
            layer = self.layers.pop(from_idx)
            self.layers.insert(to_idx, layer)
            self.active_index = to_idx
            return True
        return False

    def duplicate_layer(self, index: int) -> Optional[PaintLayer]:
        """Duplicate a layer and insert it above."""
        if not (0 <= index < len(self.layers)):
            return None

        src = self.layers[index]
        dup = PaintLayer(
            name=f"{src.name}_copy",
            resolution=src.resolution,
            blend_mode=src.blend_mode,
        )
        dup.opacity = src.opacity
        dup.visible = src.visible

        if HAS_BPY and HAS_NUMPY:
            for ch, img in src.channels.items():
                dup.ensure_channel(ch, is_data=(ch != 'base_color'))
                if ch in dup.channels:
                    dup.channels[ch].pixels[:] = img.pixels[:]

        self.layers.insert(index + 1, dup)
        self.active_index = index + 1
        return dup

    def flatten(self, channel: str):
        """Composite all visible layers for one channel, bottom to top."""
        if not HAS_BPY or not HAS_NUMPY:
            return None

        visible = [l for l in self.layers if l.visible and channel in l.channels]
        if not visible:
            return None

        first_img = visible[0].channels[channel]
        width, height = first_img.size[0], first_img.size[1]
        result = np.array(first_img.pixels[:], dtype=np.float32).reshape((height, width, 4)).copy()
        result *= visible[0].opacity

        for layer in visible[1:]:
            img = layer.channels[channel]
            layer_pixels = np.array(img.pixels[:], dtype=np.float32).reshape((height, width, 4))

            blend_fn = BLEND_MODES.get(layer.blend_mode, BLEND_MODES['MIX'])
            t = layer.opacity
            result[:, :, :3] = blend_fn(result[:, :, :3], layer_pixels[:, :, :3], t)
            result[:, :, 3] = np.clip(result[:, :, 3] + layer_pixels[:, :, 3] * t, 0, 1)

        out_name = f"BDS_flat_{channel}"
        if out_name in bpy.data.images:
            out_img = bpy.data.images[out_name]
        else:
            out_img = bpy.data.images.new(out_name, width, height, alpha=True)

        out_img.pixels[:] = result.ravel().tolist()
        out_img.update()
        return out_img

    def flatten_all(self) -> Dict[str, 'bpy.types.Image']:
        """Flatten every channel, return dict of final images."""
        result = {}
        for channel in self.channels:
            img = self.flatten(channel)
            if img is not None:
                result[channel] = img
        return result

    def build_shader_tree(self) -> None:
        """Build/update Shader Editor node tree from current layer stack."""
        if not HAS_BPY or self.obj is None:
            return

        if not self.obj.data.materials:
            mat = bpy.data.materials.new(f"BDS_{self.obj.name}_Material")
            mat.use_nodes = True
            self.obj.data.materials.append(mat)

        mat = self.obj.data.materials[0]
        tree = mat.node_tree
        nodes = tree.nodes
        links = tree.links

        nodes.clear()

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (300, 0)

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        flat_images = self.flatten_all()

        channel_input_map = {
            'base_color': 'Base Color',
            'metallic': 'Metallic',
            'roughness': 'Roughness',
            'normal': 'Normal',
        }

        y_offset = 200
        for channel, input_name in channel_input_map.items():
            if channel in flat_images:
                tex_node = nodes.new('ShaderNodeTexImage')
                tex_node.image = flat_images[channel]
                tex_node.location = (0, y_offset)

                if channel == 'normal':
                    normal_map = nodes.new('ShaderNodeNormalMap')
                    normal_map.location = (150, y_offset)
                    links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
                    links.new(normal_map.outputs['Normal'], bsdf.inputs[input_name])
                else:
                    links.new(tex_node.outputs['Color'], bsdf.inputs[input_name])

                y_offset -= 300
