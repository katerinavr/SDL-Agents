# Define the motors for the scan
motor1 = zpx  # Motor for x-direction
motor2 = zpy  # Motor for y-direction

# Define the scan parameters
startpos1 = 0.0  # Start position for motor1 (x-direction)
endpos1 = 100.0  # End position for motor1 (x-direction)
numpts1 = 100    # Number of points for motor1

startpos2 = 0.0  # Start position for motor2 (y-direction)
endpos2 = 100.0  # End position for motor2 (y-direction)
numpts2 = 100    # Number of points for motor2

dettime = 0.01   # Exposure time in seconds

# Print the scan setup
print(f"Motor1 (x-direction): Start = {startpos1}, End = {endpos1}, Points = {numpts1}")
print(f"Motor2 (y-direction): Start = {startpos2}, End = {endpos2}, Points = {numpts2}")

# Execute the scan
fly2d(motor1, startpos1, endpos1, numpts1, motor2, startpos2, endpos2, numpts2, dettime)