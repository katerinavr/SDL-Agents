# filename: move_polymer_A_to_clamp.py
import loca  # Ensure this module is correctly implemented
import robotics as ro
from robotics import procedure as proc

# Initialize the robot controller
c9 = ro.system.init('controller')

try:
    # Find the index of polymer A in the vial rack
    vial_index = proc.find_rack_index('vial', 'polymer_A')

    # Move the robot arm to the location of polymer A
    c9.position = loca.vial_rack[vial_index]

    # Use the gripper to pick up the vial
    c9.set_output('gripper', True)

    # Move the robot arm to the clamp location
    c9.position = loca.clamp

    # Place the vial in the clamp
    c9.set_output('clamp', True)
    c9.set_output('gripper', False)

except Exception as e:
    print(f"An error occurred: {e}")
