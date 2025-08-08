# filename: move_polymer_A_to_clamp.py

import loca
import robotics as ro
from robotics import procedure as proc

# Constants
VERTICAL_MOVE_DISTANCE = 5000  # 5 cm in robot units
VERTICAL_MOVE_VELOCITY = 15000

# Initialize the robot controller
c9 = ro.system.init('controller')

try:
    # Step 1: Find the rack index for polymer_A
    vial_index = proc.find_rack_index('vial', 'polymer_A')
    print(f"Vial index for polymer_A: {vial_index}")

    # Step 2: Move the robot arm to the vial position
    c9.position = loca.vial_rack[vial_index]
    print("Moved to vial position")

    # Step 3: Pick up the vial using the gripper
    c9.set_output('gripper', True)
    print("Gripper closed")

    # Step 4: Move the vial to the clamp position
    c9.move_axis('z', 0, vel=VERTICAL_MOVE_VELOCITY)  # Move up to avoid collisions
    print("Moved up")
    c9.position = loca.clamp
    print("Moved to clamp position")

    # Step 5: Place the vial in the clamp and secure it
    c9.set_output('clamp', False)  # Open the clamp
    print("Clamp opened")
    c9.move_axis('z', c9.position[3] - VERTICAL_MOVE_DISTANCE, vel=VERTICAL_MOVE_VELOCITY)  # Move down
    print("Moved down")
    c9.set_output('gripper', False)  # Release the vial
    print("Gripper opened")
    c9.move_axis('z', c9.position[3] + 1000, vel=VERTICAL_MOVE_VELOCITY)  # Move up slightly
    print("Moved up slightly")
    c9.set_output('clamp', True)  # Close the clamp
    print("Clamp closed")

    # TODO: Add confirmation step to verify vial placement

    print("PEDOT:PSS (polymer_A) vial has been successfully moved to the clamp holder.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # TODO: Add error handling and recovery procedures

finally:
    # Ensure the robot is in a safe position
    c9.move_axis('z', 0, vel=VERTICAL_MOVE_VELOCITY)
