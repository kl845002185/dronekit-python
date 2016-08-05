from dronekit import connect

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('/dev/tty.usbmodem1', wait_ready=True, baud=57600)

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable

vehicle.close()