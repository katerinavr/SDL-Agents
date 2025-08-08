# Ensure that the scanrecord and logbook variables are defined
scanrecord = '26idbSOFT:scan1'  # Example scan record, replace with the correct one if different
logbook = 'scan_log.txt'  # Example logbook file, replace with the correct one if different

# Define the parameters for the scan
startpos1 = 0
endpos1 = 100
numpts1 = 101
startpos2 = 0
endpos2 = 100
numpts2 = 101
dettime = 0.01

# Perform the 2D scan
fly2d(zpx, startpos1, endpos1, numpts1, zpy, startpos2, endpos2, numpts2, dettime)