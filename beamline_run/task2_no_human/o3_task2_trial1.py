# image-explainer
# The isolated bright particle is located at approximately
# zpx = 0 µm, zpy = –39 µm  (±1 µm).

# Please move the beam to (0 µm, –39 µm).


# filename: move_beam_to_particle.py
import time

# (The objects mov, zpx, zpy are already defined in the running S26_commandline.py session)

# target coordinates (µm)
target_x = 0.0
target_y = -39.0

print("Moving beam to (zpx = {:.1f} µm, zpy = {:.1f} µm)…".format(target_x, target_y))
mov(zpx, target_x)
mov(zpy, target_y)

# Give EPICS a moment, then report final positions
time.sleep(1)
print("Done. Current beam position:")
print("   zpx = {:.1f} µm".format(zpx.RBV))
print("   zpy = {:.1f} µm".format(zpy.RBV))