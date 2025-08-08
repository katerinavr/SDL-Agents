# The location of this bright spot (particle) appears to be at approximately:

# x = 0 µm
# y = -38 µm

# To move the beam to this location, you should adjust the beam position to these coordinates. The precision of this measurement is on the order of 1 µm, as requested.

# This isolated bright spot is ideal for further analysis as it's clearly distinguishable from the background and doesn't appear to be part of a larger cluster. The brightness of this spot suggests it could provide good data for subsequent measurements.

# Remember, this single bright spot represents a particle that is diffracting under the current conditions. Other particles may be present but not visible if they're not satisfying the diffraction condition.

# Is there anything else you'd like to know about this image or the particle location?

# Move the beam to the coordinates of the particle
mov(zpx, 0)  # Move X coordinate to 0
mov(zpy, -38)  # Move Y coordinate to -38 µm

# Wait for the movement to complete
while zpx.moving or zpy.moving:
    time.sleep(0.1)

# Check if the movement was successful
if abs(zpx.RBV - 0) < 0.1 and abs(zpy.RBV - (-38)) < 0.1:
    print(f"Beam successfully moved to coordinates: X = {zpx.RBV}, Y = {zpy.RBV}")
else:
    print(f"Warning: Beam may not have reached the exact coordinates. Current position: X = {zpx.RBV}, Y = {zpy.RBV}")