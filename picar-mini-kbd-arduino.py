#!/usr/bin/python
import os
import time
import atexit
import serial
import cv2
import math
import numpy as np
import pygame

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vidfile = cv2.VideoWriter('out-video.avi', fourcc, 20.0, (320,240))
keyfile = open('out-key.csv', 'w+')
keyfile_btn = open('out-key-btn.csv', 'w+')
keyfile.write("ts_micro,frame,wheel\n")
keyfile_btn.write("ts_micro,frame,btn,speed\n")
rec_start_time = 0

def stop():
        ser.write("s\n")
def ffw():
        ser.write("f\n")
def rew():
        ser.write("b\n")

def center():
        ser.write("c\n")
def left():
        ser.write("l\n")
def right():
        ser.write("r\n")

def degree2rad(deg):
        return deg * math.pi / 180.0

def turnOff():
        stop()
        center()

atexit.register(turnOff)

view_video = False
frame_id = 0
null_frame = np.zeros((160,120,3), np.uint8)
cv2.imshow('frame', null_frame)

angle = 0.0
btn = ''

while (True):
        # read a frame
        ret, frame = cap.read()
        ts = int(time.time() * 1000000)
        
        if ret == False:
		print "Camera is not ready"
                break

        if view_video == True:
                cv2.imshow('frame', frame)

        ch = cv2.waitKey(50) & 0xFF

        if ch == ord('j'):
                left()
                print "left"
                angle = degree2rad(-30)
                btn   = ch
        elif ch == ord('k'):
                center()
                print "center"
                angle = degree2rad(0)
                btn   = ch                
        elif ch == ord('l'):
                right()
                print "right"
                angle = degree2rad(30)
                btn   = ch                
        elif ch == ord('a'):
                ffw()
                print "accel"
        elif ch == ord('s'):
                stop()
                print "stop"                
                btn   = ch
        elif ch == ord('z'):
                rew()
                print "reverse"
        elif ch == ord('q'):
                break
	elif ch == ord('r'):
                print "toggle record mode"
                if rec_start_time == 0:
                        rec_start_time = ts
                else:
                        rec_start_time = 0
        elif ch == ord('t'):
                print "toggle video mode"
                if view_video == False:
                        view_video = True
                else:
                        view_video = False
		
                        
        if rec_start_time > 0:
                # increase frame_id
                frame_id = frame_id + 1
                
                # write input (angle)
                str = "{},{},{}\n".format(ts, frame_id, angle)
                keyfile.write(str)

                # write input (button: left, center, stop, speed)
                str = "{},{},{},{}\n".format(ts, frame_id, btn, cur_speed)
                keyfile_btn.write(str)
                
                # write video stream
                vidfile.write(frame)

	        print ts, frame_id, angle, btn

cap.release()
keyfile.close()
keyfile_btn.close()
vidfile.release()
