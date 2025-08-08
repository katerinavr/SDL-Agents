# filename: flyscan_100x100um.py
# 100 µm × 100 µm scan, 1 µm resolution, 0.01 s exposure

# 1. Select detectors (add/remove entries as desired)
detectors(['scaler'])          # examples: ['scaler','xrf'] or ['xrf','pilatus']

# 2. Run the 2-D fly scan
#    motor1 = zpy (outer loop, stepped) : −50 µm → +50 µm in 101 points  (1 µm steps)
#    motor2 = zpx (inner loop, fly)    : −50 µm → +50 µm in 100 intervals (≈1 µm resolution)
#    exposure time per point = 0.01 s
fly2d(zpy, -50, 50, 101,
      zpx, -50, 50, 100,
      0.01,
      absolute=False)          # leave “absolute” False for relative scan around current centre

print("Fly-scan started: 100 µm × 100 µm, 1 µm resolution, 0.01 s exposure.")