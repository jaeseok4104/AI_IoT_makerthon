from tkinter import *
from PIL import Image
from PIL import ImageTk
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance
from threading import Thread
import pyglet
import numpy as np
import imutils
import time
import dlib
import cv2
import pygame
import argparse
#import paho.mqtt.client as mqtt
#import pymysql
import sys



class Camera(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.btn_frame = Frame(self)
        self.label_frame = Frame(self)
        self.btn_frame.grid(row=2,column = 0)
        self.label_frame.grid(row=3,column = 0)
        self.mainFrame = Frame(self)
        self.mainFrame.grid(row=0, column=0)
        self.lmain =Label(self.mainFrame)
        self.lmain.grid(row=0, column=0)  
        self.cap = cv2.VideoCapture(0)
        self.model = 'opencv_face_detector_uint8.pb'
        self.config = 'opencv_face_detector.pbtxt'
        self.net = cv2.dnn.readNet(self.model, self.config)
        self.thresh = 0.3
        self.frame_check = 10
        self.ALARM_ON = False
        self.sec = 0
        ret, self.frame = self.cap.read()
        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.flag=0
        
        self.controller = controller
        self.mode = "STOP"
        self.draw_frame()
        
    
    def dnn(self):
        opencv_frame = imutils.resize(self.frame, width=320)
        L, gray = self.light_removing(opencv_frame)
    
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5, minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    
        if len(rects) <= 0:
            blob = cv2.dnn.blobFromImage(opencv_frame,1,(300,300),(104,177,123))
            self.net.setInput(blob)
            out = self.net.forward()
            detect = out[0,0, :, :]
            (hei, wei) = opencv_frame.shape[:2]
        
            for i in range(detect.shape[0]):
                confidence = detect[i, 2]
                if i == 0:
                    if confidence < 0.5:
                        self.mode = "PAUSE"
                        break
                    elif confidence >= 0.5:
                        x1 = int(detect[i, 3] * wei)
                        y1 = int(detect[i, 4] * hei)
                        x2 = int(detect[i, 5] * wei)
                        y2 = int(detect[i, 6] * hei)
                        cv2.rectangle(opencv_frame, (x1,y1),(x2,y2),(0,0,255))
                        
                        label = f'Face: {confidence:4.2f}'
                        cv2.putText(opencv_frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),1,cv2.LINE_AA)
                        self.mode = "RUNNING"
                        
                        
                if i == 1:
                    if confidence >= 0.5:
                        x1 = int(detect[i, 3] * wei)
                        y1 = int(detect[i, 4] * hei)
                        x2 = int(detect[i, 5] * wei)
                        y2 = int(detect[i, 6] * hei)
                        cv2.rectangle(opencv_frame, (x1,y1),(x2,y2),(0,0,255))
                        
                        label = f'Face: {confidence:4.2f}'
                        cv2.putText(opencv_frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),1,cv2.LINE_AA)
                    elif confidence < 0.5:
                        break

        # face detect success -> timer restart -> studying
        # timer start code
        elif len(rects) > 0:
            self.mode = "RUNNING"
            
            for (x, y, w, h) in rects:

                rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
                cv2.rectangle(opencv_frame, (x,y),(x+w,y+h),(0,255,0))
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                leftEye = shape[self.lStart:self.lEnd]
                rightEye = shape[self.rStart:self.rEnd]
                leftEAR = self.eye_aspect_ratio(leftEye)
                rightEAR = self.eye_aspect_ratio(rightEye)
                
                ear = (leftEAR + rightEAR) / 2.0
                
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(opencv_frame, [leftEyeHull], -1, (0,255,0), 1)
                cv2.drawContours(
                    opencv_frame, [rightEyeHull], -1, (0,255,0), 1)
                if ear < self.thresh:
                    self.flag += 1
                    print(self.flag)
                    
                    if self.flag >= self.frame_check:
                        
                        t = Thread(target = self.select_alarm, args = (1, ))
                        t.deamon =True
                        t.start()
                        self.mode="PAUSE"
                        
                        cv2.putText(opencv_frame, "**ALERT!**", (10,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255), 2)
                    
                else:
                    self.flag = 0
                    self.ALARM_ON = False
        return
    
    '''
    def show_frame(self):
        ret, self.frame = self.cap.read()
        re_dnn_frame = self.dnn()
        
        cv2image   = cv2.cvtColor(re_dnn_frame, cv2.COLOR_BGR2RGBA)

        img   = Image.fromarray(cv2image).resize((760, 400))
        imgtk = ImageTk.PhotoImage(image = img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)
    '''
    
    def light_removing(self,frame):
        rem_frame = frame
        gray = cv2.cvtColor(rem_frame, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(rem_frame, cv2.COLOR_BGR2LAB)
        L = lab[:,:,0]
        med_L = cv2.medianBlur(L,99)
        invert_L = cv2.bitwise_not(med_L)
        composed = cv2.addWeighted(gray, 0.75, invert_L, 0.25, 0)
        return L, composed

    def select_alarm(self,result):
        if result == 1:
            sound_alarm("music\ALARM.wav")

    def sound_alarm(self,path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
            
    def eye_aspect_ratio(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear



    def draw_frame(self):    
        self.btn_control=Button(self.btn_frame,text="start",font=("Helvetica",10),command = self.change_control)
        self.btn_reset=Button(self.btn_frame,text="reset",font=("Helvetica",10),command = self.time_reset)
        btn_back=Button(self.btn_frame,text="back",font=("Helvetica",10),command=lambda:self.controller.show_frame("mainmenu"))
        self.label_time=Label(self.label_frame,text="00:00:00",font=("Helvetica",40))
        
        self.label_time.grid(row=0,column=1)
        self.btn_control.grid(row=2,column=0)
        self.btn_reset.grid(row=2,column=1)
        btn_back.grid(row=5,column=0)

    
    
    def change_control(self):
        if self.mode == "STOP":
            self.mode = "RUNNING"
            print(self.mode)
            self.stopwatch_start()
            #self.show_frame()
            self.dnn()
        elif self.mode == "RUNNING":
            self.mode = "PAUSE"
            print(self.mode)
        elif self.mode == "PAUSE":
            self.mode = "RUNNING"
            print(self.mode)
        self.change_button()
    
    def change_button(self):
        if self.mode == "STOP":
            self.btn_control.config(text="start")
        elif self.mode == "RUNNING":
            self.btn_control.config(text="pause")
        elif self.mode == "PAUSE":
            self.btn_control.config(text="resume")
    
    def stopwatch_start(self):
        self.stopwatch_loop()
    
    def stopwatch_loop(self):
        hour , second = divmod(self.sec,3600)
        minute , second = divmod(second,60)

        if self.mode == "RUNNING":
            new_time = "{:02}:{:02}:{:02}".format(hour, minute, second)
            self.sec += 1
            self.label_time.config(text=new_time)
           
        elif self.mode == "STOP":
            return
        self.label_time.after(1000,self.stopwatch_loop)
        

        
    def time_reset(self):
        self.mode = "STOP"
        self.label_time.config(text="00:00:00")
        self.change_button()
    
        
