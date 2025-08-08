# Set up scan parameters
motor1 = zpx  # X-direction motor
motor2 = zpy  # Y-direction motor
startpos1 = -50  # Start position for X (μm)
endpos1 = 50     # End position for X (μm)
numpts1 = 101    # Number of points in X direction (100 μm / 1 μm resolution + 1)
startpos2 = -50  # Start position for Y (μm)
endpos2 = 50     # End position for Y (μm)
numpts2 = 101    # Number of points in Y direction (100 μm / 1 μm resolution + 1)
dettime = 0.01   # Exposure time (seconds)

# Execute the scan
fly2d(motor1, startpos1, endpos1, numpts1, motor2, startpos2, endpos2, numpts2, dettime, absolute=False)

# Check if the scan is complete
print("Scan complete. Check the results.")