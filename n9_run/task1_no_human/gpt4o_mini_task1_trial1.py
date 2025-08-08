# filename: move_vial_to_clamp.py
import loca
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import time  # Import time for delays

def move_vial_to_clamp(polymer_label='polymer_A'):
    # Initialize the robot controller
    c9 = ro.system.init('controller')

    # Step 1: Find the index of the vial containing polymer A
    vial_index = proc.find_rack_index('vial', polymer_label)

    # Check if the vial index is valid
    if vial_index is None:
        print(f"Error: Vial with label '{polymer_label}' not found.")
        return

    # Step 2: Move to the vial position
    c9.position = loca.vial_rack[vial_index]

    # Step 3: Close the gripper to pick up the vial
    c9.set_output('gripper', True)
    time.sleep(1)  # Wait for the gripper to close

    # Step 4: Move to the clamp holder position
    c9.position = loca.clamp

    # Step 5: Open the gripper to release the vial into the clamp holder
    c9.set_output('gripper', False)
    time.sleep(1)  # Wait for the gripper to open

# Execute the function
move_vial_to_clamp()
