import loca
import robotics as ro
from robotics import procedure as proc

# Constants
VERTICAL_MOVE_DISTANCE = 5000
MOVE_VELOCITY = 15000

# Initialize the robot controller
c9 = ro.system.init('controller')

try:
    # Find the rack index for polymer_A
    vial_index = proc.find_rack_index('vial', 'polymer_A')
    if vial_index is None:
        raise ValueError("Vial for polymer_A not found in the rack")

    # Move the robot arm to the vial position
    c9.position = loca.vial_rack[vial_index]

    # Pick up the vial using the gripper
    c9.set_output('gripper', True)
    if not c9.get_input('gripper_closed'):
        raise RuntimeError("Failed to close gripper")

    # Move the arm up slightly to safely remove the vial from the rack
    c9.move_axis('z', c9.position[3] - VERTICAL_MOVE_DISTANCE, vel=MOVE_VELOCITY)

    # Move the vial to the clamp position
    c9.position = loca.clamp

    # Place the vial in the clamp
    c9.set_output('clamp', False)
    if not c9.get_input('clamp_open'):
        raise RuntimeError("Failed to open clamp")

    c9.move_axis('z', c9.position[3] + VERTICAL_MOVE_DISTANCE, vel=MOVE_VELOCITY)
    c9.set_output('clamp', True)
    if not c9.get_input('clamp_closed'):
        raise RuntimeError("Failed to close clamp")

    # Release the vial
    c9.set_output('gripper', False)
    if not c9.get_input('gripper_open'):
        raise RuntimeError("Failed to open gripper")

    # Move the arm up slightly
    c9.move_axis('z', c9.position[3] - VERTICAL_MOVE_DISTANCE, vel=MOVE_VELOCITY)

    print("PEDOT:PSS (polymer_A) vial has been successfully moved to the clamp holder.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Add any necessary error handling or recovery procedures here
