def main():
    # 1) Choose detector(s)  ------------------------------------------------
    detectors(['scaler'])          # use scaler for quick fluorescence count

    # 2) Configure and start scan  -----------------------------------------
    fly2d(
        zpy, -50.0,  50.0, 101,    # outer loop: Y from −50 µm to +50 µm in 1 µm steps
        zpx, -50.0,  50.0, 101,    # inner loop: X from −50 µm to +50 µm in 1 µm steps
        0.01                       # exposure time per point [s]
        # default absolute=False -> positions are relative to current motor positions
    )

if __name__ == '__main__':
    main()