import math

from aisle_driver.control import command, wrap, yaw_of


def test_full_speed_then_slows_then_stops():
    assert command(0.0, 8.0, 0.0) == (0.5, 0.0)
    v, _ = command(7.5, 8.0, 0.0)
    assert 0.0 < v < 0.5
    assert command(8.0, 8.0, 0.0) == (0.0, 0.0)


def test_steers_back_onto_the_heading():
    _, w = command(1.0, 8.0, 0.1)
    assert w < 0
    _, w = command(1.0, 8.0, -0.1)
    assert w > 0


def test_angles():
    assert abs(yaw_of(math.sin(0.5), math.cos(0.5)) - 1.0) < 1e-9
    assert abs(wrap(3 * math.pi) - math.pi) < 1e-9
