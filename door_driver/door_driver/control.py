"""The forward drive's control law, without ROS (so it is tested on its own)."""

import math

ARRIVED_TOLERANCE = 0.01  # m


def yaw_of(qz: float, qw: float) -> float:
    return 2.0 * math.atan2(qz, qw)


def wrap(a: float) -> float:
    return math.atan2(math.sin(a), math.cos(a))


def progress(start: tuple[float, float, float], x: float, y: float) -> float:
    """Metres travelled along the start heading (negative if behind the start)."""
    x0, y0, yaw0 = start
    return (x - x0) * math.cos(yaw0) + (y - y0) * math.sin(yaw0)


def command(travelled: float, distance: float, heading_error: float, speed: float = 0.4,
            slow_zone: float = 0.6, min_speed: float = 0.05, k_heading: float = 1.5) -> tuple[float, float]:
    """(v, w): `speed` until the last `slow_zone` metres, then slowing in proportion to what is left; zero once within
    ARRIVED_TOLERANCE of `distance` (or past it). w steers back onto the start heading."""
    left = distance - travelled
    if left <= ARRIVED_TOLERANCE:
        return 0.0, 0.0
    v = max(min_speed, speed * min(1.0, left / slow_zone))
    w = max(-0.5, min(0.5, -k_heading * heading_error))
    return v, w
