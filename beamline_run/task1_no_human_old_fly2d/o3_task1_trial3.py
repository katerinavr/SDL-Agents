# Turn on the detectors you want recorded during the scan
detectors(['scaler', 'xrf'])        # modify this list if you need different detectors

# 100 µm range ⇒ −50 µm … +50 µm; step = 1 µm ⇒ 101 points per axis
# fly2d(motor1, start1, end1, npts1, motor2, start2, end2, npts2, exptime, absolute=False)
fly2d(zpy, -50, 50, 101,            # slow (outer) axis  – Y
      zpx, -50, 50, 101,            # fast (inner) axis – X
      0.01)                         # exposure time (s)