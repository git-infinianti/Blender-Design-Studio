"""Geometry helpers: Delaunay, convex hull, intersection tests."""
import math
from typing import Tuple, Optional, List
from mathutils import Vector


def point_in_triangle(p: Vector, a: Vector, b: Vector,
                      c: Vector) -> bool:
    """Test if point p lies inside triangle abc using barycentric coords."""
    v0 = c - a
    v1 = b - a
    v2 = p - a

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < 1e-10:
        return False

    inv_denom = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return u >= 0 and v >= 0 and (u + v) <= 1


def barycentric_coords(p: Vector, a: Vector, b: Vector,
                       c: Vector) -> Tuple[float, float, float]:
    """Compute barycentric coordinates of p with respect to triangle abc."""
    v0 = b - a
    v1 = c - a
    v2 = p - a

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < 1e-10:
        return (1.0, 0.0, 0.0)

    inv_denom = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom
    w = 1.0 - u - v

    return (w, u, v)


def line_segment_intersection(
    p1: Vector, p2: Vector, p3: Vector, p4: Vector
) -> Optional[Vector]:
    """Find intersection point of line segments p1-p2 and p3-p4.
    
    Returns the intersection point or None if segments don't intersect.
    """
    d1 = p2 - p1
    d2 = p4 - p3
    d3 = p3 - p1

    cross_d1_d2 = d1.x * d2.y - d1.y * d2.x
    if abs(cross_d1_d2) < 1e-10:
        return None

    t = (d3.x * d2.y - d3.y * d2.x) / cross_d1_d2
    u = (d3.x * d1.y - d3.y * d1.x) / cross_d1_d2

    if 0 <= t <= 1 and 0 <= u <= 1:
        return Vector((p1.x + t * d1.x, p1.y + t * d1.y))
    return None


def polygon_area(vertices: List[Vector]) -> float:
    """Compute area of a polygon using the shoelace formula."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i].x * vertices[j].y
        area -= vertices[j].x * vertices[i].y
    return abs(area) / 2.0


def polygon_centroid(vertices: List[Vector]) -> Vector:
    """Compute the centroid of a polygon."""
    if not vertices:
        return Vector((0, 0))
    cx = sum(v.x for v in vertices) / len(vertices)
    cy = sum(v.y for v in vertices) / len(vertices)
    return Vector((cx, cy))


def angle_between_vectors(v1: Vector, v2: Vector) -> float:
    """Compute the angle in radians between two 2D vectors."""
    dot = v1.normalized().dot(v2.normalized())
    dot = max(-1.0, min(1.0, dot))
    return math.acos(dot)


def convex_hull_2d(points: List[Vector]) -> List[int]:
    """Compute 2D convex hull using Andrew's monotone chain algorithm.
    
    Returns list of indices forming the convex hull in CCW order.
    """
    if len(points) <= 1:
        return list(range(len(points)))

    indexed = sorted(enumerate(points), key=lambda p: (p[1].x, p[1].y))

    def cross(o, a, b):
        return ((a[1].x - o[1].x) * (b[1].y - o[1].y) -
                (a[1].y - o[1].y) * (b[1].x - o[1].x))

    lower = []
    for p in indexed:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(indexed):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    return [p[0] for p in hull]


def distance_point_to_segment(p: Vector, a: Vector, b: Vector) -> float:
    """Compute the minimum distance from point p to segment ab."""
    ab = b - a
    ap = p - a
    t = ap.dot(ab) / ab.dot(ab) if ab.dot(ab) > 0 else 0.0
    t = max(0.0, min(1.0, t))
    closest = a + ab * t
    return (p - closest).length
