import numpy as np
import math

from signals import (
    _make_timebase,
    sine_signal,
    triangle_signal,
    time_shift,
    time_scale,
    time_shift_and_scale,
)

# Tolerance levels for the numerical comparisons
RTOL = 1e-7
ATOL = 1e-12

def almost_equal(a, b, rtol=RTOL, atol=ATOL):
    """
    Wrapper around np.allclose with stricter default tolerances.
    """
    return np.allclose(a, b, rtol=rtol, atol=atol)
    
# Timebase Tests
def test_make_timebase_basic():
    """
    Ensure _make_timebase creates the correct number of samples and spacing.
    """
    t = _make_timebase(0.0, 1.0, 10.0)  # Should result in 10 samples: [0.0, 0.1, ..., 0.9]
    assert len(t) == 10
    assert math.isclose(t[1] - t[0], 0.1, rel_tol=1e-12, abs_tol=1e-12)
    assert t[0] == 0.0
    assert t[-1] < 1.0  # Should not include the endpoint


def test_make_timebase_errors():
    """
    _make_timebase should raise ValueError on invalid input parameters.
    """
    try:
        _make_timebase(0, 1, 0)  # Zero sampling rate
        assert False, "Expected ValueError for fs <= 0"
    except ValueError:
        pass

    try:
        _make_timebase(1, 0, 10)  # Reversed time range
        assert False, "Expected ValueError for t_end <= t_start"
    except ValueError:
        pass
# Signal Generator Tests
def test_sine_signal_length_and_range():
    """
    Check sine signal length and amplitude bounds.
    """
    f, amp, fs, t0, t1 = 5.0, 2.0, 200.0, 0.0, 2.0
    t, y = sine_signal(f, t0, t1, amp, fs, phase=0.0)
    expected_len = int((t1 - t0) * fs)
    assert len(t) == expected_len
    assert len(y) == expected_len
    assert np.max(y) <= amp + 1e-9
    assert np.min(y) >= -amp - 1e-9


def test_triangle_signal_length_and_range():
    """
    Check triangle signal length and amplitude bounds.
    """
    f, amp, fs, t0, t1 = 5.0, 1.0, 200.0, 0.0, 2.0
    t, y = triangle_signal(f, t0, t1, amp, fs)
    expected_len = int((t1 - t0) * fs)
    assert len(t) == expected_len
    assert len(y) == expected_len
    assert np.max(y) <= amp + 1e-9
    assert np.min(y) >= -amp - 1e-9


# Time Transformation Tests
def test_time_shift_pure_shift():
    """
    Validate the time shift: time values should be shifted by tau, the data remains unchanged.
    """
    t = np.array([0.0, 0.1, 0.2, 0.3])
    y = np.array([10.0, 11.0, 12.0, 13.0])
    tau = 0.25
    ts, ys = time_shift(t, y, tau)
    assert almost_equal(ts, t + tau)
    assert np.array_equal(ys, y)


def test_time_scale_basic():
    """
    Scaling by factor 'a' compresses or stretches the signal in time.

    This test uses y = t for simplicity, so we expect:
    y_scaled(t) ≈ original(a*t) within defined domain; otherwise, it uses the fill value.
    """
    t = np.linspace(0, 1, 11)
    y = t.copy()
    ts, ys = time_scale(t, y, a=2.0, fill=-1.0)
    assert almost_equal(ts, t)

    # Values for t in [0, 0.5] should follow y=2t
    in_bounds = t <= 0.5 + 1e-12
    assert almost_equal(ys[in_bounds], 2.0 * t[in_bounds])
    assert np.allclose(ys[~in_bounds], -1.0)  # Should match fill

def test_time_shift_and_scale_equivalence():
    """
    time_shift_and_scale should match manual interpolation of x(a * t - tau).
    """
    f, amp, fs, t0, t1 = 5.0, 1.0, 100.0, 0.0, 1.0
    tau, a = 0.15, 1.2
    t, y = sine_signal(f, t0, t1, amp, fs)

    tc, yc = time_shift_and_scale(t, y, tau=tau, a=a, fill=0.0)

    # Expected result for this method using direct interpolation
    query = a * t - tau
    y_expected = np.interp(query, t, y, left=0.0, right=0.0)

    assert almost_equal(tc, t)
    assert almost_equal(yc, y_expected)
    
# Script Mode
if __name__ == "__main__":
    test_make_timebase_basic()
    test_make_timebase_errors()
    test_sine_signal_length_and_range()
    test_triangle_signal_length_and_range()
    test_time_shift_pure_shift()
    test_time_scale_basic()
    test_time_shift_and_scale_equivalence()
    print("Passed all test")
