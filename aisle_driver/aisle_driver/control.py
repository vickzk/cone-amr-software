"""The aisle drive's control law, without ROS (so it is tested on its own)."""

import math


def yaw_of(qz: float, qw: float) -> float:
    return 2.0 * math.atan2(qz, qw)


def wrap(a: float) -> float:
    return math.atan2(math.sin(a), math.cos(a))


def command(travelled: float, distance: float, heading_error: float, speed: float = 0.5,
            slow_zone: float = 1.0, k_heading: float = 1.5) -> tuple[float, float]:
    """(v, w): full speed, slowing over the last `slow_zone` metres, zero at `distance`; w steers back on heading."""
    left = distance - travelled
    if left <= 0.02:
        return 0.0, 0.0
    v = speed * min(1.0, max(0.15, left / slow_zone))
    w = max(-0.6, min(0.6, -k_heading * heading_error))
    return v, w
