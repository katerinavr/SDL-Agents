# filename: scan_100um_square.py
#
# 100 µm × 100 µm fly-scan, 1 µm step, 0.01 s dwell.
# Outer loop: Y (zpy), inner loop: X (zpx)

# -----------------------------------------------------------------
# 1. Choose the detectors you want to gate during the scan
#    (modify the list if you need additional detectors).
detectors(['scaler', 'xrf'])

# 2. Define scan parameters
step_size     = 1        # µm
half_range    = 50       # ±50 µm gives 100 µm full width
num_pts_axis  = int((2*half_range)/step_size) + 1   # 101 points
exposure_time = 0.01     # seconds per point

# 3. Launch the 2-D fly scan
fly2d(
    zpy, -half_range, +half_range, num_pts_axis,   # outer (Y) loop
    zpx, -half_range, +half_range, num_pts_axis,   # inner (X) loop
    exposure_time                                  # dwell
)