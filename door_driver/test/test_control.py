import math

from door_driver.control import command, progress, wrap, yaw_of


def test_full_speed_then_slows_then_stops_at_2m():
    assert command(0.0, 2.0, 0.0) == (0.4, 0.0)
    v, _ = command(1.8, 2.0, 0.0)
    assert 0.0 < v < 0.4
    assert command(2.0, 2.0, 0.0) == (0.0, 0.0)
    assert command(2.1, 2.0, 0.0) == (0.0, 0.0)  # overshoot: stays stopped


def test_creeps_rather_than_stalls_just_short():
    v, _ = command(1.98, 2.0, 0.0)
    assert v > 0.0


def test_steers_back_onto_the_heading():
    assert command(1.0, 2.0, 0.1)[1] < 0
    assert command(1.0, 2.0, -0.1)[1] > 0


def test_progress_is_along_the_start_heading():
    assert abs(progress((-4.6, -3.2, 0.0), -2.6, -3.2) - 2.0) < 1e-9
    assert abs(progress((0.0, 0.0, math.pi / 2), 0.3, 1.5) - 1.5) < 1e-9  # sideways drift doesn't count
    assert progress((0.0, 0.0, 0.0), -0.5, 0.0) < 0


def test_angles():
    assert abs(yaw_of(math.sin(0.5), math.cos(0.5)) - 1.0) < 1e-9
    assert abs(wrap(3 * math.pi) - math.pi) < 1e-9
