# In the provided image, the bright spot is located at the coordinates approximately (0, -40) um in the zpx and zpy axes.

# To move the beam to this location, you should adjust the beam position to these coordinates:

# - **zpx (um): 0**
# - **zpy (um): -40**

# Make sure to confirm the movement and ensure the beam is accurately positioned at this point for further analysis.

# filename: move_beam.py
import epics
import time

# Define motors
zpx = epics.Device('26idcnpi:X_HYBRID_SP.', attrs=('VAL','DESC'))
zpy = epics.Device('26idcnpi:Y_HYBRID_SP.', attrs=('VAL','DESC'))

# Move the beam to the specified coordinates
def move_beam(zpx_position, zpy_position):
    epics.caput(zpx.NAME + '.VAL', zpx_position)
    time.sleep(1)  # Wait for the motor to move
    epics.caput(zpy.NAME + '.VAL', zpy_position)
    time.sleep(1)  # Wait for the motor to move

    # Confirm the new positions
    new_zpx = epics.caget(zpx.NAME + '.VAL')
    new_zpy = epics.caget(zpy.NAME + '.VAL')
    print(f"Beam moved to zpx: {new_zpx} um, zpy: {new_zpy} um")

# Move to the desired position
move_beam(0, -40)