# In the provided nano-diffraction image, the bright spots appear to be located at the following coordinates:

# 1. **(x, y) = (20, 20) µm**
# 2. **(x, y) = (-30, 30) µm**

# Among these, the one at **(20, 20) µm** appears to be more isolated compared to the others.

# You should move the beam towards the coordinates **(20, 20) µm** for further analysis.

# filename: move_beam.py
import epics
import time

# Define the target coordinates
target_x = 20  # in µm
target_y = 20  # in µm

# Move the beam to the target coordinates
mov(zpx, target_x)  # Move in the x direction
mov(zpy, target_y)  # Move in the y direction
