# Ensure motors are initialized and ready
# Check if zpx and zpy are locked or require setup

# Execute a 2D scan with the specified parameters
fly2d(motor1=zpx, startpos1=0, endpos1=100, numpts1=100,
      motor2=zpy, startpos2=0, endpos2=100, numpts2=100,
      dettime=0.01, absolute=True)

# Ensure prescan and postscan functions are called within fly2d or manually