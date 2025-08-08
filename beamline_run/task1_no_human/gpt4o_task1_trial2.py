# Define the scan parameters
startpos1 = 0.0  # Start position for x direction
endpos1 = 100.0  # End position for x direction
numpts1 = 101    # Number of points in x direction

startpos2 = 0.0  # Start position for y direction
endpos2 = 100.0  # End position for y direction
numpts2 = 101    # Number of points in y direction

dettime = 0.01   # Exposure time in seconds

# Execute the 2D scan
try:
    fly2d(zpx, startpos1, endpos1, numpts1, zpy, startpos2, endpos2, numpts2, dettime, absolute=True)
except Exception as e:
    print(f"An error occurred during the scan: {e}")