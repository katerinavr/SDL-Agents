try:
    fly2d(samx, -50, 50, 101, samy, -50, 50, 101, 0.01)
    print("Scan completed successfully. Please check the saved data.")
except Exception as e:
    print(f"An error occurred during the scan: {e}")