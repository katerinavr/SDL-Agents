# image-explainer (to chat_manager):

# In the provided image, the bright spot is located at the coordinates approximately (0, -40) um in the zpx and zpy axes.

# To move the beam to this location, you should adjust the beam position to these coordinates:

# - **zpx (um): 0**
# - **zpy (um): -40**

# Make sure to confirm the movement and ensure the beam is accurately positioned at this point for further analysis.


# filename: move_beam_to_particle.py
import time
import datetime

# Target positions
target_x = 0.0  # Target position for zpx in micrometers
target_y = -40.0  # Target position for zpy in micrometers

# Move the beam to the target position using the mov function
mov(zpx, target_x)  # Move zpx
mov(zpy, target_y)  # Move zpy

# Log the movement
logbook = "path_to_logbook.txt"  # Define the path to your logbook
with open(logbook, "a") as fp:
    fp.write(f'Moved beam to position: zpx = {target_x} um, zpy = {target_y} um at {datetime.datetime.now()}\n')

print(f'Moved beam to position: zpx = {target_x} um, zpy = {target_y} um')