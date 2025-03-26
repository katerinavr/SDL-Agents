# filename: move_substrate_to_rack.py
import loca
import robotics as ro

# Initialize the robot controller
c9 = ro.system.init('controller')

# Pick up the substrate using the Bernoulli substrate gripper tool
c9.tool = 'substrate_tool'  # Ensure this is the correct tool identifier
c9.set_output('substrate_tool', True)  # Activate the vacuum to pick up the substrate

# Move the substrate to the substrate rack location [0,0]
try:
    c9.position = loca.substrate_rack_seq[0, 0]  # Ensure correct indexing and data structure
except Exception as e:
    print(f"Error moving to substrate rack location: {e}")

# Place the substrate in the designated position
c9.set_output('substrate_tool', False)  # Deactivate the vacuum to release the substrate
c9.tool = None  # Drop off the tool in the gripper