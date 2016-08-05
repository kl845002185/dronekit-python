from dronekit import connect, VehicleMode
import sys
import time
import urllib2


# Connect to UDP endpoint (and wait for default attributes to accumulate)

vehicle = connect('/dev/ttyACM0', wait_ready = True)
#vehicle = connect('/dev/tty.usbmodem1')
vehicle.mode = VehicleMode("ALT_HOLD")

# Get all vehicle attributes (state)
print "Vehicle state:"
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Heading: %s" % vehicle.heading
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Mode: %s" % vehicle.mode.name
print " Is Armable?: %s" % vehicle.is_armable
print " Armed: %s" % vehicle.armed

print "Arming motors"
vehicle.armed = True
print vehicle.armed

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(10)

#Confirm vehicle armed before attempting to take off
while (not vehicle.armed):
    print " Waiting for arming..."
    time.sleep(1)



vehicle.close()
print "Done."
