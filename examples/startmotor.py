#edited mn
from dronekit import connect, VehicleMode
import sys
import time

# Connect to UDP endpoint (and wait for default attributes to accumulate)
target = sys.argv[1] if len(sys.argv) >= 2 else 'udpin:0.0.0.0:14550'
print 'Connecting to ' + target + '...'
vehicle = connect('/dev/ttyACM0', wait_ready=True)

# Get all vehicle attributes (state)
print "Vehicle state:"
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
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

vehicle.mode = VehicleMode("ALT_HOLD")

print "Arming motors"
vehicle.armed = True
print vehicle.armed
'''
# Get all original channel values (before override)
print "Channel values from RC Tx:", vehicle.channels
vehicle.channels.overrides = {}
# Access channels individually
print "Read 8 channels individually:"
print " Ch1: %s" % vehicle.channels['1']
print " Ch2: %s" % vehicle.channels['2']
print " Ch3: %s" % vehicle.channels['3']
print " Ch4: %s" % vehicle.channels['4']
print " Ch5: %s" % vehicle.channels['5']
print " Ch6: %s" % vehicle.channels['6']
print " Ch7: %s" % vehicle.channels['7']
print " Ch8: %s" % vehicle.channels['8']
print "Number of channels: %s" % len(vehicle.channels)

print " Ch4: %s" % vehicle.channels['3']
vehicle.channels.overrides['3'] = 10
vehicle.flush()
print "should be running"
time.sleep(1);
vehicle.channels.overrides['3'] = None
vehicle.flush()
'''

# vehicle.close()
print "Done."
