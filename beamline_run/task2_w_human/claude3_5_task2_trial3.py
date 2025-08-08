# Based on the nano-diffraction image provided, I can see a single bright spot which likely corresponds to a particle that diffracts at this particular diffraction condition. This is exactly what we're looking for in a nano-diffraction image.

# The location of this bright spot (particle) appears to be at approximately:

# x = 0 µm
# y = -38 µm

# To move the beam to this location, you should adjust the beam position to these coordinates. The precision of this measurement is on the order of 1 µm, as requested.

# This isolated bright spot is ideal for further analysis as it's clearly distinguishable from the background and doesn't appear to be part of a larger cluster. The brightness of this spot suggests it could provide good data for subsequent measurements.

# Remember, this single bright spot represents a particle that is diffracting under the current conditions. Other particles may be present but not visible if they're not satisfying the diffraction condition.


# Move the beam to the absolute coordinates of the particle
mov(zpx, 0)
mov(zpy, -38)

time.sleep(1)  # Wait for the movement to complete

print(f"Beam moved to coordinates: X = {zpx.RBV}, Y = {zpy.RBV}")

# Perform a fine 2D scan around the particle
scan_range = 2.5  # μm
num_points = 21  # This will give us a step size of 0.25 μm

fly2d(zpx, -scan_range, scan_range, num_points,
      zpy, -scan_range, scan_range, num_points,
      dettime=0.5, absolute=False)

print("Fine scan completed. Please analyze the results to confirm the exact particle location.")