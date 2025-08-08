# In the provided image, the bright spot is located at the coordinates approximately (0, -40) um in the zpx and zpy axes.

# To move the beam to this location, you should adjust the beam position to these coordinates:

# - **zpx (um): 0**
# - **zpy (um): -40**

# Make sure to confirm the movement and ensure the beam is accurately positioned at this point for further analysis.

# filename: move_beam.py
import epics
import time

# Assuming the motors are already defined in the main script
# Use the existing motors defined in the provided code

def move_beam_to_particle():
    # Move the beam to the specified coordinates (0, -40) um
    mov(zpx, 0)    # Move in the x direction
    mov(zpy, -40)  # Move in the y direction

# Execute the movement
move_beam_to_particle()