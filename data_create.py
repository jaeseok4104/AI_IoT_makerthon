import cv2
import numpy as np

cap = cv2.VideoCapture(2)
cap.set(3, 720)
cap.set(4, 1080)
num = 0
pos = './images/positive'
neg = './images/negetive'
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    k = cv2.waitKey(1)
    if k == ord('s'):
        images_dir = pos + str(num)+'.bmp'
        cv2.imwrite(images_dir, gray)
        num+=1
    if k == ord('d'):
        images_dir = neg + str(num)+'.bmp'
        cv2.imwrite(images_dir, gray)
        num+=1
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()