# filename: move_vial_to_clamp.py
import loca
import robotics as ro
from robotics import procedure as proc
import time

def move_vial_to_clamp():
    # Initialize the robot controller
    c9 = ro.system.init('controller')

    # Define the polymer label
    polymer_label = 'polymer_A'

    # Find the index of the vial containing polymer A
    vial_index = proc.find_rack_index('vial', polymer_label)
    if vial_index is None:
        print("Error: Vial containing polymer A not found.")
        return

    # Move the robot arm to the vial position
    c9.position = loca.vial_rack[vial_index]

    # Close the gripper to pick up the vial
    c9.set_output('gripper', True)
    time.sleep(1)  # Wait for the gripper to close

    # Move the robot arm to the clamp holder position
    c9.position = loca.clamp

    # Open the gripper to release the vial into the clamp holder
    c9.set_output('gripper', False)
    time.sleep(1)  # Wait for the gripper to open
    time.sleep(1)  # Wait for the gripper to open

if __name__ == "__main__":
    move_vial_to_clamp()
