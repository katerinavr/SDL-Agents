# filename: return_gripper_to_start.py
import loca
import robotics as ro

# Initialize the robot controller
c9 = ro.system.init('controller')
# c9.set_output('substrate_tool', False) 
# c9.set_output('coater_stage_vacuum', False)
# c9.set_output('gripper', False)
# c9.home_robot()
# Return the gripper to its starting position
c9.position = [0, 0, 0, 0]  # Move robot arm to the initial location