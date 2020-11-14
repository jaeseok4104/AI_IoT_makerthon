import sys
import numpy as np
import cv2
import time
#from matplotlib import pyplot as plt

model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'
#model = 'opencv_face_detector/opencv_face_detector_uint8.pb'
#config = 'opencv_face_detector/opencv_face_detector.pbtxt'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()

net = cv2.dnn.readNet(model, config)
eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')
if net.empty():
    print('Net open failed!')
    sys.exit()


while True:
    ret, frame = cap.read()
   
    if not ret:
        break
    
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    out = net.forward()

    detect = out[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0, 255))
        
        label = f'Face: {confidence:4.2f}'
        cv2.putText(frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        
        
        face_hei = int(y2 - y1)
        face_wei = int(x2 - x1)
        img = frame[y1:int(y1+(face_hei*2/3)),x1:x2]

        eyecenter = int(x1 + face_wei/2)
        

        eyes = eye_classifier.detectMultiScale(img,1.1,5,None,None,(60,60))
        time.sleep(0.5)
        for (x2, y2, w2, h2) in eyes:
            if x2 < eyecenter:
                left_frame = img[y2+int(h2/4):y2+h2,x2:x2+w2]
                gray_frame = cv2.cvtColor(left_frame,cv2.COLOR_BGR2GRAY)
                dy = cv2.Sobel(gray_frame,-1,0,1)
                _,dst = cv2.threshold(dy, 150, 255, cv2.THRESH_BINARY)
                count = 0
                for x in range(dst.shape[1]):
                            for y in range(dst.shape[0]):
                                if dst[y][x] == 255:
                                    count = count + 1
                print(count)  
                # dst2 = np.zeros(Lab_planes[0].shape, np.uint8)

        
                # bw = Lab_planes[0].shape[1] // 2
                # bh = Lab_planes[0].shape[0] // 2
                # for y in range(2):
                #     for x in range(2):
                #         src_ = Lab_planes[0][y*bh:(y+1)*bh, x*bw:(x+1)*bw]
                #         dst_ = dst2[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
                #         cv2.threshold(src_, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU, dst_)
    
    
    cv2.imshow('dy',dy)
    cv2.imshow('dst',dst)
    cv2.imshow('left',left_frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

        