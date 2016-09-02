# Author: Yikai Wang
# Date: Aug 2016
# Function: Add listener to some attributes
# Email: kl845002185@gmail.com

from dronekit import connect, VehicleMode  # Needed for basic connection of mode setting
import sys
import time
import threading
import urllib2
from pymavlink import mavutil


# TASK: Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Basic motion test for the BLueROV. ')
parser.add_argument('--connect',
					help="""Vehicle connection target string. 
					If not specified, SITL automatically started and used.""")
args = parser.parse_args()

connection_string = args.connect
sitl = None
connection_to_vehicle = True  # If you want to use simulator instead of real test, just change this to False.

connection = False
index = '0'
connection_string = '/dev/ttyACM'  


# Connection parts is introduced in motion_test.py
if not connection_to_vehicle:
	import dronekit_sitl
	sitl = dronekit_sitl.start_default()
	connection_string = sitl.connection_string()
	vehicle = connect(connection_string, wait_ready = True)
else:
	while not connection:  # Use try and except, because the name of the USB connection file may change.
		try:
			vehicle = connect(connection_string + index, wait_ready = True)
			print ("Connect to " + connection_string + index)
			connection = True
		except:
			print ("Cannot connect to " + connection_string + index)
			index = str(int(index) + 1)
		# If you still cannot find the file after 10 trials, there's something wrong with the pixhawk connection.
		if index.__len__() >= 2:             
			exit()

# vehicle = connect('192.168.2.2:14555', wait_ready = True)  # This is for UDP connection.
mode_string = "ALT_HOLD"  # There are "MANUAL", "STABILIZE" and "ALT_HOLD" there modes available.
vehicle.mode = VehicleMode(mode_string)


#Create a message listener for all messages.
@vehicle.on_message('*')
def listener(self, name, message):
	print 'message: %s' % message

# You can use this for listening to the channel values.
@vehicle.on_message('ATTITUDE')
def attitude_listener(self, name, msg):
	print '---%s' % (msg)
	time.sleep(3)
	
# Other listeners available:	
"""
@self.on_message('GLOBAL_POSITION_INT')
@self.on_message('ATTITUDE')
@self.on_message('VFR_HUD')
@self.on_message('RANGEFINDER')
@self.on_message('MOUNT_STATUS')
@self.on_message('AUTOPILOT_VERSION')
@self.on_message('RC_CHANNELS_RAW')
@self.on_message('SYS_STATUS')
@self.on_message('GPS_RAW_INT')
@self.on_message(['WAYPOINT_CURRENT', 'MISSION_CURRENT'])
@self.on_message('EKF_STATUS_REPORT')
@self.on_message('HEARTBEAT')
@self.on_message(['WAYPOINT_COUNT', 'MISSION_COUNT'])
@self.on_message(['HOME_POSITION'])
@self.on_message(['WAYPOINT', 'MISSION_ITEM'])
@self.on_message(['WAYPOINT_REQUEST', 'MISSION_REQUEST'])
@self.on_message(['PARAM_VALUE'])
"""	
	
time.sleep(120)

vehicle.close()
print "Finished all the tasks"
