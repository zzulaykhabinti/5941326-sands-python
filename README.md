# Processing Toolkit

This is a Python-based utility for generating and modifying the basic time-domain signals.  

This is built as part of my coursework for the subject AESB2122-24 (Signals & Systems), Applied Earth Sciences at TU Delft.

---

## Project Description

This repository provides a set of tools that can be used for working with digital signals that use NumPy, Matplotlib and Math.  

It allows you to:

- Construct periodic signals like sine and triangle waves  
- Apply time-based transformations such as shifting and scaling  
- Generate visual comparisons between original and modified signals  
- Run test cases to verify the correctness of signal logic  

---

## Features

### Signal Generation

Implemented in `signals.py`, are the following functions used to generate common waveforms:

- `sine_signal(freq, t0, t1, amp, fs, phase=0.0)`  
  Produces a sine wave using the specified frequency, time interval, amplitude, and sampling rate.

- `triangle_signal(freq, t0, t1, amp, fs)`  
  Creates a triangle waveform over a defined timebase.

Both functions return a NumPy array for time and the corresponding signal values.

### Time-Domain Operations

The project supports three types of time-domain manipulations:

- `time_shift(t, y, tau)`  
  Offsets a signal in time by `tau` seconds without altering its values.

- `time_scale(t, y, a, fill=0.0)`  
  Resamples the signal with a time scaling factor `a`. The `fill` argument defines values outside the interpolation range.

- `time_shift_and_scale(t, y, tau, a, fill=0.0)`  
  Applies both time shift and scaling using a combined affine transformation.

---

## Running the Code

The main script is `run.py`. This generates the signals, applies all transformations to them, and creates the plots.

To execute:

```bash
python run.py


## How to Test



This project includes a script found in `test.py`, which can be used to verify the correctness of all core functions.  



To run the tests use:



```bash

python test.py



this will give you an output that looks like:



!\[pytest output](pytest\_result.png)





## Requirements



This project requires the following Python packages:



\- numpy

\- matplotlib

\- math



If they are not already installed, you can install them using:



```bash

pip install numpy matplotlib math





## Project Structure



project-root/

├── README.md # Project documentation and usage guide

├── run.py # Main script: generates signals and saves plots

├── signals.py # Signal generation and time-domain transformation functions

├── test.py # Unit tests for verifying functionality

├── pyproject.toml # Dependency and project configuration

├── hello.py # Additional example or placeholder script

├── pytest-result.png # (Optional) Screenshot of successful test output

└── pycache/ # Automatically generated Python bytecode


---


