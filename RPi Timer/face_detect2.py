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
import paho.mqtt.client as mqtt
import pymysql
import sys

model = '/home/pi/opencv/DNN/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = '/home/pi/opencv/DNN/deploy.prototxt'

def light_removing(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    L = lab[:,:,0]
    med_L = cv2.medianBlur(L,99)
    invert_L = cv2.bitwise_not(med_L)
    composed = cv2.addWeighted(gray, 0.75, invert_L, 0.25, 0)
    return L, composed

def select_alarm(result):
    if result == 1:
        sound_alarm("ALARM.wav")

def sound_alarm(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

thresh = 0.3
frame_check = 10

ALARM_ON = False

print("[INFO] loading facial landmark predictor...")
detector = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("[INFO] starting video stream thread...")

cap = cv2.VideoCapture(-1)
flag=0
time.sleep(1.0)


if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()
    
net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    sys.exit()
    
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frame = imutils.resize(frame, width=450)
    L, gray = light_removing(frame)
    
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5, minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(rects) <= 0:
        blob = cv2.dnn.blobFromImage(frame,1,(300,300),(104,177,123))
        net.setInput(blob)
        out = net.forward()
        detect = out[0,0, :, :]
        (hei, wei) = frame.shape[:2]
    
        for i in range(detect.shape[0]):
            confidence = detect[i, 2]
            if confidence < 0.5:
                break
            # face detect fail -> timer stop -> sleep
            # timer stop code
            
            # face detect success -> timer restart -> studying
            # timer start code
            x1 = int(detect[i, 3] * wei)
            y1 = int(detect[i, 4] * hei)
            x2 = int(detect[i, 5] * wei)
            y2 = int(detect[i, 6] * hei)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,0,255))
            
            label = f'Face: {confidence:4.2f}'
            cv2.putText(frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),1,cv2.LINE_AA)
    
    # face detect success -> timer restart -> studying
    # timer start code
    for (x, y, w, h) in rects:

        rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0))
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        
        ear = (leftEAR + rightEAR) / 2.0
        
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0,255,0), 1)
        cv2.drawContours(
            frame, [rightEyeHull], -1, (0,255,0), 1)
        if ear < thresh:
            flag += 1
            print(flag)
            
            if flag >= frame_check:
                
                t = Thread(target = select_alarm, args = (1, ))
                t.deamon =True
                t.start()
                
                cv2.putText(frame, "**ALERT!**", (10,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255), 2)
            
        else:
            flag = 0
            ALARM_ON = False
    
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()

