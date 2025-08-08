# Inspection of the two images gives three obvious diffraction spots (bright pixels in the nano-diffraction map):

# 1) zpx ≈ –42 µm , zpy ≈ +46 µm
# 2) zpx ≈ +27 µm , zpy ≈ +18 µm
# 3) zpx ≈  +5 µm , zpy ≈ –18 µm

# Cross–checking these positions on the nano-fluorescence image:

# •  Position 2 and Position 3 fall in the middle of bright 10 × 10 µm (or larger) fluorescence patches, indicating particle clusters – these should be avoided.  
# •  Position 1 sits in a much darker fluorescence region, well away from any extended bright patch, so the particle there is most likely isolated.

# Recommended target

# zpx = –42 µm
# zpy = +46 µm
# (accuracy ±1 µm)

# Please move the beam to (–42, +46) µm to probe this single, strongly-diffracting, isolated particle.

# move_to_strong_iso_particle.py
import time          # approved standard library

# zpx, zpy motor objects and mov() helper are already defined
target_zpx = -42.0   # µm
target_zpy =  46.0   # µm

print(f"Current beam position (µm): zpx = {zpx.RBV:.2f},  zpy = {zpy.RBV:.2f}")

mov(zpx, target_zpx)          # safe, logged move
mov(zpy, target_zpy)

time.sleep(1.0)               # let the piezos settle

print(f"New beam position (µm):     zpx = {zpx.RBV:.2f},  zpy = {zpy.RBV:.2f}")
print("Beam is now centred on the isolated, strongly-diffracting particle.")