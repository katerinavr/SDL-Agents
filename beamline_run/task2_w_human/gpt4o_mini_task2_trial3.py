# image-explainer (to chat_manager):

# In the provided image, the bright spot is located at the coordinates approximately (0, -40) um in the zpx and zpy axes.

# To move the beam to this location, you should adjust the beam position to these coordinates:

# - **zpx (um): 0**
# - **zpy (um): -40**

# Make sure to confirm the movement and ensure the beam is accurately positioned at this point for further analysis.


# filename: move_beam_to_particle.py
import epics
import time
import datetime

# Define motors for moving the x-ray beam
zpx = epics.Device('26idcnpi:X_HYBRID_SP.', attrs=('VAL', 'DESC'))  # Define zpx motor
zpy = epics.Device('26idcnpi:Y_HYBRID_SP.', attrs=('VAL', 'DESC'))  # Define zpy motor

# Target positions
target_x = 0.0  # Target position for zpx in micrometers
target_y = -40.0  # Target position for zpy in micrometers

# Logbook path
logbook = "path_to_logbook.txt"  # Define the path to your logbook

def move_beam(target_x, target_y):
    # Move the beam to the target position
    try:
        # Move zpx and zpy motors
        epics.caput(zpx.NAME + '.VAL', target_x)  # Move zpx
        epics.caput(zpy.NAME + '.VAL', target_y)  # Move zpy
        time.sleep(1)  # Wait for the motors to reach the position

        # Log the movement
        with open(logbook, "a") as fp:
            fp.write(f'Moved beam to position: zpx = {target_x} um, zpy = {target_y} um at {datetime.datetime.now()}\n')

        print(f'Moved beam to position: zpx = {target_x} um, zpy = {target_y} um')
    except Exception as e:
        print(f"Error moving the beam: {e}")

# Execute the movement
move_beam(target_x, target_y)
