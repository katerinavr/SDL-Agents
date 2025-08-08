# The strongest isolated diffraction spot is located at approximately
# • zpx ≈ 0 µm
# • zpy ≈ –39 µm

# Please move the beam to (0 µm, –39 µm) with ±1 µm precision to centre it on this particle.

# Move the beam to the bright-spot location and verify the final position
target_zpx = 0.0     # µm
target_zpy = -39.0   # µm
tolerance  = 1.0     # µm

# 1) Move
mov(zpx, target_zpx)
mov(zpy, target_zpy)

# 2) Confirm
err_x = abs(zpx.RBV - target_zpx)
err_y = abs(zpy.RBV - target_zpy)

print(f"\nRequested   : zpx = {target_zpx:.1f} µm, zpy = {target_zpy:.1f} µm")
print(f"Readback    : zpx = {zpx.RBV:.2f} µm, zpy = {zpy.RBV:.2f} µm")
print(f"Deviation   : Δx  = {err_x:.2f} µm, Δy  = {err_y:.2f} µm")

if err_x <= tolerance and err_y <= tolerance:
    print("✅  Beam is centred on the particle within ±1 µm.")
else:
    print("⚠️  Beam is not yet within tolerance—tweak further if necessary.")