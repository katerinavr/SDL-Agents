# Execute the scan
fly2d(zpx, -50, 50, 101, zpy, -50, 50, 101, 0.01, absolute=False)

# Wait for the scan to complete
while sc2.BUSY == 1:
    time.sleep(1)

print("Scan complete. Verifying results...")

# Verify scan completion and gather information
scan_number = epics.caget(scanrecord+':saveData_scanNumber', as_string=True)
pathname = epics.caget(scanrecord+':saveData_fullPathName', as_string=True)

print(f"Scan #{scan_number} completed.")
print(f"Data saved in: {pathname}")

# Check if Medipix was one of the detectors used
if 'medipix' in dets_list:
    medipix_path = pathname[:-4] + 'Images/' + scan_number + '/'
    print(f"Medipix images saved in: {medipix_path}")

# Check if Pilatus was one of the detectors used
if 'pilatus' in dets_list:
    pilatus_path = '/home/det/s26data/' + pathname[15:-4] + 'Images/' + scan_number + '/'
    print(f"Pilatus images saved in: {pilatus_path}")

# Suggest next steps
print("\nNext steps:")
print("1. Check the logbook for detailed scan information.")
print("2. Analyze the saved data using your preferred data analysis tools.")
print("3. If you need to visualize the scan results, consider using plotting libraries like matplotlib or specialized X-ray data analysis software.")
print("4. To perform any post-processing or data conversion, you may need to write additional Python scripts or use existing data processing pipelines.")

print("\nDo you want to perform any specific analysis or visualization of the scan results?")