
import numpy as np


#Function to create a uniform time vector
def _make_timebase(t_start: float, t_end: float, fs: float) -> np.ndarray:
    """
    Generates a uniform time vector from t_start to t_end with sampling rate fs.
    
    Parameters:
        t_start (float): Start time in seconds.
        t_end (float): End time in seconds (exclusive).
        fs (float): Sampling frequency in Hz (must be > 0).
    
    Returns:
        np.ndarray: Time samples spaced by 1/fs.
    """
    if fs <= 0:
        raise ValueError("Sampling rate fs must be > 0.")
    if t_end <= t_start:
        raise ValueError("End time must be greater than start time.")

    dt = 1.0 / fs
    return np.arange(t_start, t_end, dt)


#Function to generate signal

def sine_signal(freq: float, t0: float, t1: float, amp: float, fs: float, phase: float = 0.0):
    """
    Generate a sinusoidal waveform: y(t) = A·sin(2πft + φ)

    Parameters:
        freq (float): Frequency in Hz.
        t0 (float): Start time (seconds).
        t1 (float): End time (seconds), exclusive.
        amp (float): Amplitude.
        fs (float): Sampling rate in Hz.
        phase (float): Phase offset in radians.

    Returns:
        tuple (np.ndarray, np.ndarray): Time vector and signal vector.
    """
    t = _make_timebase(t0, t1, fs)
    y = amp * np.sin(2 * np.pi * freq * t + phase)

    return t, y


def triangle_signal(freq: float, t0: float, t1: float, amp: float, fs: float):
    """
    Generate a symmetric triangular waveform over time base.

    Parameters:
        freq (float): Frequency in Hz.
        t0 (float): Start time (seconds).
        t1 (float): End time (seconds), exclusive.
        amp (float): Peak amplitude.
        fs (float): Sampling rate in Hz.

    Returns:
        tuple (np.ndarray, np.ndarray): Time vector and signal vector.
    """
    t = _make_timebase(t0, t1, fs)

    #Function to make the phase ranges from 0 to 1
    frac = (freq * t) % 1.0

    #Triangle scaled to [-1, 1] then to [-amp, amp]
    tri = 2.0 * np.abs(2.0 * frac - 1.0) - 1.0

    return t, amp * tri


#Functions to create time-domains 

def time_shift(t: np.ndarray, y: np.ndarray, tau: float):
    """
    Apply a pure time shift to signal (non-interpolative).
    x(t) -> x(t - τ)

    Parameters:
        t (np.ndarray): Time vector.
        y (np.ndarray): Signal values.
        tau (float): Time shift in seconds (positive = delay).

    Returns:
        tuple (np.ndarray, np.ndarray): Shifted time vector and original signal.
    """
    if t.shape[0] != y.shape[0]:
        raise ValueError("Length mismatch between time and signal arrays.")

    #To ensure no resampling
    return t + tau, y


def time_scale(t: np.ndarray, y: np.ndarray, a: float, fill: float = 0.0):
    """
    Apply time scaling via interpolation: x(t) -> x(a·t)

    Parameters:
        t (np.ndarray): Original time vector.
        y (np.ndarray): Signal values.
        a (float): Time scaling factor (a > 1 compresses, a < 1 stretches).
        fill (float): Fill value for extrapolated regions.

    Returns:
        tuple (np.ndarray, np.ndarray): Original time vector and resampled signal.
    """
    if a == 0:
        raise ValueError("Scaling factor 'a' must be nonzero.")
    if t.shape[0] != y.shape[0]:
        raise ValueError("Input time and signal arrays must have same length.")

    #Interpolation points shifted by the scaling factor
    query_points = a * t
    y_scaled = np.interp(query_points, t, y, left=fill, right=fill)

    return t, y_scaled


def time_shift_and_scale(t: np.ndarray, y: np.ndarray, tau: float, a: float, fill: float = 0.0):
    """
    Apply combined affine time transform: x(t) -> x(a·t - τ)

    Parameters:
        t (np.ndarray): Time vector.
        y (np.ndarray): Signal values.
        tau (float): Time shift in seconds.
        a (float): Time scaling factor.
        fill (float): Fill value for out-of-domain samples.

    Returns:
        tuple (np.ndarray, np.ndarray): Time vector and transformed signal.
    """
    if a == 0:
        raise ValueError("Scaling factor 'a' must not be zero.")
    if t.shape[0] != y.shape[0]:
        raise ValueError("Length mismatch between t and y arrays.")

    #Combined time remapping in order to rescale then shift
    query = a * t - tau
    y_trans = np.interp(query, t, y, left=fill, right=fill)

    return t, y_trans