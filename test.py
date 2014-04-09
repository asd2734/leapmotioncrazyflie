################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

global leap_data
global last_fist_flag
global fist_flag
global cal_flag 
global cal_counter
global pitch_cal_total
global roll_cal_total
global yaw_cal_total
global thrust_cal_total
global cal_done


last_fist_flag = False
fist_flag = False
cal_flag = False
cal_counter = 0
pitch_cal_total = 0.0
roll_cal_total = 0.0
yaw_cal_total = 0.0
thrust_cal_total = 0.0
cal_done = False

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        
        print "Connected"

        # Enable gestures

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global last_fist_flag
        global fist_flag
        global cal_flag 
        global cal_counter
        global pitch_cal_total
        global roll_cal_total
        global yaw_cal_total
        global thrust_cal_total
        global cal_done
        
        leap_data = [0,0,0]
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        '''last_fist_flag = False
        fist_flag = False
        cal_flag = False
        cal_counter = 0
        pitch_cal_total = 0.0
        roll_cal_total = 0.0
        yaw_cal_total = 0.0
        thrust_cal_total = 0.0
        pitch_init = 0.0
        roll_init = 0.0
        yaw_init = 0.0
        thrust_init = 0.0
        pitch_leap = 0.0
        roll_leap = 0.0
        yaw_leap = 0.0
        thrust_leap = 0.0'''

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            
            # Setpoint to Crazyflie
            '''self.cf_commander.send_setpoint(
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)'''
            
            
            # Calculate the hand's pitch, roll, and yaw angles
            #print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees, fingers: %d" % (
            #    direction.pitch * Leap.RAD_TO_DEG,
            #    normal.roll * Leap.RAD_TO_DEG,
            #    direction.yaw * Leap.RAD_TO_DEG, len(frame.fingers))
            '''leap_data[0] = direction.pitch * Leap.RAD_TO_DEG
            leap_data[1] = normal.roll * Leap.RAD_TO_DEG
            leap_data[2] = direction.yaw * Leap.RAD_TO_DEG'''
            pitch_leap = direction.pitch * Leap.RAD_TO_DEG
            roll_leap = normal.roll * Leap.RAD_TO_DEG
            yaw_leap = direction.yaw * Leap.RAD_TO_DEG
            thrust_leap = hand.stabilized_palm_position.y
            
            finger_num = len(frame.fingers)
            roll_degree = normal.roll * Leap.RAD_TO_DEG
            if not (frame.hands.is_empty and frame.gestures().is_empty):
                if (finger_num <= 1 and abs(roll_degree) < 50):
                    fist_flag = True
                    
                else:
                    fist_flag = False
                    
                    
            if (last_fist_flag) and (not fist_flag):
                cal_flag = True
            if (cal_flag and cal_done == 0):
                if (not fist_flag):
                    if cal_counter == 0:
                        print "calibrating..."
                        
                    if (cal_counter <= 200):
                        cal_counter += 1
                        pitch_cal_total += pitch_leap
                        roll_cal_total += roll_leap
                        yaw_cal_total += yaw_leap
                        thrust_cal_total += thrust_leap
                    else:
                        cal_flag = False
                        cal_counter = 0
                        pitch_init = pitch_cal_total/200
                        roll_init = roll_cal_total/200
                        yaw_init = yaw_cal_total/200
                        thrust_init = thrust_cal_total/200
                        pitch_cal_total = 0
                        roll_cal_total = 0
                        yaw_cal_total = 0
                        thrust_cal_total = 0
                        cal_done = True
                        print "calibration done. pitch: %f degrees, roll: %f degrees, yaw: %f degrees, y position: %f millimeters" % (
                    pitch_init, roll_init, yaw_init, thrust_init)
                else:
                    print "calibration interrupted. Please try again"
                    cal_flag = False
                    cal_counter = 0
                    pitch_cal_total = 0
                    roll_cal_total = 0
                    yaw_cal_total = 0
                    thrust_cal_total = 0
                
            last_fist_flag = fist_flag                  
        else:
            fist_flag = False

            # Gestures
            


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    
    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
