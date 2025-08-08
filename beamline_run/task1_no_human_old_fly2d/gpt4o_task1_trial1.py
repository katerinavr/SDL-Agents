# Ensure the motors are correctly configured and ready for scanning
# Perform a 2D scan with the specified parameters
fly2d(zpx, 0, 100, 101, zpy, 0, 100, 101, 0.01, absolute=True)
