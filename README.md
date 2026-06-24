# Blender Design Studio — Implementation Plan

> A comprehensive Blender addon replicating the core functionality of **Marvelous Designer Pro** (3D clothing/fabric design) and **Substance Painter** (3D texture painting) within Blender's native environment.

---

## 1. Feature Overview

Blender Design Studio (BDS) bridges two major creative pipelines into a single Blender addon:

| Domain | Original Software | Key Capabilities |
|---|---|---|
| **Garment Design** | Marvelous Designer Pro | 2D pattern drafting, seam stitching, real-time cloth simulation, garment draping onto avatars, fabric property editing |
| **Texture Painting** | Substance Painter | Layer-based PBR painting, UDIM-aware workflows, smart materials, procedural masks, texture baking, material channel painting |

The addon already has a minimal scaffold (`blender_design_studio/`) with a `PatternPiece` data model, a placeholder operator, and a single UI panel. This plan expands that into a production-grade tool.

---

## 2. Technical Approach

### High-Level Architecture

```
blender_design_studio/
├── __init__.py                  # Addon registration, bl_info, preferences
├── core/
│   ├── __init__.py
│   ├── pattern.py               # 2D pattern geometry model (exists, expand)
│   ├── garment.py               # Garment assembly (pieces + seams → 3D mesh)
│   ├── simulation.py            # Cloth sim wrapper & real-time stepping
│   ├── fabric.py                # Fabric material properties database
│   ├── seam.py                  # Seam/stitch definitions + constraints
│   ├── paint_engine.py          # Core texture paint engine (brush, stroke)
│   ├── layer_stack.py           # PBR layer stack manager
│   ├── bake.py                  # Texture baking pipeline
│   ├── udim.py                  # UDIM tile management
│   └── smart_material.py        # Procedural smart material system
├── ops/
│   ├── __init__.py
│   ├── pattern_ops.py           # Pattern CRUD operators (exists, expand)
│   ├── seam_ops.py              # Seam stitching operators
│   ├── sim_ops.py               # Simulation control operators
│   ├── paint_ops.py             # Paint stroke, fill, projection operators
│   ├── layer_ops.py             # Layer add/remove/reorder operators
│   ├── bake_ops.py              # Baking operators
│   └── import_export_ops.py     # DXF/SVG pattern import, texture export
├── ui/
│   ├── __init__.py
│   ├── panels.py                # Main sidebar panels (exists, expand)
│   ├── pattern_editor.py        # 2D pattern editor (custom SpaceView)
│   ├── layer_panel.py           # Layer stack UI (Substance-style)
│   ├── fabric_panel.py          # Fabric property inspector
│   ├── paint_toolbar.py         # Brush/tool bar for painting
│   └── gizmos.py                # Custom gizmos (seam handles, pattern grips)
├── gpu/
│   ├── __init__.py
│   ├── pattern_draw.py          # GPU-accelerated 2D pattern overlay
│   ├── paint_preview.py         # Real-time paint stroke preview
│   └── sim_preview.py           # Cloth sim wireframe overlay
├── nodes/
│   ├── __init__.py
│   ├── smart_material_tree.py   # Custom node tree for smart materials
│   └── mask_nodes.py            # Procedural mask generator nodes
├── props/
│   ├── __init__.py
│   ├── scene_props.py           # Scene-level addon properties
│   ├── object_props.py          # Per-object garment/paint data
│   └── preferences.py           # Addon preferences
└── utils/
    ├── __init__.py
    ├── math_utils.py            # Geometry helpers, Delaunay, convex hull
    ├── mesh_utils.py            # bmesh helpers, UV utilities
    └── texture_utils.py         # Image buffer manipulation
```

### Strategy Summary

1. **Garment pipeline**: 2D pattern → triangulated mesh → seam constraint graph → Blender Cloth modifier (or custom solver) → draped 3D garment.
2. **Paint pipeline**: Layer stack stored as scene data → GPU shader composites layers in real-time → on-mesh stroke painting writes to the active layer's image buffer → final flatten/export.
3. Both pipelines share the mesh object; a garment can be painted in place.

---

## 3. Blender APIs and Systems

### Core APIs

| API / Module | Purpose |
|---|---|
| `bpy.types.Operator` | All tool operations (pattern creation, simulation, painting) |
| `bpy.types.Panel`, `bpy.types.UIList` | Sidebar panels, layer list UI |
| `bpy.types.PropertyGroup` | Per-object and per-scene addon data |
| `bpy.types.Gizmo`, `bpy.types.GizmoGroup` | Seam handles, pattern control points |
| `bmesh` | Procedural mesh construction, pattern triangulation, seam merging |
| `bpy.types.ClothModifier` / `bpy.types.ClothSettings` | Native cloth simulation parameters |
| `bpy.ops.object.modifier_add(type='CLOTH')` | Adding/configuring cloth sim |
| `gpu` module (`gpu.shader`, `gpu.types.GPUBatch`) | Custom viewport overlays for patterns, paint preview |
| `bpy.types.SpaceView3D.draw_handler_add` | Registering custom draw callbacks |
| `bpy.types.Image`, `bpy.data.images` | Texture/image buffer management for painting |
| `bpy.types.ShaderNodeTree` / `bpy.types.NodeTree` | Smart material node graphs |
| `bpy.types.Timer` | Real-time simulation stepping |
| `bpy.app.handlers` | Frame-change handlers for sim playback |
| `bpy.types.Mesh.uv_layers` | UV map access for UDIM workflows |
| `bpy.ops.image.save_as` | Exporting painted textures |
| `mathutils` (`Vector`, `Matrix`, `geometry`) | All geometric computations |
| `bpy.types.KeyMap`, `bpy.types.KeyMapItem` | Custom keybindings for tools |

### External Dependencies (bundled or pip-installed)

| Library | Purpose |
|---|---|
| `triangle` (Jonathan Shewchuk) | Constrained Delaunay triangulation of 2D patterns |
| `scipy.spatial` (optional) | Voronoi, KD-tree for nearest-point queries |
| `numpy` | Fast array math for simulation, image buffers |
| `Pillow` (PIL) | Image compositing fallback, format conversion |

---

## 4. Implementation Steps

### Phase 1 — Pattern Drafting & 2D Editor (Weeks 1–3)

#### Step 1.1: Expand `PatternPiece` Data Model

Extend the existing `core/pattern.py`:

```python
@dataclass
class PatternPiece:
    name: str
    verts: List[Vector]           # 2D control points
    edges: List[Tuple[int, int]]  # boundary edges
    internal_lines: List[Tuple[int, int]]  # dart lines, grain lines
    seam_allowance: float = 0.01  # meters
    fabric_id: str = "default"
    uv_island_index: int = -1     # maps to a UDIM tile

    def triangulate(self) -> Tuple[List[Vector], List[Tuple[int,int,int]]]:
        """Constrained Delaunay triangulation via `triangle` library."""
        ...

    def offset_boundary(self, distance: float) -> 'PatternPiece':
        """Generate seam-allowance offset curve."""
        ...
```

#### Step 1.2: 2D Pattern Editor Overlay

Create `gpu/pattern_draw.py`:

- Register a `draw_handler` on `SpaceView3D` (POST_PIXEL) for an orthographic 2D overlay.
- Render pattern outlines, vertices, seam-allowance dashes using `gpu.shader.from_builtin('POLYLINE_SMOOTH_COLOR')`.
- Implement hit-testing for vertex/edge selection in screen space.

Create `ui/pattern_editor.py`:

- A togglable "Pattern Mode" that switches the 3D viewport to a top-down orthographic view locked to Z-up.
- Tool shelf shows pattern-specific tools: Add Point, Move Point, Add Edge, Split Edge, Mirror, Import SVG/DXF.

#### Step 1.3: Pattern Drawing Operators

Expand `ops/pattern_ops.py`:

| Operator | `bl_idname` | Description |
|---|---|---|
| `BDS_OT_create_pattern` | `bds.create_pattern` | Create empty pattern piece (exists, refine) |
| `BDS_OT_add_pattern_point` | `bds.add_pattern_point` | Add vertex at mouse position (modal) |
| `BDS_OT_move_pattern_point` | `bds.move_pattern_point` | Translate selected vertices |
| `BDS_OT_delete_pattern_element` | `bds.delete_pattern_element` | Remove selected verts/edges |
| `BDS_OT_mirror_pattern` | `bds.mirror_pattern` | Mirror piece across axis |
| `BDS_OT_import_pattern` | `bds.import_pattern` | Import DXF/SVG as pattern outline |
| `BDS_OT_triangulate_pattern` | `bds.triangulate_pattern` | Convert 2D outline → mesh via Delaunay |

Each modal operator uses `context.window_manager.modal_handler_add(self)` and processes `MOUSEMOVE`, `LEFTMOUSE`, `RIGHTMOUSE`, `ESC` events.

#### Step 1.4: Pattern Import (DXF/SVG)

In `ops/import_export_ops.py`:

- Parse SVG `<path>` elements into vertex/edge lists using Python's `xml.etree.ElementTree`.
- Parse DXF using a lightweight reader (entities: `LINE`, `LWPOLYLINE`, `SPLINE`).
- Map parsed geometry into `PatternPiece` instances.

---

### Phase 2 — Seam Stitching & Garment Assembly (Weeks 4–5)

#### Step 2.1: Seam Data Model

Create `core/seam.py`:

```python
@dataclass
class SeamSegment:
    piece_a: str          # PatternPiece name
    edge_indices_a: List[int]  # edge indices on piece A
    piece_b: str
    edge_indices_b: List[int]
    stitch_type: str = "normal"  # normal | zipper | gather
    strength: float = 1.0

@dataclass
class SeamCollection:
    seams: List[SeamSegment] = field(default_factory=list)

    def add_seam(self, piece_a, edges_a, piece_b, edges_b, **kwargs):
        ...

    def build_constraint_pairs(self) -> List[Tuple[int, int]]:
        """Return global vertex-index pairs that must be merged."""
        ...
```

#### Step 2.2: Seam Stitching Operators

`ops/seam_ops.py`:

| Operator | Description |
|---|---|
| `BDS_OT_select_seam_edge` | Click edges on two pieces to define a seam pair |
| `BDS_OT_stitch_seams` | Merge seam-paired vertices into a single mesh |
| `BDS_OT_auto_seam` | Auto-match edges by proximity + length heuristic |
| `BDS_OT_remove_seam` | Unlink a seam pair |

#### Step 2.3: Garment Assembly

Create `core/garment.py`:

```python
class Garment:
    def __init__(self, pattern_collection: PatternCollection, seams: SeamCollection):
        self.patterns = pattern_collection
        self.seams = seams

    def assemble_flat(self) -> bpy.types.Object:
        """Place all triangulated pieces as a single mesh, flat on XY plane."""
        ...

    def wrap_around_avatar(self, avatar_obj: bpy.types.Object) -> None:
        """Position pattern pieces roughly around avatar using bounding box heuristics."""
        ...

    def apply_seam_constraints(self, obj: bpy.types.Object) -> None:
        """Add vertex groups + Cloth modifier pin groups for seam merging."""
        ...
```

---

### Phase 3 — Cloth Simulation (Weeks 6–8)

#### Step 3.1: Fabric Material Properties

Create `core/fabric.py`:

```python
FABRIC_PRESETS = {
    "cotton": {"mass": 0.15, "stiffness": 15.0, "damping": 5.0, "bending": 0.5},
    "silk":   {"mass": 0.06, "stiffness": 5.0,  "damping": 2.0, "bending": 0.1},
    "denim":  {"mass": 0.35, "stiffness": 40.0, "damping": 10.0, "bending": 5.0},
    "leather":{"mass": 0.50, "stiffness": 80.0, "damping": 15.0, "bending": 10.0},
}

class FabricMaterial:
    def __init__(self, preset: str = "cotton"):
        props = FABRIC_PRESETS[preset]
        self.mass = props["mass"]           # kg/m²
        self.structural_stiffness = props["stiffness"]
        self.damping = props["damping"]
        self.bending_stiffness = props["bending"]

    def apply_to_cloth_modifier(self, cloth_mod: bpy.types.ClothModifier):
        settings = cloth_mod.settings
        settings.mass = self.mass
        settings.tension_stiffness = self.structural_stiffness
        settings.compression_stiffness = self.structural_stiffness
        settings.bending_stiffness = self.bending_stiffness
        settings.tension_damping = self.damping
        settings.compression_damping = self.damping
```

#### Step 3.2: Simulation Controller

Create `core/simulation.py`:

```python
class SimulationController:
    def __init__(self, garment_obj: bpy.types.Object):
        self.obj = garment_obj
        self._timer = None

    def setup(self, fabric: FabricMaterial, avatar: bpy.types.Object):
        # Add Cloth modifier
        mod = self.obj.modifiers.new("BDS_Cloth", 'CLOTH')
        fabric.apply_to_cloth_modifier(mod)

        # Add Collision modifier to avatar
        if not any(m.type == 'COLLISION' for m in avatar.modifiers):
            avatar.modifiers.new("BDS_Collision", 'COLLISION')

        # Pin seam vertices
        self._setup_pin_groups()

    def step(self, context):
        """Advance sim by one frame (called by timer or frame_change handler)."""
        context.scene.frame_set(context.scene.frame_current + 1)

    def start_realtime(self, context):
        """Register a timer for interactive draping."""
        self._timer = context.window_manager.event_timer_add(
            time_step=1/30, window=context.window
        )

    def stop_realtime(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
```

#### Step 3.3: Simulation Operators

`ops/sim_ops.py`:

| Operator | Description |
|---|---|
| `BDS_OT_sim_setup` | Configure cloth + collision modifiers |
| `BDS_OT_sim_start` | Begin real-time draping (modal timer) |
| `BDS_OT_sim_pause` | Pause simulation |
| `BDS_OT_sim_reset` | Reset to rest pose |
| `BDS_OT_sim_bake` | Bake simulation to cache |
| `BDS_OT_apply_drape` | Apply modifier, finalize mesh |

---

### Phase 4 — Texture Paint Engine (Weeks 9–12)

#### Step 4.1: Layer Stack System

Create `core/layer_stack.py`:

```python
class PaintLayer:
    def __init__(self, name: str, resolution: int = 2048, blend_mode: str = 'MIX'):
        self.name = name
        self.visible = True
        self.opacity = 1.0
        self.blend_mode = blend_mode  # MIX, MULTIPLY, OVERLAY, SCREEN, etc.
        self.locked = False
        self.mask: Optional['PaintLayer'] = None
        # Each layer stores per-channel images
        self.channels: Dict[str, bpy.types.Image] = {}

    def ensure_channel(self, channel: str, resolution: int, is_data: bool = False):
        """Create or get an image for a PBR channel (base_color, metallic, roughness, normal, height)."""
        key = f"BDS_{self.name}_{channel}"
        if key not in bpy.data.images:
            img = bpy.data.images.new(key, resolution, resolution, alpha=True, is_data=is_data)
            img.colorspace_settings.name = 'Non-Color' if is_data else 'sRGB'
        self.channels[channel] = bpy.data.images[key]


class LayerStack:
    def __init__(self, obj: bpy.types.Object):
        self.obj = obj
        self.layers: List[PaintLayer] = []
        self.active_index: int = 0
        self.channels = ["base_color", "metallic", "roughness", "normal", "height"]

    def add_layer(self, name: str, above: bool = True) -> PaintLayer:
        ...

    def remove_layer(self, index: int):
        ...

    def move_layer(self, from_idx: int, to_idx: int):
        ...

    def flatten(self, channel: str) -> bpy.types.Image:
        """Composite all visible layers for one channel top-to-bottom."""
        ...

    def flatten_all(self) -> Dict[str, bpy.types.Image]:
        """Flatten every channel, return dict of final images."""
        ...

    def build_shader_tree(self):
        """Build/update Shader Editor node tree from current layer stack."""
        ...
```

#### Step 4.2: Brush & Stroke Engine

Create `core/paint_engine.py`:

```python
class BrushSettings:
    def __init__(self):
        self.radius: int = 50          # pixels
        self.strength: float = 1.0
        self.falloff: str = 'SMOOTH'   # SMOOTH, SHARP, LINEAR, CONSTANT
        self.color: Tuple[float,float,float] = (1.0, 1.0, 1.0)
        self.texture: Optional[bpy.types.Image] = None  # stamp texture
        self.spacing: float = 0.1      # fraction of radius
        self.channel: str = "base_color"

class PaintStroke:
    """Records a single continuous stroke for undo/redo."""
    def __init__(self, layer: PaintLayer, brush: BrushSettings):
        self.layer = layer
        self.brush = brush
        self.points: List[Tuple[float, float, float]] = []  # UV coords + pressure

    def apply(self):
        """Write brush stamps along self.points into layer's image buffer."""
        img = self.layer.channels[self.brush.channel]
        pixels = numpy.array(img.pixels[:]).reshape((img.size[1], img.size[0], 4))
        for u, v, pressure in self.points:
            self._stamp(pixels, u, v, pressure)
        img.pixels[:] = pixels.ravel().tolist()

    def _stamp(self, pixels, u, v, pressure):
        """Blend a single brush footprint into the pixel array."""
        ...
```

#### Step 4.3: Paint Operators

`ops/paint_ops.py`:

| Operator | Description |
|---|---|
| `BDS_OT_paint_stroke` | Modal: capture mouse → raycast → UV hit → stamp to active layer |
| `BDS_OT_paint_fill` | Fill selection / UV island with solid color |
| `BDS_OT_paint_projection` | Project an image onto mesh surface |
| `BDS_OT_paint_clone` | Clone stamp from reference point |
| `BDS_OT_pick_color` | Eyedropper: sample color from surface |

The paint stroke operator flow:

1. `invoke()` → start modal, enable draw callback.
2. `modal()` → on `MOUSEMOVE` + `LEFTMOUSE` pressed:
   - `context.region.view2d` or 3D `view3d_utils.region_2d_to_origin_3d` → ray.
   - `obj.ray_cast(origin, direction)` → hit location + face index.
   - `mesh.uv_layers.active` → interpolate UV from barycentric coords.
   - Stamp brush at UV coordinate into active layer image.
   - Tag `gpu` redraw for preview.
3. `cancel()` / `RIGHTMOUSE` → undo stroke.

#### Step 4.4: Real-Time Paint Preview (GPU)

Create `gpu/paint_preview.py`:

- Use a custom GLSL fragment shader to composite the layer stack on the fly.
- Bind each layer's image as a texture uniform.
- Blend in the shader according to `blend_mode` and `opacity`.
- Draw result onto the mesh surface using `gpu.types.GPUBatch` from the mesh's triangulated geometry + UVs.
- Update only the dirty region (bounding box of the latest stroke segment) each frame.

---

### Phase 5 — UDIM Support (Weeks 13–14)

#### Step 5.1: UDIM Tile Manager

Create `core/udim.py`:

```python
class UDIMTileSet:
    def __init__(self, base_name: str, resolution: int = 2048):
        self.base_name = base_name
        self.resolution = resolution
        self.tiles: Dict[int, bpy.types.Image] = {}  # key = UDIM number (1001, 1002, ...)

    def add_tile(self, u_index: int, v_index: int) -> bpy.types.Image:
        udim_number = 1001 + u_index + v_index * 10
        name = f"{self.base_name}.{udim_number}"
        img = bpy.data.images.new(name, self.resolution, self.resolution, alpha=True)
        img.source = 'TILED'
        self.tiles[udim_number] = img
        return img

    def get_tile_for_uv(self, u: float, v: float) -> Optional[bpy.types.Image]:
        u_idx = int(u)
        v_idx = int(v)
        udim = 1001 + u_idx + v_idx * 10
        return self.tiles.get(udim)
```

#### Step 5.2: UDIM-Aware Painting

- Modify `PaintStroke.apply()` to resolve which UDIM tile a UV coordinate falls into.
- Normalize UV within tile: `local_u = u - int(u)`, `local_v = v - int(v)`.
- Stamp into the correct tile image.
- Support painting across tile boundaries by splitting the brush footprint.

---

### Phase 6 — Smart Materials & Procedural Masks (Weeks 15–17)

#### Step 6.1: Custom Node Tree

Create `nodes/smart_material_tree.py`:

```python
class BDS_SmartMaterialTree(bpy.types.NodeTree):
    bl_idname = 'BDSSmartMaterialTree'
    bl_label = 'BDS Smart Material'
    bl_icon = 'MATERIAL'

class BDS_NT_CurvatureMask(bpy.types.Node):
    bl_idname = 'BDS_NT_CurvatureMask'
    bl_label = 'Curvature Mask'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Intensity')
        self.inputs.new('NodeSocketFloat', 'Radius')
        self.outputs.new('NodeSocketColor', 'Mask')

    def execute(self, mesh: bpy.types.Mesh) -> numpy.ndarray:
        """Compute per-vertex curvature, bake to texture."""
        ...

class BDS_NT_AOMask(bpy.types.Node):
    bl_idname = 'BDS_NT_AOMask'
    bl_label = 'Ambient Occlusion Mask'
    ...

class BDS_NT_PositionGradient(bpy.types.Node):
    bl_idname = 'BDS_NT_PositionGradient'
    bl_label = 'Position Gradient'
    ...
```

#### Step 6.2: Smart Material Application

A smart material is a pre-built node graph that, when applied:

1. Bakes mesh data maps (curvature, AO, world-space normal, position) using `bpy.ops.object.bake(type='...')` or custom compute.
2. Feeds those maps through the node graph to produce procedural masks.
3. Generates layer stack entries with the computed masks automatically applied.

---

### Phase 7 — Texture Baking Pipeline (Week 18)

Create `core/bake.py`:

```python
class BakeManager:
    BAKE_TYPES = ['DIFFUSE', 'ROUGHNESS', 'NORMAL', 'AO', 'EMIT']

    def __init__(self, obj: bpy.types.Object, resolution: int = 4096):
        self.obj = obj
        self.resolution = resolution

    def bake_from_highpoly(self, highpoly: bpy.types.Object, cage_extrusion: float = 0.01):
        """Transfer detail from highpoly via Cycles bake."""
        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.render.bake.use_selected_to_active = True
        scene.render.bake.cage_extrusion = cage_extrusion
        # ... set up image nodes, bake each type

    def bake_layer_stack(self, layer_stack: LayerStack):
        """Flatten layer stack and export per-channel textures."""
        for channel in layer_stack.channels:
            img = layer_stack.flatten(channel)
            img.filepath_raw = f"//textures/{self.obj.name}_{channel}.png"
            img.save()

    def export_textures(self, output_dir: str, format: str = 'PNG'):
        """Export all baked textures to disk."""
        ...
```

---

### Phase 8 — UI/UX Polish & Integration (Weeks 19–20)

#### Panels & Layout

Expand `ui/panels.py` into a multi-tab interface:

```
BDS sidebar (bl_category = 'BDS')
├── BDS_PT_main_panel              — Mode selector (Pattern / Drape / Paint)
├── BDS_PT_pattern_panel           — Pattern tools, piece list, import
│   └── BDS_UL_pattern_list        — UIList of pattern pieces
├── BDS_PT_seam_panel              — Seam definition, auto-stitch
├── BDS_PT_simulation_panel        — Fabric presets, sim controls
├── BDS_PT_paint_panel             — Brush settings, channel selector
│   └── BDS_PT_brush_settings      — Sub-panel: radius, strength, falloff
├── BDS_PT_layer_panel             — Layer stack with UIList
│   └── BDS_UL_layer_list          — Photoshop-style layer list with visibility toggles
├── BDS_PT_smart_material_panel    — Smart material library + apply
├── BDS_PT_bake_panel              — Bake settings + export
└── BDS_PT_udim_panel              — UDIM tile grid management
```

---

## 5. Code Structure — Key Classes and Data Structures

### Data Model Classes (`core/`)

| Class | File | Responsibility |
|---|---|---|
| `PatternPiece` | `pattern.py` | Single 2D pattern outline with verts, edges, metadata |
| `PatternCollection` | `pattern.py` | Container of all pattern pieces |
| `SeamSegment` | `seam.py` | Links two edge sequences across pieces |
| `SeamCollection` | `seam.py` | All seams in a garment |
| `Garment` | `garment.py` | Assembly: patterns + seams → 3D mesh |
| `FabricMaterial` | `fabric.py` | Physical cloth properties |
| `SimulationController` | `simulation.py` | Manages cloth modifier lifecycle |
| `PaintLayer` | `layer_stack.py` | Single paint layer with per-channel images |
| `LayerStack` | `layer_stack.py` | Ordered stack of layers with compositing |
| `BrushSettings` | `paint_engine.py` | Brush configuration |
| `PaintStroke` | `paint_engine.py` | Stroke recording + pixel writing |
| `UDIMTileSet` | `udim.py` | UDIM tile image management |
| `BakeManager` | `bake.py` | Texture baking orchestration |
| `BDS_SmartMaterialTree` | `smart_material_tree.py` | Custom node tree type |

### Operator Classes (`ops/`)

| Class | `bl_idname` | Type |
|---|---|---|
| `BDS_OT_create_pattern` | `bds.create_pattern` | Standard |
| `BDS_OT_add_pattern_point` | `bds.add_pattern_point` | Modal |
| `BDS_OT_move_pattern_point` | `bds.move_pattern_point` | Modal |
| `BDS_OT_triangulate_pattern` | `bds.triangulate_pattern` | Standard |
| `BDS_OT_import_pattern` | `bds.import_pattern` | File-select |
| `BDS_OT_select_seam_edge` | `bds.select_seam_edge` | Modal |
| `BDS_OT_stitch_seams` | `bds.stitch_seams` | Standard |
| `BDS_OT_sim_setup` | `bds.sim_setup` | Standard |
| `BDS_OT_sim_start` | `bds.sim_start` | Modal (timer) |
| `BDS_OT_sim_pause` | `bds.sim_pause` | Standard |
| `BDS_OT_sim_reset` | `bds.sim_reset` | Standard |
| `BDS_OT_paint_stroke` | `bds.paint_stroke` | Modal |
| `BDS_OT_paint_fill` | `bds.paint_fill` | Standard |
| `BDS_OT_layer_add` | `bds.layer_add` | Standard |
| `BDS_OT_layer_remove` | `bds.layer_remove` | Standard |
| `BDS_OT_layer_move` | `bds.layer_move` | Standard |
| `BDS_OT_bake_textures` | `bds.bake_textures` | Standard |
| `BDS_OT_export_textures` | `bds.export_textures` | File-select |

### Property Groups (`props/`)

```python
class BDS_PatternPieceProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    fabric_preset: bpy.props.EnumProperty(items=[...])
    seam_allowance: bpy.props.FloatProperty(default=0.01, min=0.0)

class BDS_LayerProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    visible: bpy.props.BoolProperty(default=True)
    opacity: bpy.props.FloatProperty(default=1.0, min=0.0, max=1.0)
    blend_mode: bpy.props.EnumProperty(items=[...])
    locked: bpy.props.BoolProperty(default=False)

class BDS_SceneProps(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty(items=[
        ('PATTERN', 'Pattern', 'Pattern drafting mode'),
        ('DRAPE', 'Drape', 'Cloth simulation mode'),
        ('PAINT', 'Paint', 'Texture painting mode'),
    ])
    pattern_pieces: bpy.props.CollectionProperty(type=BDS_PatternPieceProps)
    active_piece_index: bpy.props.IntProperty()
    paint_layers: bpy.props.CollectionProperty(type=BDS_LayerProps)
    active_layer_index: bpy.props.IntProperty()
    active_channel: bpy.props.EnumProperty(items=[
        ('base_color', 'Base Color', ''),
        ('metallic', 'Metallic', ''),
        ('roughness', 'Roughness', ''),
        ('normal', 'Normal', ''),
        ('height', 'Height', ''),
    ])
```

---

## 6. Integration Points

### Between Garment and Paint Pipelines

1. **Shared Mesh**: A draped garment mesh is directly paintable. The `LayerStack` is attached via `BDS_SceneProps` to the same object.
2. **UV Continuity**: Pattern pieces generate UV islands that map 1:1 to UDIM tiles. When a pattern is triangulated, UVs are auto-assigned so the paint pipeline can target specific pieces.
3. **Seam Visibility**: Seam edges are stored in a vertex group (`bds_seams`), allowing the smart material system to generate wear/stitch effects along seams.

### With Blender's Native Systems

| Blender Feature | Integration |
|---|---|
| **Shader Editor** | `LayerStack.build_shader_tree()` auto-generates a Principled BSDF node tree with Mix nodes per layer |
| **Cloth Modifier** | `SimulationController` configures native Cloth; no custom solver needed for v1 |
| **UV Editor** | UDIM tiles are standard Blender tiled images; artists can edit UVs normally |
| **Texture Paint Mode** | BDS painting supplements (not replaces) native texture paint; layers are standard `bpy.types.Image` |
| **Render Engines** | Baked textures are standard PBR maps compatible with Cycles and EEVEE |
| **Animation System** | Cloth sim bakes to standard cache; garment animations play normally |

---

## 7. Challenges and Solutions

### Challenge 1: Real-Time Cloth Simulation Performance

**Problem**: Blender's cloth sim is frame-locked and can be slow for high-poly garments.

**Solution**:
- Use the native Cloth modifier for quality draping (it's GPU-accelerated in Blender 3.x+).
- For interactive preview, use a decimated proxy mesh (e.g., 5K triangles) with a Shrinkwrap modifier transferring results to the hi-res mesh.
- Implement `SimulationController.start_realtime()` with a timer that steps frames at 30 fps on the proxy.

### Challenge 2: Layer Compositing Performance

**Problem**: Compositing 10+ layers in Python is too slow for real-time preview.

**Solution**:
- Use numpy for CPU compositing (vectorized operations on the full image buffer).
- For real-time preview, use a GPU fragment shader that samples all layer textures and blends them per-pixel.
- Only re-composite dirty regions (track bounding box of each stroke).

### Challenge 3: Painting Precision (Seam Bleeding, UV Distortion)

**Problem**: Brush strokes near UV seams produce visible artifacts. UV distortion warps brush stamps.

**Solution**:
- Implement seam padding: after stamping, dilate the painted region by N pixels across UV boundaries using a flood-fill in the image buffer.
- Compensate for UV distortion by scaling the brush footprint inversely to the Jacobian of the UV→3D mapping at the hit point.

### Challenge 4: Undo/Redo for Paint Strokes

**Problem**: Blender's undo system snapshots the entire scene; pixel-level undo is expensive.

**Solution**:
- Store per-stroke image diffs (only the changed pixel region) in a custom undo stack.
- Use `bpy.types.Operator.bl_options = {'UNDO'}` so the operator itself is in Blender's undo history.
- On undo, restore the saved pixel region rather than the entire image.

### Challenge 5: UDIM Cross-Tile Painting

**Problem**: A single brush stroke may span two UDIM tiles.

**Solution**:
- In `PaintStroke.apply()`, detect when the brush footprint crosses a tile boundary.
- Split the stamp into two partial stamps, one per tile, with correct UV remapping.

### Challenge 6: Custom 2D Editor Without SpaceType Registration

**Problem**: Blender's Python API does not allow registering entirely new editor types (SpaceTypes).

**Solution**:
- Use a 3D Viewport in orthographic top-down mode as the 2D editor.
- Lock camera rotation via a modal operator.
- Draw pattern overlays using `gpu` module draw handlers in POST_PIXEL space.
- This gives a "fake" 2D editor that feels native.

---

## 8. UI/UX Considerations

### Workflow Modes

The addon uses a three-mode paradigm matching the real-world workflow:

1. **Pattern Mode** — Draw/import 2D patterns, define seams, adjust pieces. Viewport locks to orthographic 2D. Toolbar shows pattern-specific tools.
2. **Drape Mode** — Position pieces around an avatar, run cloth simulation, adjust fabric properties. Standard 3D viewport. Toolbar shows simulation controls.
3. **Paint Mode** — Layer-based PBR painting on the draped garment. Toolbar shows brush settings, layer panel. Similar to entering Blender's Texture Paint mode but with the BDS layer engine active.

Mode is selected via `BDS_SceneProps.mode` and the main panel dynamically shows the relevant sub-panels.

### Keymap

| Key | Action | Mode |
|---|---|---|
| `B` | Brush tool | Paint |
| `E` | Eraser | Paint |
| `F` | Resize brush (drag) | Paint |
| `Shift+F` | Adjust strength (drag) | Paint |
| `P` | Add point | Pattern |
| `S` | Select seam edge | Pattern |
| `Space` | Start/Pause simulation | Drape |
| `Alt+Z` | Toggle X-ray (see through garment) | Drape |

Registered via `bpy.context.window_manager.keyconfigs.addon.keymaps.new()`.

### Layer List UX

- `bpy.types.UIList` subclass showing layer name, visibility eye icon, blend mode dropdown, opacity slider.
- Drag-to-reorder via `BDS_OT_layer_move` with `direction` enum property.
- Right-click context menu: Duplicate, Merge Down, Flatten Visible.

### Pie Menus

- `Ctrl+Shift+P` — Quick pattern tools pie menu.
- `Ctrl+Shift+B` — Quick brush selection pie menu.

### Status Bar Hints

Use `context.workspace.status_text_set("LMB: Paint | RMB: Cancel | F: Resize Brush")` during modal operators to guide users.

---

## Summary & Milestone Schedule

| Phase | Feature | Key Deliverables |
|---|---|---|
| **1** | Pattern Drafting | 2D editor overlay, pattern data model, import SVG/DXF |
| **2** | Seam Stitching | Seam data model, stitch operators, garment assembly |
| **3** | Cloth Simulation | Fabric presets, sim controller, real-time draping |
| **4** | Texture Painting | Layer stack, brush engine, PBR channel painting |
| **5** | UDIM Support | Tile manager, cross-tile painting |
| **6** | Smart Materials | Custom node tree, procedural masks, auto-layering |
| **7** | Baking Pipeline | High→low bake, layer flatten, texture export |
| **8** | UI/UX Polish | Multi-mode panels, keymaps, pie menus, status hints |

Each phase builds on the previous, with the garment pipeline (Phases 1–3) and paint pipeline (Phases 4–7) converging at Phase 8 for a unified experience.