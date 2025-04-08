# filename: move_vial_to_clamp.py
import robotics as ro
from robotics import procedure as proc
from lab_setup import rack_status

# Initialize the robot controller
controller = ro.system.init('controller')

# Access the rack status to find the location of the vial
vial_rack = rack_status.get('vial', {})

# Identify the location of the vial with PEDOT:PSS
sol_label = 'PEDOT:PSS'
vial_index = proc.find_rack_index('vial', sol_label)

if vial_index is not None:
    # Move the robot arm to the vial's location
    controller.position = vial_rack[vial_index]

    # Use the gripper to pick up the vial
    controller.set_output('gripper', True)

    # Move the robot arm to the clamp location
    controller.position = loca.clamp

    # Place the vial in the clamp
    controller.set_output('gripper', False)
else:
    print("Vial with PEDOT:PSS not found in the rack.")