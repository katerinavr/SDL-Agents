# Set up detectors
detectors(['scaler'])

# Set count time
count_time(0.01)

# Lock hybrid piezos
lock_hybrid()

# Execute 2D fly scan
# We'll use samx and samy for the scan, with a range of -50 to 50 (total 100 um) and 101 points (1 um resolution)
fly2d(samx, -50, 50, 101, samy, -50, 50, 101, 0.01)

# Print information about the scan
print(f"Starting 2D scan: 100 μm x 100 μm area, 1 μm resolution, 0.01 sec exposure time")
print(f"Estimated scan time: {101 * 101 * 0.01:.2f} seconds (excluding motor movements)")