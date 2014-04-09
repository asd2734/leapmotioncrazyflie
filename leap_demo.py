# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2014 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

"""
Simple example that connects to the first Crazyflie found, ramps up/down
the motors and disconnects.
"""

import time, sys
from threading import Thread

#FIXME: Has to be launched from within the example folder
sys.path.append("../lib")
import cflib
from cflib.crazyflie import Crazyflie

import logging
logging.basicConfig(level=logging.ERROR)

import pygame
from pygame.locals import *


import sys
sys.path.append("../lib")


import time
from threading import Timer

import cflib.crtp
from cfclient.utils.logconfigreader import LogConfig
from cflib.crazyflie import Crazyflie

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

global datas
datas = ""


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
global pitch_init
global roll_init
global yaw_init
global thrust_init
global cal_done
global run_flag

last_fist_flag = False
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
cal_done = False
run_flag = True

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
        global leap_data
        global last_fist_flag
        global fist_flag
        global cal_flag 
        global cal_counter
        global pitch_cal_total
        global roll_cal_total
        global yaw_cal_total
        global thrust_cal_total
        global pitch_init
        global roll_init
        global yaw_init
        global thrust_init
        global cal_done
        
        leap_data = [0,0,0,0]
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            if cal_done == False:
                if not frame.hands.is_empty:
                    # Get the first hand
                    hand = frame.hands[0]
        
                    # Get the hand's normal vector and direction
                    normal = hand.palm_normal
                    direction = hand.direction

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
                                print "calibration done. pitch: %f degrees, roll: %f degrees, yaw: %f degrees, thrust: %f" % (
                            pitch_init, roll_init, yaw_init, thrust_init)
                                time.sleep(1)
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
            else: 
                
                # Calculate the hand's pitch, roll, and yaw angles
                
                leap_data[0] = direction.pitch * Leap.RAD_TO_DEG - pitch_init
                leap_data[1] = normal.roll * Leap.RAD_TO_DEG - roll_init
                leap_data[2] = direction.yaw * Leap.RAD_TO_DEG - yaw_init
                leap_data[3] = hand.stabilized_palm_position.y - thrust_init
                print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees, thrust: %f, fingers: %d" % (
                    leap_data[0],
                    leap_data[1],
                    leap_data[2], leap_data[3], len(frame.fingers))
                

            


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"




class LoggingExample:
     

    """
    Simple logging example class that logs the Stabilizer from a supplied
    link uri and disconnects after 5s.
    """
    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        # Create a Crazyflie object without specifying any cache dirs
        ''' self._cf = Crazyflie()

        # Connect some callbacks from the Crazyflie API
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        print "Connecting to %s" % link_uri

        # Try to connect to the Crazyflie
        self._cf.open_link("radio://0/2/250K")
        #self._cf.open_link("radio://0/8/250K")'''

        # Variable used to keep main loop occupied until disconnect
        self.is_connected = True
        Thread(target=self._ramp_motors).start()

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print "Connected to %s" % link_uri

        # The definition of the logconfig can be made before connecting
        '''self._lg_stab = LogConfig(name="Stabilizer", period_in_ms=10)
        self._lg_stab.add_variable("stabilizer.roll", "float")
        self._lg_stab.add_variable("stabilizer.pitch", "float")
        self._lg_stab.add_variable("stabilizer.yaw", "float")

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        self._cf.log.add_config(self._lg_stab)
        if self._lg_stab.valid:
            # This callback will receive the data
            self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
            # This callback will be called on errors
            self._lg_stab.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self._lg_stab.start()
        else:
            print("Could not add logconfig since some variables are not in TOC")'''
        
        

        # Start a timer to disconnect in 10s
        #t = Timer(5, self._cf.close_link)
        #t.start()

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print "Error when logging %s: %s" % (logconf.name, msg)

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from the log API when data arrives"""
        #print "[%d][%s]: %s" % (timestamp, logconf.name, data)
        global datas
        datas = str(data)
        #print datas
        

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)"""
        print "Connection to %s failed: %s" % (link_uri, msg)
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print "Connection to %s lost: %s" % (link_uri, msg)

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print "Disconnected from %s" % link_uri
        self.is_connected = False
        
    def _ramp_motors(self):
        time.sleep(0.1)
        global datas
        global leap_data
        global run_flag
        thrust_mult = 1
        thrust_step = 2000
        thrust = 10000
        pitch = 0
        del_pitch = 5
        roll = 0
        del_roll = 5
        yawrate = 0
        old_leap_data = [0,0,0,0]
        old_leap_data[0] = 0
        old_leap_data[1] = 0
        old_leap_data[2] = 0
        old_leap_data[3] = 0
        pygame.init()
        screen = pygame.display.set_mode((480*2, 360))
        name = ""
        font = pygame.font.Font(None, 50)
        while True:
            
            #print datas
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    
                    if evt.key == K_BACKSPACE:
                        name = name[:-1]
                    elif evt.key == K_RETURN:
                        name = ""
                    elif evt.key == K_LEFT:
                        
                        roll -= del_roll
                        #name = str(roll)
                    elif evt.key == K_RIGHT:
                        
                        roll += del_roll
                        #name = str(roll)
                    elif evt.key == K_DOWN:
                        
                        pitch -= del_pitch
                        #name = str(pitch)
                    elif evt.key == K_UP:
                         
                        pitch += del_pitch
                        #name = str(pitch) 
                    elif evt.key == K_w:
                        
                        thrust += thrust_step
                        #name = str(thrust)
                    elif evt.key == K_s:
                        
                        thrust -= thrust_step
                        #name = str(thrust)
                    elif evt.key == K_q:
                        run_flag = not run_flag

                        
                        
                    elif evt.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                elif evt.type == QUIT:
                    self._cf.commander.send_setpoint(0, 0, 0, 0)
                    time.sleep(0.1)
                    self._cf.close_link()
                    return
            
            if abs(leap_data[0]) > 10.0 and abs(leap_data[0])<60.0:
                pitch_com = -leap_data[0]/2.0
            elif leap_data[0] > 60.0:
                pitch_com = -20.0
            elif leap_data[0] < -60.0:
                pitch_com = 20.0
            else:
                pitch_com = 0
            
            if abs(leap_data[1]) > 10.0 and abs(leap_data[1])<60.0:
                roll_com  = -leap_data[1]/2.0
            elif leap_data[1]>60.0:
                roll_com = -20.0
            elif leap_data[1]<-60.0:
                roll_com = 20.0
            else:
                roll_com = 0

            if abs(pitch_com) < 10.0 and abs(roll_com) < 10.0 and abs(leap_data[2]) > 20:
                pitch_com = 0.0
                roll_com = 0.0
                yaw_com = leap_data[2]/5.0
            else:
                yaw_com = 0
            
            if leap_data[3] > 0 and leap_data[3] < 10:
               thrust_com = 10000 + leap_data[3] * 2000
            if leap_data[3] >=10 and leap_data[3] <=500:
                thrust_com = 30000 + leap_data[3] * 50
            elif leap_data[3] <= 0:
               thrust_com = 10000
            elif leap_data[3] > 1500:
                thrust_com = 10000
                
                
                
                
            pitch = (0.707*(roll_com + pitch_com))
            roll = (0.707*(roll_com - pitch_com))
            yawrate = yaw_com
            if run_flag:    
                thrust = thrust_com
            else:
                thrust = 10000
            #pitch = pitch_com
            #roll = roll_com
                
            name = "Pitch: " 
            name += str(int(pitch_com))
            name += ", Roll: "
            name += str(int(roll_com))
            name += ", Thrust: "
            name += str(int(thrust_com))
            name += ", Yawrate: "
            name += str(int(yaw_com))
            name += ", Live: "
            name += str(run_flag)
            
            screen.fill ((0, 0, 0))
            block = font.render(name, True, (255, 255, 255))
            rect = block.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(block, rect)
            pygame.display.flip()
            if thrust < 10001:
                thrust = 10000
            elif thrust > 60000:
                thrust = 60000
            #self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
            time.sleep(0.1)







        
if __name__ == '__main__':

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found

    available = "aaa"

            # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

        # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    if len(available) > 0:
        le = LoggingExample(available[0][0])
    else:
        print "No Crazyflies found, cannot run example"