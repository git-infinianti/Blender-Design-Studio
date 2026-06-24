"""Texture baking pipeline for exporting PBR textures."""
from typing import List, Dict, Optional
import os

try:
    import bpy

    HAS_BPY = True
except ImportError:
    HAS_BPY = False


class BakeManager:
    """Orchestrates texture baking and export."""

    BAKE_TYPES = ['DIFFUSE', 'ROUGHNESS', 'NORMAL', 'AO', 'EMIT']

    def __init__(self, obj=None, resolution: int = 4096):
        self.obj = obj
        self.resolution = resolution

    def bake_from_highpoly(self, highpoly, cage_extrusion: float = 0.01) -> Dict[str, 'bpy.types.Image']:
        """Transfer detail from highpoly to lowpoly via Cycles bake."""
        if not HAS_BPY or self.obj is None:
            return {}

        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.render.bake.use_selected_to_active = True
        scene.render.bake.cage_extrusion = cage_extrusion

        results = {}
        mat = self._ensure_material()
        tree = mat.node_tree

        for bake_type in self.BAKE_TYPES:
            img_name = f"BDS_bake_{self.obj.name}_{bake_type.lower()}"
            img = bpy.data.images.new(img_name, self.resolution, self.resolution, alpha=True)

            tex_node = tree.nodes.new('ShaderNodeTexImage')
            tex_node.image = img
            tree.nodes.active = tex_node

            bpy.ops.object.select_all(action='DESELECT')
            highpoly.select_set(True)
            self.obj.select_set(True)
            bpy.context.view_layer.objects.active = self.obj

            try:
                bpy.ops.object.bake(type=bake_type)
                results[bake_type.lower()] = img
            except RuntimeError:
                pass

            tree.nodes.remove(tex_node)

        return results

    def bake_layer_stack(self, layer_stack) -> Dict[str, str]:
        """Flatten layer stack and save per-channel textures.

        Returns a dict mapping channel name to file path.
        """
        if not HAS_BPY:
            return {}

        paths = {}
        flat_images = layer_stack.flatten_all()

        for channel, img in flat_images.items():
            filepath = f"//textures/{self.obj.name}_{channel}.png"
            img.filepath_raw = filepath
            img.file_format = 'PNG'
            img.save()
            paths[channel] = filepath

        return paths

    def export_textures(
        self,
        output_dir: str,
        format: str = 'PNG',
        images: Optional[Dict[str, 'bpy.types.Image']] = None,
    ) -> List[str]:
        """Export all baked/painted textures to disk."""
        if not HAS_BPY:
            return []

        exported = []
        if images is None:
            images = {img.name: img for img in bpy.data.images if img.name.startswith("BDS_")}

        for name, img in images.items():
            filepath = os.path.join(output_dir, f"{name}.{format.lower()}")
            img.filepath_raw = filepath
            img.file_format = format
            img.save()
            exported.append(filepath)

        return exported

    def _ensure_material(self):
        """Ensure the object has a material with node tree."""
        if not self.obj.data.materials:
            mat = bpy.data.materials.new(f"BDS_{self.obj.name}")
            mat.use_nodes = True
            self.obj.data.materials.append(mat)
        return self.obj.data.materials[0]
