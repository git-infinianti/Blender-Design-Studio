"""Image buffer manipulation utilities for texture painting."""
from typing import Tuple, Optional

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


def create_blank_image(name: str, width: int, height: int,
                       color: Tuple[float, float, float, float] = (0, 0, 0, 0),
                       is_data: bool = False) -> Optional['bpy.types.Image']:
    """Create a new blank image with the given fill color."""
    if not HAS_BPY:
        return None

    img = bpy.data.images.new(name, width, height, alpha=True,
                               is_data=is_data)
    if is_data:
        img.colorspace_settings.name = 'Non-Color'

    # Fill with color
    r, g, b, a = color
    pixels = [0.0] * (width * height * 4)
    for i in range(0, len(pixels), 4):
        pixels[i] = r
        pixels[i + 1] = g
        pixels[i + 2] = b
        pixels[i + 3] = a
    img.pixels[:] = pixels
    img.update()
    return img


def copy_image_data(src: 'bpy.types.Image',
                    dst: 'bpy.types.Image') -> bool:
    """Copy pixel data from source image to destination image."""
    if not HAS_BPY:
        return False

    if (src.size[0] != dst.size[0] or src.size[1] != dst.size[1]):
        return False

    dst.pixels[:] = src.pixels[:]
    dst.update()
    return True


def dilate_image(img: 'bpy.types.Image', iterations: int = 1) -> None:
    """Dilate non-transparent pixels outward to reduce UV seam artifacts.
    
    This extends painted pixels into neighboring transparent areas,
    which helps prevent visible seams in the final texture.
    """
    if not HAS_BPY or not HAS_NUMPY:
        return

    width, height = img.size[0], img.size[1]
    pixels = np.array(img.pixels[:]).reshape((height, width, 4))

    for _ in range(iterations):
        alpha = pixels[:, :, 3]
        new_pixels = pixels.copy()

        # Find transparent pixels adjacent to opaque ones
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                # Shift the array
                shifted_alpha = np.roll(np.roll(alpha, dy, axis=0),
                                        dx, axis=1)
                shifted_pixels = np.roll(np.roll(pixels, dy, axis=0),
                                         dx, axis=1)

                # Where current pixel is transparent but neighbor is opaque
                mask = (alpha < 0.01) & (shifted_alpha > 0.01)
                for c in range(4):
                    new_pixels[:, :, c] = np.where(
                        mask, shifted_pixels[:, :, c], new_pixels[:, :, c]
                    )

        pixels = new_pixels

    img.pixels[:] = pixels.ravel().tolist()
    img.update()


def get_image_region(img: 'bpy.types.Image',
                     x: int, y: int, width: int,
                     height: int) -> Optional['np.ndarray']:
    """Extract a rectangular region from an image as a numpy array."""
    if not HAS_BPY or not HAS_NUMPY:
        return None

    img_w, img_h = img.size[0], img.size[1]
    pixels = np.array(img.pixels[:]).reshape((img_h, img_w, 4))

    x = max(0, min(x, img_w))
    y = max(0, min(y, img_h))
    x2 = max(0, min(x + width, img_w))
    y2 = max(0, min(y + height, img_h))

    return pixels[y:y2, x:x2].copy()


def set_image_region(img: 'bpy.types.Image',
                     x: int, y: int,
                     region: 'np.ndarray') -> None:
    """Set a rectangular region of an image from a numpy array."""
    if not HAS_BPY or not HAS_NUMPY:
        return

    img_w, img_h = img.size[0], img.size[1]
    pixels = np.array(img.pixels[:]).reshape((img_h, img_w, 4))

    rh, rw = region.shape[:2]
    x2 = min(x + rw, img_w)
    y2 = min(y + rh, img_h)

    pixels[y:y2, x:x2] = region[:y2 - y, :x2 - x]

    img.pixels[:] = pixels.ravel().tolist()
    img.update()
