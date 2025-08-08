# filename: find_best_location.py
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load images
diffraction_image_path = 'C:/Users/kvriz/Desktop/SDL-Agents/figure160.png'
fluorescence_image_path = 'C:/Users/kvriz/Desktop/SDL-Agents/scan160_xrf.png'

# Read images
diffraction_image = cv2.imread(diffraction_image_path, cv2.IMREAD_GRAYSCALE)
fluorescence_image = cv2.imread(fluorescence_image_path, cv2.IMREAD_GRAYSCALE)

# Find the brightest spot in the diffraction image
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(diffraction_image)

# Check if the brightest spot is isolated in the fluorescence image
x, y = max_loc
is_isolated = True  # Placeholder for isolation check

# Define a region around the brightest spot to check for isolation
check_radius = 5
for i in range(-check_radius, check_radius + 1):
    for j in range(-check_radius, check_radius + 1):
        if (0 <= x + i < fluorescence_image.shape[1]) and (0 <= y + j < fluorescence_image.shape[0]):
            if fluorescence_image[y + j, x + i] > 0:  # Assuming non-zero indicates presence of other particles
                is_isolated = False
                break
    if not is_isolated:
        break

# Output results
if is_isolated:
    print(f"Best location found at coordinates: {max_loc}")
    # Move the beam to this location (you would replace this with your actual move command)
    # Example: mov(zpx, max_loc[0])
    # Example: mov(zpy, max_loc[1])
else:
    print("No isolated particle found at the brightest spot.")

# Optionally display the images
plt.subplot(1, 2, 1)
plt.title('Nano-Diffraction Image')
plt.imshow(diffraction_image, cmap='gray')
plt.scatter(max_loc[0], max_loc[1], color='red')  # Mark the brightest spot
plt.subplot(1, 2, 2)
plt.title('Nano-Fluorescence Image')
plt.imshow(fluorescence_image, cmap='gray')
plt.show()