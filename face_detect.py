import sys
import numpy as np
import cv2


model = './data/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = './data/deploy.prototxt'
#model = 'opencv_face_detector/opencv_face_detector_uint8.pb'
#config = 'opencv_face_detector/opencv_face_detector.pbtxt'

eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')
eye_cascade1 = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
eye_cascade2 = cv2.CascadeClassifier('./data/haarcascade_lefteye_2splits.xml')
eye_cascade3 = cv2.CascadeClassifier('./data/haarcascade_righteye_2splits.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()

net = cv2.dnn.readNet(model, config)
if net.empty():
    print('Net open failed!')
    sys.exit()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not ret:
        break
    # frame = cv2.flip(frame,1)
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    out = net.forward()

    detect = out[0, 0, :, :]
    (h, w) = frame.shape[:2]
    op = 1
    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break
        op = 0
        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0, 255))
        h = y2 - y1
        w = x2 - x1
        x = x1
        y = y1
        roi_gray_left = gray[y:y+h, (int)(x+w/2):x+w]
        roi_gray_right = gray[y:y+h, x:x+(int)(w/2)]
        roi_color_left = frame[y:y+(int)(h/2)+20, x+(int)(w/2):x+w]
        roi_color_right = frame[y:y+(int)(h/2)+20, x:x+(int)(w/2)]
    if range(detect.shape[0])>0 :
        print('a')
        eye_left = eye_cascade2.detectMultiScale(roi_gray_left,1.3,5,minSize=(20,20))
        eye_right = eye_cascade3.detectMultiScale(roi_gray_right,1.3,5,minSize=(20,20))
        print(x,y,h,w)
        print(eye_left)
        print(eye_right)
        for(ex, ey, ew, eh) in eye_left:
            cv2.rectangle(roi_color_left,(ex,(int)(ey+ey/3)),(ex+ew,ey+eh),(0,255,0),2)
            roi_eye_left = roi_gray_left[ey+(int)(ey/3): ey+eh, ex:ex+ew]
        for(ex, ey, ew, eh) in eye_right:
            cv2.rectangle(roi_color_right,(ex,(int)(ey+ey/3)),(ex+ew,ey+eh),(0,255,0),2)
            roi_eye_right = roi_gray_right[ey+(int)(ey/3): ey+eh, ex:ex+ew]
    print('p')
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break


cv2.destroyAllWindows()