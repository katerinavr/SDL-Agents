import epics
import time

# Define motors for moving the x-ray beam
zpx = epics.Device('26idcnpi:X_HYBRID_SP.', attrs=('VAL','DESC'))  # Motor for moving the x-ray beam in the x direction
zpx.add_pv('26idcnpi:m34.RBV', attr='RBV')  # Add readback PV

zpy = epics.Device('26idcnpi:Y_HYBRID_SP.', attrs=('VAL','DESC'))  # Motor for moving the x-ray beam in the y direction
zpy.add_pv('26idcnpi:m35.RBV', attr='RBV')  # Add readback PV

# Scan parameters
start_x = -50.0  # Start position in micrometers
end_x = 50.0     # End position in micrometers
num_pts_x = 101  # Number of points (100 micrometers / 1 micrometer resolution + 1)
start_y = -50.0  # Start position in micrometers
end_y = 50.0     # End position in micrometers
num_pts_y = 101  # Number of points (100 micrometers / 1 micrometer resolution + 1)
det_time = 0.01  # Exposure time in seconds

# Execute the scan
fly2d(zpx, start_x, end_x, num_pts_x, zpy, start_y, end_y, num_pts_y, det_time)