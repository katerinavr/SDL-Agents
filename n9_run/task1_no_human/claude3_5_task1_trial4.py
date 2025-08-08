import robotics as ro
from robotics import procedure as proc
import loca

# Constants
Z_CLEARANCE = 5000
MOVE_VELOCITY = 15000

# Initialize the robot controller
c9 = ro.system.init('controller')

try:
    # Step 1: Find the rack index for polymer A
    vial_index = proc.find_rack_index('vial', 'polymer_A')
    if vial_index is None:
        raise ValueError("Polymer A vial not found in the rack")

    # Step 2: Move the robot arm to the vial rack position for polymer A
    c9.position = loca.vial_rack[vial_index]

    # Step 3: Pick up the vial using the gripper
    c9.set_output('gripper', True)  # Close the gripper to grab the vial

    # Safety check: Ensure the vial is grasped
    if not c9.get_input('gripper_closed'):
        raise RuntimeError("Failed to grasp the vial")

    # Move the arm up slightly to clear the rack
    c9.move_axis('z', c9.position[3] - Z_CLEARANCE, vel=MOVE_VELOCITY)

    # Step 4: Move the vial to the clamp location
    c9.position = loca.clamp

    # Step 5: Place the vial in the clamp
    c9.set_output('clamp', False)  # Open the clamp
    c9.set_output('gripper', False)  # Open the gripper to release the vial
    c9.set_output('clamp', True)  # Close the clamp to secure the vial

    # Safety check: Ensure the clamp is closed
    if not c9.get_input('clamp_closed'):
        raise RuntimeError("Failed to secure the vial in the clamp")

    # Move the arm up slightly to clear the clamp
    c9.move_axis('z', c9.position[3] - Z_CLEARANCE, vel=MOVE_VELOCITY)

    print("Vial with polymer A has been successfully moved to the clamp location.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Implement appropriate error handling procedures here

finally:
    # Ensure the gripper is opened and the arm is in a safe position
    c9.set_output('gripper', False)
    c9.position = loca.safe_position  # Assuming there's a defined safe position
