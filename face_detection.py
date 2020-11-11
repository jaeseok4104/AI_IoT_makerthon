import cv2
# import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 1080)
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
face_cascade1 = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
face_cascade2 = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt2.xml')
face_cascade3 = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt_tree.xml')
face_cascade4 = cv2.CascadeClassifier('./data/haarcascade_frontalface_smile.xml')
face_cascade5 = cv2.CascadeClassifier('./data/haarcascade_profileface.xml')
# face_cascade = cv2.CascadeClassifier('./data/output.xml')
eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')
eye_cascade1 = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
eye_cascade2 = cv2.CascadeClassifier('./data/haarcascade_lefteye_2splits.xml')
eye_cascade3 = cv2.CascadeClassifier('./data/haarcascade_righteye_2splits.xml')

pos = './images/positive'
neg = './images/negetive'
num = 0
not_detect = 0
op = 0
eye_left = ()
eye_right = ()
def eye_detection () :
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+(h/2), x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)
    for(ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if (ret):
        faces = face_cascade2.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
        if (faces == ()):
            not_detect = 0
            faces = face_cascade5.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
            if (faces != ()) :
                not_detect = 1
        else : 
            not_detect = 1
        if (not_detect != 0) :    
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray_left = gray[y:y+h, x+w/2:x+w]
                roi_gray_right = gray[y:y+h, x:x+w/2]
                roi_color_left = frame[y:y+(h/2)+20, x+w/2:x+w]
                roi_color_right = frame[y:y+(h/2)+20, x:x+w/2]

                eye_left = eye_cascade2.detectMultiScale(roi_gray_left,1.3,5,minSize=(20,20))
                eye_right = eye_cascade3.detectMultiScale(roi_gray_right,1.3,5,minSize=(20,20))

                for(ex, ey, ew, eh) in eye_left:
                    cv2.rectangle(roi_color_left,(ex,ey+ey/3),(ex+ew,ey+eh),(0,255,0),2)
                    roi_eye_left = roi_gray_left[ey+ey/3: ey+eh, ex:ex+ew]
                for(ex, ey, ew, eh) in eye_right:
                    cv2.rectangle(roi_color_right,(ex,ey+ey/3),(ex+ew,ey+eh),(0,255,0),2)
                    roi_eye_right = roi_gray_right[ey+ey/3: ey+eh, ex:ex+ew]

    gray_canny = gray.copy()
    gray_ret, gray_canny_binary = cv2.threshold(gray_canny, 50,255, cv2.THRESH_OTSU) 
    gray_canny = cv2.Canny(gray_canny, 70, 150)
    
    if (not_detect!=1) :
        if (eye_left != ()) :
            roi_eye_left_canny = roi_eye_left.copy()
            roi_eye_left_canny_ret, roi_eye_left_canny_b = cv2.threshold(roi_eye_left_canny, 50,255, cv2.THRESH_OTSU) 
            roi_eye_left_canny_e = cv2.Canny(roi_eye_left_canny_b, 70, 150)            
            cv2.imshow('roi_eye_left_canny', roi_eye_left_canny_e)
        if (eye_right != ()) :
            roi_eye_right_canny = roi_eye_right.copy()
            roi_eye_right_canny_ret, roi_eye_right_canny_b = cv2.threshold(roi_eye_right_canny, 50,255, cv2.THRESH_OTSU) 
            roi_eye_right_canny_e = cv2.Canny(roi_eye_right_canny_b, 70, 150)
            cv2.imshow('roi_eye_right_canny', roi_eye_right_canny_e)



    cv2.imshow('gray_canny_binary', gray_canny_binary)
    cv2.imshow('gray_canny', gray_canny)
    cv2.imshow('face_detection(frame)', frame)
    k = cv2.waitKey(1)
    if k == ord('s'):
        images_dir = pos + str(num)+'.bmp'
        cv2.imwrite(images_dir, frame)
        num+=1
    if k == ord('d'):
        images_dir = neg + str(num)+'.bmp'
        cv2.imwrite(images_dir, frame)
        num+=1
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()