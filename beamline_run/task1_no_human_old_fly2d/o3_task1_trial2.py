# Scan 100 µm × 100 µm area with 1 µm resolution, 0.01 s exposure
# Outer loop  (slow): zpy  –50 µm → +50 µm   (101 lines)
# Inner loop (fast): zpx  –50 µm → +50 µm   (101 points per line)

fly2d(
    zpy, -50, 50, 101,   # slow axis (Y), start, end, number of points
    zpx, -50, 50, 101,   # fast axis (X), start, end, number of points
    0.01                 # exposure time (s)
)