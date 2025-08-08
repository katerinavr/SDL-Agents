# In the provided scan, there is a bright spot located at approximately the coordinates (0, -40) um in the zpx and zpy axes. This is where the particle is likely located.

# To move the beam towards this location, adjust the beam position to (0, -40) um. This should allow for further analysis of the particle at that specific coordinate.


# filename: move_beam.py
import epics
import time

# Define motors for beam movement
zpx = epics.Device('26idcnpi:X_HYBRID_SP.', attrs=('VAL','DESC'))  # X direction
zpy = epics.Device('26idcnpi:Y_HYBRID_SP.', attrs=('VAL','DESC'))  # Y direction

def mov(motor, position):
    # Move motor to absolute position defined by the 2nd argument.
    motor.VAL = position
    time.sleep(1)
    print(motor.DESC + " ---> " + str(motor.RBV))

# Move the beam to the specified coordinates
mov(zpx, 0)    # Move in the x direction
mov(zpy, -40)  # Move in the y direction