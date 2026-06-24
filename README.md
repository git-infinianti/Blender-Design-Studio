# Blender Design Studio

> A comprehensive Blender extension combining **Marvelous Designer**-style garment design and **Substance Painter**-style texture painting within Blender's native environment.

**Compatible with Blender 4.2+ and 5.x (including 5.1.2)**

---

## Features

### 🧵 Garment Design Pipeline
- **2D Pattern Drafting** — Draw, edit, and import (SVG/DXF) pattern pieces in an orthographic 2D editor overlay
- **Garment Presets** — One-click loading of common garment templates (T-Shirt, Skirt, Pants, Dress) with pre-configured seams
- **Seam Stitching** — Define seam pairs between pattern edges, auto-match by proximity, and stitch into a single mesh
- **Cloth Simulation** — Real-time draping with 8 fabric presets (cotton, silk, denim, leather, chiffon, wool, polyester, linen)
- **Avatar Wrapping** — Automatically position pattern pieces around a character mesh for simulation

### 🎨 Texture Paint Pipeline
- **Layer-Based PBR Painting** — Photoshop-style layer stack with blend modes (Mix, Multiply, Screen, Overlay, Add)
- **Per-Channel Painting** — Paint directly to Base Color, Metallic, Roughness, Normal, or Height channels
- **UDIM Support** — Full tiled texture workflow with automatic tile detection and cross-tile painting
- **Clone Stamp** — Sample from a reference point and paint cloned texture at target locations
- **Color Picker** — Sample color directly from painted layers on the mesh surface
- **Fill Tool** — Fill entire layers or UV islands with solid colors
- **Projection Painting** — Project images onto mesh surfaces from the current view
- **Smart Materials** — Procedural mask system with curvature, AO, and position gradient nodes
- **Batch Texture Export** — Export all channels for all objects in one operation (PNG, JPEG, EXR, TGA)

### 🔧 Quality of Life
- **Quick Fabric Assign** — Rapidly change cloth physics properties with fabric presets
- **Custom Keymaps** — Intuitive keyboard shortcuts for all major tools
- **Status Bar Hints** — Contextual guidance during modal operations
- **Undo/Redo** — Per-stroke undo with minimal memory footprint
- **Shader Tree Auto-Build** — Automatically generates Principled BSDF node trees from the layer stack

---

## Installation

### Method 1: Extension Install (Blender 4.2+, Recommended)

1. Download or clone this repository
2. In Blender, go to **Edit → Preferences → Get Extensions → Install from Disk**
3. Select the `blender_design_studio/` folder (it contains `blender_manifest.toml`)
4. The extension is automatically enabled

### Method 2: Legacy Addon Install

1. Download or clone this repository
2. In Blender, go to **Edit → Preferences → Add-ons → Install**
3. Navigate to `blender_design_studio/__init__.py`
4. Enable the addon by checking **Blender Design Studio**

### After Installation

The addon panel appears in the 3D Viewport sidebar under the **BDS** tab (`N` key to open sidebar).

### Optional Dependencies

For full functionality, install these Python packages into Blender's Python environment:

```bash
# From Blender's Python directory:
./python -m pip install numpy triangle scipy Pillow
```

| Library | Purpose | Required? |
|---------|---------|-----------|
| `numpy` | Fast array math for painting and simulation | Bundled with Blender |
| `triangle` | Constrained Delaunay triangulation of patterns | Optional (fallback available) |
| `scipy` | KD-tree for nearest-point queries | Optional |
| `Pillow` | Image format conversion, compositing fallback | Optional |

The addon gracefully degrades when optional libraries are unavailable.

---

## Quick Start

### Creating a Garment from a Preset

1. Open the **BDS** sidebar panel
2. Switch to **Pattern** mode
3. Click **Load Garment Preset** and select a template (e.g., T-Shirt)
4. Pattern pieces are automatically created and assembled as a flat mesh
5. Switch to **Drape** mode
6. Select your avatar mesh and enable **Is Avatar** in the BDS object properties
7. Click **Setup Simulation** and then **Start Simulation**
8. Watch the garment drape around your character

### Painting Textures

1. Select a mesh object with UV maps
2. Switch to **Paint** mode in the BDS panel
3. Add a paint layer using the Layer panel
4. Choose your channel (Base Color, Metallic, etc.)
5. Set brush color, radius, and strength
6. Press `B` to activate the paint brush and paint directly on the mesh
7. Use **Batch Export** to save all textures at once

---

## Architecture

```
blender_design_studio/
├── blender_manifest.toml        # Extension manifest (Blender 4.2+/5.x)
├── __init__.py                  # Addon registration, bl_info, preferences
├── core/
│   ├── pattern.py               # 2D pattern geometry model
│   ├── garment.py               # Garment assembly (pieces + seams → 3D mesh)
│   ├── garment_presets.py       # Pre-built garment templates (NEW)
│   ├── simulation.py            # Cloth sim wrapper & real-time stepping
│   ├── fabric.py                # Fabric material properties (8 presets)
│   ├── seam.py                  # Seam/stitch definitions + constraints
│   ├── paint_engine.py          # Core texture paint engine (brush, stroke)
│   ├── layer_stack.py           # PBR layer stack manager with blend modes
│   ├── bake.py                  # Texture baking pipeline
│   ├── udim.py                  # UDIM tile management
│   └── smart_material.py        # Procedural smart material system
├── ops/
│   ├── pattern_ops.py           # Pattern CRUD operators
│   ├── seam_ops.py              # Seam stitching operators
│   ├── sim_ops.py               # Simulation control operators
│   ├── paint_ops.py             # Paint stroke, fill, clone, projection, pick
│   ├── layer_ops.py             # Layer add/remove/reorder operators
│   ├── bake_ops.py              # Baking operators
│   ├── preset_ops.py            # Garment presets & batch export (NEW)
│   └── import_export_ops.py     # DXF/SVG pattern import, texture export
├── ui/
│   ├── panels.py                # Main sidebar panels
│   ├── pattern_editor.py        # 2D pattern editor overlay
│   ├── layer_panel.py           # Layer stack UI
│   ├── fabric_panel.py          # Fabric property inspector
│   ├── paint_toolbar.py         # Brush/tool bar for painting
│   └── gizmos.py                # Custom gizmos (seam handles)
├── gpu/
│   ├── pattern_draw.py          # GPU-accelerated 2D pattern overlay
│   ├── paint_preview.py         # Real-time paint stroke preview
│   └── sim_preview.py           # Cloth sim wireframe overlay
├── nodes/
│   ├── smart_material_tree.py   # Custom node tree for smart materials
│   └── mask_nodes.py            # Procedural mask generator nodes
├── props/
│   ├── scene_props.py           # Scene-level addon properties
│   ├── object_props.py          # Per-object garment/paint data
│   └── preferences.py           # Addon preferences
└── utils/
    ├── math_utils.py            # Geometry helpers, convex hull
    ├── mesh_utils.py            # bmesh helpers, UV utilities, raycasting
    └── texture_utils.py         # Image buffer manipulation
```

---

## Workflow Modes

The addon uses a three-mode paradigm:

| Mode | Purpose | Key Tools |
|------|---------|-----------|
| **Pattern** | 2D pattern drafting, import, seam definition | Add Point, Move, Mirror, Import SVG/DXF, Seam Select |
| **Drape** | Cloth simulation and garment fitting | Setup Sim, Start/Pause/Reset, Bake, Apply Drape |
| **Paint** | Layer-based PBR texture painting | Brush, Fill, Clone, Projection, Color Picker |

Mode is selected via the main BDS panel and dynamically shows relevant sub-panels.

---

## Keyboard Shortcuts

| Key | Action | Mode |
|-----|--------|------|
| `B` | Brush stroke tool | Paint |
| `E` | Color picker (eyedropper) | Paint |
| `P` | Add pattern point | Pattern |
| `Shift+S` | Select seam edge | Pattern |
| `Ctrl+Shift+Space` | Start/pause simulation | Drape |

---

## Garment Presets

Pre-built templates for rapid prototyping:

| Preset | Pieces | Default Fabric | Description |
|--------|--------|----------------|-------------|
| **T-Shirt** | Front, Back, Sleeve | Cotton | Basic short-sleeve shirt |
| **A-Line Skirt** | 4 Panels | Cotton | Flared skirt with side seams |
| **Basic Pants** | Front Leg, Back Leg | Denim | Straight-leg pants |
| **Simple Dress** | Bodice, Skirt | Silk | A-line dress |

Use **Load Garment Preset** (`bds.load_garment_preset`) to instantly create a garment with pre-configured pattern pieces, seam connections, and fabric properties.

---

## Fabric Presets

| Fabric | Mass (kg/m²) | Stiffness | Damping | Bending | Character |
|--------|-------------|-----------|---------|---------|-----------|
| Cotton | 0.15 | 15.0 | 5.0 | 0.5 | Breathable, everyday |
| Silk | 0.06 | 5.0 | 2.0 | 0.1 | Flowing, lightweight |
| Denim | 0.35 | 40.0 | 10.0 | 5.0 | Heavy, structured |
| Leather | 0.50 | 80.0 | 15.0 | 10.0 | Thick, rigid |
| Chiffon | 0.04 | 3.0 | 1.0 | 0.05 | Ultra-sheer, flowing |
| Wool | 0.25 | 20.0 | 8.0 | 2.0 | Warm, medium drape |
| Polyester | 0.12 | 12.0 | 4.0 | 0.3 | Smooth, synthetic |
| Linen | 0.20 | 25.0 | 7.0 | 1.5 | Crisp, natural |

---

## Layer Stack & Paint System

The paint system uses a non-destructive layer stack:

- **Per-channel images** — Each layer stores separate images for each PBR channel
- **Blend modes** — Mix, Multiply, Screen, Overlay, Add
- **Opacity control** — Per-layer opacity with real-time preview
- **Flatten** — Composite all visible layers using numpy-accelerated blending
- **Auto shader tree** — Generates Principled BSDF node tree from flattened layers

### Brush Settings

| Property | Range | Description |
|----------|-------|-------------|
| Radius | 1–500 px | Brush size in texture pixels |
| Strength | 0.0–1.0 | Opacity/pressure multiplier |
| Falloff | Smooth/Sharp/Linear/Constant | Edge softness curve |
| Color | RGB | Paint color for base_color channel |
| Channel | base_color/metallic/roughness/normal/height | Target PBR channel |

---

## Integration with Blender

| Blender Feature | Integration |
|-----------------|-------------|
| **Shader Editor** | Auto-generates Principled BSDF node tree from layer stack |
| **Cloth Modifier** | Native cloth simulation with fabric preset configuration |
| **UV Editor** | UDIM tiles are standard Blender tiled images |
| **Texture Paint** | Supplements native painting with layer-based workflow |
| **Render Engines** | Output textures compatible with Cycles and EEVEE |
| **Animation** | Cloth simulation bakes to standard cache |

---

## API Reference

### Key Operators

| Operator | bl_idname | Description |
|----------|-----------|-------------|
| Load Garment Preset | `bds.load_garment_preset` | Load a pre-built garment template |
| Batch Export | `bds.batch_export_textures` | Export all textures for all objects |
| Quick Fabric | `bds.quick_fabric_assign` | Assign fabric properties quickly |
| Create Pattern | `bds.create_pattern` | Create a new pattern piece |
| Paint Stroke | `bds.paint_stroke` | Modal brush painting |
| Paint Fill | `bds.paint_fill` | Fill layer with color |
| Clone Stamp | `bds.paint_clone` | Clone texture from source |
| Pick Color | `bds.pick_color` | Sample color from surface |
| Setup Sim | `bds.sim_setup` | Configure cloth simulation |
| Start Sim | `bds.sim_start` | Begin real-time draping |
| Stitch Seams | `bds.stitch_seams` | Merge seam vertices |
| Add Layer | `bds.layer_add` | Add paint layer |
| Bake Textures | `bds.bake_textures` | Bake texture maps |

---

## Compatibility

| Blender Version | Status | Notes |
|-----------------|--------|-------|
| 3.x | ⚠️ Legacy | May work but unsupported |
| 4.0–4.1 | ⚠️ Partial | bl_info format only |
| 4.2–4.4 | ✅ Supported | Extension manifest supported |
| 5.0–5.1.2 | ✅ Supported | Full extension system |

### Blender 5.x Notes

- Uses `blender_manifest.toml` for extension metadata (new standard)
- Retains `bl_info` for backward compatibility with 4.x
- Fixed: `workspace.status_text_set()` → `area.header_text_set()`
- Fixed: Gizmo `PERSISTENT` option → `SHOW_MODAL_ALL`
- Fixed: Quaternion view rotation assignment uses proper `mathutils.Quaternion`
- Compatible with Python 3.13 (bundled in Blender 5.1)

---

## Development

### Running Tests

```bash
# Basic syntax check (no Blender required)
python -m py_compile blender_design_studio/__init__.py
```

### Project Structure

The addon follows Blender's recommended extension layout:
- Property groups registered before classes that use them
- Operators use `{'REGISTER', 'UNDO'}` for proper undo support
- Modal operators clean up state on cancel/finish
- GPU draw handlers properly unregister on addon disable

---

## License

See [LICENSE](LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the existing code style
4. Test in Blender 5.1+ before submitting
5. Open a Pull Request

### Code Conventions

- Use `bl_idname` prefix `bds.` for all operators
- Use `BDS_` prefix for all class names
- Property groups use type annotations (`name: StringProperty(...)`)
- Optional dependencies are guarded with `try/except ImportError`
- All core modules have `HAS_BPY` / `HAS_NUMPY` guards for testability outside Blender
