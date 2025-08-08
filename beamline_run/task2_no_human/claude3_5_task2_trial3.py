# The location of this bright spot (particle) appears to be at approximately:

# x = 0 µm
# y = -38 µm

# To move the beam to this location, you should adjust the beam position to these coordinates. The precision of this measurement is on the order of 1 µm, as requested.

# Move the beam to the particle location
movr(zpx, 0)  # X position doesn't need to change
movr(zpy, -38)  # Move Y position by -38 µm

# Verify the new position
print(f"New X position: {zpx.RBV}")
print(f"New Y position: {zpy.RBV}")

# Perform a fine 2D scan around the particle
fly2d(zpx, -2.5, 2.5, 11, zpy, -2.5, 2.5, 11, 0.5)