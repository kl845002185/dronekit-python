from dronekit import connect, VehicleMode
vehicle = connect('/dev/ttyACM0', wait_ready=True)

vehicle.mode = VehicleMode("LAND")
