# Update scan parameters
start_pos = -25  # Reduce scan range to 50x50 µm
end_pos = 25
num_points = 126  # Increase resolution to 0.4 µm steps

# Perform the new 2D fly scan
fly2d(outer_motor, start_pos, end_pos, num_points,
        inner_motor, start_pos, end_pos, num_points,
        exposure_time, absolute=False)