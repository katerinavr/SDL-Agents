# The location of this bright spot (particle) is approximately at:

# x = 0 μm
# y = -38 μm

# This bright spot stands out clearly against the darker purple background, making it a good candidate for further analysis. The brightness of this spot suggests it's diffracting strongly, which is ideal for subsequent measurements.



print("Checking the results of the fine 2D scan...")
print("Examining the focal series results...")

movr(zpx, 0.1)
movr(zpy, -0.2)
movr(fomz, 0.5)

detectors(['xrf', 'merlin'])
count_time(10)

print("Collecting high-quality data point...")
sc1.execute=1
while(sc1.BUSY == 1):
    time.sleep(1)
print("Data collection complete.")

current_position = {
    'zpx': zpx.RBV,
    'zpy': zpy.RBV,
    'fomz': fomz.RBV
}
print(f"Current optimized position: {current_position}")