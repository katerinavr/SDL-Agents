# 100 µm × 100 µm area, 1 µm resolution, 0.01 s exposure
fly2d(zpy, -50, 50, 101,        # outer loop (Y): start, end, 101 points
      zpx, -50, 50, 100,        # inner loop (X): start, end, 100 points
      0.01)