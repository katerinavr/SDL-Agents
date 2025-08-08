# filename: move_beam.py
import epics
import time

# Define the target coordinates
target_x = 30  # in µm
target_y = 30  # in µm

# Move the beam to the target coordinates
mov(zpx, target_x)  # Move in the x direction
mov(zpy, target_y)  # Move in the y direction