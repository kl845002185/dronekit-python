# Author: Yikai Wang
# Date: Aug 2016
# Function: This class is used for basic motion control and motion memorizing.
# Email: kl845002185@gmail.com

from dronekit import connect, VehicleMode
import time


class MotionControl:
    def __init__(self, vehicle):
        self.motion_stack = []  # Used to memorize the motions of bluerov
        # Channel 3, 4, 6, 7 are for basic motions control.
        # The region of channel 3, 4, 6, 7 is [1100, 1900]. 1500 is the center value(corresponding motor is still).
        self.DEFAULT_CHANNEL_OVERRIDES = {
            '1': 1500, '2': 1500, '3': 1500, '4': 1500,
            '5': 1100, '6': 1500, '7': 1500, '8': 1500
        }  
        """
        channels[0] = 1500 + pitchTrim;                           // pitch
        channels[1] = 1500 + rollTrim;                            // roll
        channels[2] = constrain_int16((z+zTrim)*throttleScale+throttleBase,1100,1900);  // throttle
        channels[3] = constrain_int16(r*rpyScale+rpyCenter,1100,1900);                       // yaw
        channels[4] = mode;                                       // for testing only
        channels[5] = constrain_int16((x+xTrim)*rpyScale+rpyCenter,1100,1900);           // forward for ROV
        channels[6] = constrain_int16((y+yTrim)*rpyScale+rpyCenter,1100,1900);           // lateral for ROV
        channels[7] = camTilt;                                    // camera tilt
        channels[8] = lights1;                                    // lights 1
        channels[9] = lights2;                                    // lights 2
        channels[10] = video_switch;                              // video switch
        """
        # Initialze the channel values to the default values.
        vehicle.channels.overrides = self.DEFAULT_CHANNEL_OVERRIDES  
        self.in_recall = False  # When the vehicle is in the recall state, set it to True.

    # Arm bluerov after calling the MotionControl class
    @staticmethod
    def arm(vehicle, mode_string):  
        print "Arming motors"
        vehicle.armed = True
        vehicle.mode = VehicleMode(mode_string)
        print " Armed: %s" % vehicle.armed

    # Set the vehicle channels to the initial values so that all the motors stop spinning.
    def stop(self, vehicle, *arg):
        # __temp is the element of the motion_stack.
        __temp = {
            'Motion Name': 'Stop',
            'Speed(%)': 1500,
            'Duration(s)': 0
        }
        # print(__temp)
        if not self.in_recall:
            self.motion_stack.append(__temp)
        vehicle.channels.overrides = self.DEFAULT_CHANNEL_OVERRIDES

    def yaw(self, vehicle, speed, duration):  # Positive speed is yaw right
        __temp = {
            'Motion Name': 'Yaw',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        # Convert the speed region from [-100, 100] to [1100, 1900]
        speed = speed * 4 + 1500
        if duration < 0:
            duration = 0
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['6'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Yaw speed region is [-100, 100]")

    def throttle(self, vehicle, speed, duration):  # Positive speed is throttle forward
        __temp = {
            'Motion Name': 'Throttle',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        speed = speed * 4 + 1500
        speed = 3000 - speed # Reverse the control direction due to the channel calibration
        if duration < 0:
            duration = 0
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['4'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Throttle speed region is [-100, 100]")

    def strafe(self, vehicle, speed, duration):  # Positive speed is strafe right
        __temp = {
            'Motion Name': 'Strafe',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        if duration < 0:
            duration = 0
        speed = speed * 4 + 1500
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['7'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Strafe speed region is [-100, 100]")

    def pitch(self, vehicle, speed, duration):  # Positive speed is pitch ascend
        __temp = {
            'Motion Name': 'Pitch',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        if duration < 0:
            duration = 0
        speed = speed * 4 + 1500
        if (1100 <= speed <= 1900):
            print(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['3'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Pitch speed region is [-100, 100]")

    # Traceback. Let bluerov return to the home position.
    def motions_recall(self, vehicle, motion_stack):
        self.in_recall = True
        print("Recalling")
        __get_motion = {
            'Stop': self.stop,
            'Yaw': self.yaw,
            'Throttle': self.throttle,
            'Strafe': self.strafe,
        }
        while len(motion_stack):
            last_motion = motion_stack[-1]
            # You need to use speed_coef like this because the motion of opposite direction is not accuately symmetric.
            if last_motion['Motion Name'] == 'Yaw':
                if last_motion['Speed(%)'] > 0: 
                    speed_coef = 1.5
                else:
                    speed_coef = 0.667
            else:
                speed_coef = 1
            __get_motion.get(last_motion['Motion Name'], self.stop)\
                (vehicle, -last_motion['Speed(%)'] * speed_coef, last_motion['Duration(s)'])
            motion_stack.pop()
        self.in_recall = False

