# Best candidate:

# • zpx ≈ –42 µm
# • zpy ≈ +46 µm
# (precision ±1 µm)

# Why this point?

# 1. Nano-diffraction image: the brightest, most concentrated diffraction spot sits at (–40 to –43 µm, +44 to +47 µm).
# 2. Nano-fluorescence image: the same coordinate lies in a comparatively dark region, far from the extended >10 µm bright clusters found around (0 µm, –15 µm) and (+30 µm, +25 µm). This indicates an isolated, single particle rather than a thick aggregate.

# Action:

# • Move the X-ray beam to (zpx, zpy) = (–42 µm, +46 µm).
# • Once centred, begin the detailed diffraction/fluorescence measurement on this single particle.

# filename: move_to_isolated_particle.py
# Move the HXN nano-beam to the isolated particle identified in scan 160

# 1. Send the beam
mov(zpx, -42)     # X direction  (outboard = +)
mov(zpy,  46)     # Y direction  (up     = +)

# 2. Verify the final position
print(f"zpx = {zpx.RBV:.2f} µm,  zpy = {zpy.RBV:.2f} µm")