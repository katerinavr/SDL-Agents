# Update scan parameters for higher resolution
start_pos = -25  # Scan a smaller 50x50 µm area
end_pos = 25
num_points = 251  # 0.2 µm steps
exposure_time = 0.05  # Longer exposure for better signal

# Perform the high-resolution 2D fly scan
fly2d(outer_motor, start_pos, end_pos, num_points,
      inner_motor, start_pos, end_pos, num_points,
      exposure_time, absolute=False)