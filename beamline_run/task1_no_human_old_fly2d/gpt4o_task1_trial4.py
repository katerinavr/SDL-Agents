# Define the parameters for the scan
startpos1 = 0  # Start position for motor1 (x-axis)
endpos1 = 100  # End position for motor1 (x-axis)
numpts1 = 101  # Number of points for motor1 (1 micrometer resolution)

startpos2 = 0  # Start position for motor2 (y-axis)
endpos2 = 100  # End position for motor2 (y-axis)
numpts2 = 101  # Number of points for motor2 (1 micrometer resolution)

dettime = 0.01  # Exposure time in seconds

# Execute the 2D scan
fly2d(zpx, startpos1, endpos1, numpts1, zpy, startpos2, endpos2, numpts2, dettime, absolute=False)