# Import necessary libraries
import epics
import time

# Assuming zpx and zpy are already defined as motors for x and y directions
# Perform the 2D scan
fly2d(motor1=zpx, startpos1=0, endpos1=100, numpts1=101,
      motor2=zpy, startpos2=0, endpos2=100, numpts2=101,
      dettime=0.01, absolute=True)