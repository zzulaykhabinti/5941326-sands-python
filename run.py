"""
run.py

This script demonstrates the use of signal generation and time-domain transformations
provided by my signals.py file. in short what it does is:
 - it Generates sine and triangle waveforms
 - it Applies time shift, time scale, and combined transformations
 - makes the plots and saves each result to a PNG file for visual inspection
"""

import numpy as np
import matplotlib.pyplot as plt

# Import transformation utilities and signal generators
from signals import (
    sine_signal,
    triangle_signal,
    time_shift,
    time_scale,
    time_shift_and_scale
)


# Signal generation and transform parameters

FREQ = 5.0        # Frequency in Hertz
AMP = 1.0         # Amplitude of signals
FS = 200          # Sampling rate in samples per second
T0, T1 = 0.0, 2.0 # Time range for the signal in seconds

TAU = 0.30        # Time shift in seconds (positive = right shift)
A = 1.5           # Time scaling factor (>1 compresses; <1 stretches)
FILL = 0.0        # Fill value for undefined regions after interpolation


def plot_and_save(
    t_orig, y_orig,
    t_shifted, y_shifted,
    t_scaled, y_scaled,
    title, out_file
):
    """
    Plots original, time-shifted, and time-scaled versions of a signal.

    Parameters:
        t_orig (np.ndarray): Original time values
        y_orig (np.ndarray): Original signal values
        t_shifted (np.ndarray): Time values after shifting
        y_shifted (np.ndarray): Signal after time shift
        t_scaled (np.ndarray): Time values after scaling
        y_scaled (np.ndarray): Signal after time scaling
        title (str): Plot title
        out_file (str): Output file path for PNG
    """
    plt.figure(figsize=(10, 5.5))
    plt.plot(t_orig, y_orig, label="Original", lw=1.8)
    plt.plot(t_shifted, y_shifted, '--', label=f"Shifted (τ={TAU}s)", lw=1.5)
    plt.plot(t_scaled, y_scaled, ':', label=f"Scaled (a={A})", lw=1.5)

    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    plt.close()
    print(f"Saved plot to: {out_file}")


def plot_combined(t_orig, y_orig, t_comb, y_comb, title, out_file):
    """
    Plots original signal versus a combined shift-and-scale transformation.

    Parameters:
        t_orig (np.ndarray): Original time vector
        y_orig (np.ndarray): Original signal
        t_comb (np.ndarray): Transformed time vector
        y_comb (np.ndarray): Transformed signal (shift + scale)
        title (str): Plot title
        out_file (str): Output filename
    """
    plt.figure(figsize=(10, 5.5))
    plt.plot(t_orig, y_orig, label="Original", lw=1.8)
    plt.plot(t_comb, y_comb, "--", label=f"Combined (a={A}, τ={TAU})", lw=1.5)

    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    plt.close()
    print(f"Saved plot to: {out_file}")


def main():
    # --- Signal generation ---
    t_sin, y_sin = sine_signal(FREQ, T0, T1, AMP, FS)
    t_tri, y_tri = triangle_signal(FREQ, T0, T1, AMP, FS)

    # --- Apply time-domain operations ---
    t_sin_shifted, y_sin_shifted = time_shift(t_sin, y_sin, TAU)
    t_tri_shifted, y_tri_shifted = time_shift(t_tri, y_tri, TAU)

    t_sin_scaled, y_sin_scaled = time_scale(t_sin, y_sin, A, fill=FILL)
    t_tri_scaled, y_tri_scaled = time_scale(t_tri, y_tri, A, fill=FILL)

    t_sin_comb, y_sin_comb = time_shift_and_scale(t_sin, y_sin, TAU, A, fill=FILL)
    t_tri_comb, y_tri_comb = time_shift_and_scale(t_tri, y_tri, TAU, A, fill=FILL)

    #Visualization of the output
    plot_and_save(
        t_sin, y_sin,
        t_sin_shifted, y_sin_shifted,
        t_sin_scaled, y_sin_scaled,
        title="Sine Wave: Original vs Shifted vs Scaled",
        out_file="sine_shift_scale.png"
    )

    plot_combined(
        t_sin, y_sin,
        t_sin_comb, y_sin_comb,
        title="Sine Wave: Original vs Combined (Shift + Scale)",
        out_file="sine_combined.png"
    )

    plot_and_save(
        t_tri, y_tri,
        t_tri_shifted, y_tri_shifted,
        t_tri_scaled, y_tri_scaled,
        title="Triangle Wave: Original vs Shifted vs Scaled",
        out_file="triangle_shift_scale.png"
    )

    plot_combined(
        t_tri, y_tri,
        t_tri_comb, y_tri_comb,
        title="Triangle Wave: Original vs Combined (Shift + Scale)",
        out_file="triangle_combined.png"
    )

    #Basic verification  of the output
    print("First 10 samples of sine:", np.round(y_sin[:10], 6))
    print("First 10 samples of triangle:", np.round(y_tri[:10], 6))


if __name__ == "__main__":
    main()
