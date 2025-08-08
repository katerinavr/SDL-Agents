# filename: find_best_particle.py
import cv2
import numpy as np
import epics

# Load images
diffraction_image_path = r"C:\Users\kvriz\Desktop\SDL-Agents\figure160.png"
fluorescence_image_path = r"C:\Users\kvriz\Desktop\SDL-Agents\scan160_xrf.png"

# Read images
diffraction_image = cv2.imread(diffraction_image_path, cv2.IMREAD_GRAYSCALE)
fluorescence_image = cv2.imread(fluorescence_image_path, cv2.IMREAD_GRAYSCALE)

# Find the brightest spot in the diffraction image
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(diffraction_image)

# Check if the brightest spot is isolated in the fluorescence image
x, y = max_loc
is_isolated = True

# Define a small region around the brightest spot to check for isolation
check_radius = 5
for i in range(-check_radius, check_radius + 1):
    for j in range(-check_radius, check_radius + 1):
        if (0 <= x + i < fluorescence_image.shape[1]) and (0 <= y + j < fluorescence_image.shape[0]):
            if fluorescence_image[y + j, x + i] > 50:  # Threshold for isolation
                is_isolated = False
                break
    if not is_isolated:
        break

# Move the beam if the spot is isolated
if is_isolated:
    print(f"Best location found at: {max_loc}")
    # Move the beam to the identified coordinates
    zpx = epics.Motor('26idcnpi:X_HYBRID_SP.')
    zpy = epics.Motor('26idcnpi:Y_HYBRID_SP.')
    zpx.move(max_loc[0], wait=True)
    zpy.move(max_loc[1], wait=True)
else:
    print("The best-diffracting particle is not isolated.")