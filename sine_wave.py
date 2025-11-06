import numpy as np

def create_sine_wave(frequency,duration):
    t = np.linspace(0, duration, int(44100 * duration))
    return np.sin(2 * np.pi * frequency * t)

print(create_sine_wave(440,2))
