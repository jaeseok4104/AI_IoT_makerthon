import sys
import numpy as np
import cv2
import pymysql
import time


model = './data/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = './data/deploy.prototxt'

eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')
eye_cascade1 = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
eye_cascade2 = cv2.CascadeClassifier('./data/haarcascade_lefteye_2splits.xml')
eye_cascade3 = cv2.CascadeClassifier('./data/haarcascade_righteye_2splits.xml')

model_yolo = './data/yolov3-tiny.weights'
config_yolo = './data/yolov3-tiny.cfg'
class_labels = './data/coco.names'
confThreshold = 0.352
nmsThreshold = 0.4

cap = cv2.VideoCapture(0)
#init
eye_det_l = 0
eye_det_r = 0
frame_num = 0
sum_l_rev = 0
sum_r_rev = 0

eyeDet_nRcnt=0
eyeDet_nLcnt=0

sleep_value=50

PHONE_FLAG = 0
FACE_NOT_DETECT_NUM = 0
EYE_NOT_DETECT_NUM = 0
if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()

##yolo_net read
net_yolo = cv2.dnn.readNet(model_yolo, config_yolo)
if net_yolo.empty():
    print('Net open failed!')
    sys.exit()

classes = []
with open(class_labels, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
colors = np.random.uniform(0, 255, size=(len(classes), 3))

layer_names = net_yolo.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net_yolo.getUnconnectedOutLayers()]

#dnn_net read
net = cv2.dnn.readNet(model, config)
if net.empty():
    print('Net open failed!')
    sys.exit()

#INSERT db DATA
conn = pymysql.connect(host='192.168.0.194', user='root', password='qwerasdf12', db='raspi_db', charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from collect_data")
sql = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        break
    
    ##yolo blob img
    blob_yolo = cv2.dnn.blobFromImage(frame, 1/255., (320, 320), swapRB=True)
    net_yolo.setInput(blob_yolo)
    outs_yolo = net_yolo.forward(output_layers)
    h, w = frame.shape[:2]

    class_ids = []
    confidences = []
    boxes = []
    
    #dnn blob img
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    out = net.forward()

    detect = out[0, 0, :, :]
    (h, w) = frame.shape[:2]

    #yolo detection
    for out in outs_yolo:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence_yolo = scores[class_id]
            if confidence_yolo > confThreshold:
                cx = int(detection[0] * w)
                cy = int(detection[1] * h)
                bw = int(detection[2] * w)
                bh = int(detection[3] * h)

                sx = int(cx - bw / 2)
                sy = int(cy - bh / 2)

                boxes.append([sx, sy, bw, bh])
                confidences.append(float(confidence_yolo))
                class_ids.append(int(class_id))

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    #yolo cell  phone detection
    for i in indices:
        i = i[0]
        if classes[class_ids[i]] == 'cell phone' :
            if PHONE_FLAG == 0 :
                PHONE_FLAG = 1
                sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('phone', NOW())"
                cursor.execute(sql)
                conn.commit()
            # sx, sy, bw, bh = boxes[i]
            # label = '{0}: {1:.2f}'.format(classes[class_ids[i]],confidences[i])
            # color = colors[class_ids[i]]
            # cv2.rectangle(frame, (sx, sy, bw, bh), color, 2)
            # cv2.putText(frame, label, (sx, sy - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
        else :
            PHONE_FLAG = 0



    # t, _ = net_yolo.getPerfProfile()
    # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    # cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    #             0.7, (0, 0, 255), 1, cv2.LINE_AA)

    #dnn face detection
    if not PHONE_FLAG :
        FACE_DETECT_FLAG = 0
        for i in range(detect.shape[0]):
            confidence = detect[i, 2]
            if confidence < 0.5:
                if FACE_NOT_DETECT_NUM>600 :
                    sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('sleep', NOW())"
                    cursor.execute(sql)
                    conn.commit()
                FACE_NOT_DETECT_NUM+=1
                break
            FACE_DETECT_FLAG = 1
            FACE_NOT_DETECT_NUM = 0
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

        #eyedetection
        if FACE_DETECT_FLAG :
            eye_left = eye_cascade2.detectMultiScale(roi_gray_left,1.3,5,minSize=(20,20))
            eye_right = eye_cascade3.detectMultiScale(roi_gray_right,1.3,5,minSize=(20,20))
            for(ex, ey, ew, eh) in eye_left:
                cv2.rectangle(roi_color_left,(ex,(int)(ey+ey/6)),(ex+ew,ey+eh),(0,255,0),2)
                roi_eye_left = roi_gray_left[ey+(int)(ey/6): ey+eh, ex:ex+ew]
            for(ex, ey, ew, eh) in eye_right:
                cv2.rectangle(roi_color_right,(ex,(int)(ey+ey/6)),(ex+ew,ey+eh),(0,255,0),2)
                roi_eye_right = roi_gray_right[ey+(int)(ey/6): ey+eh, ex:ex+ew]
            
            #get_eye_edge
            if (eye_left != ()) :
                roi_eye_left_canny = roi_eye_left.copy()
                roi_eye_left_canny_ret, roi_eye_left_canny_b = cv2.threshold(roi_eye_left_canny, 50,255, cv2.THRESH_BINARY) 
                roi_eye_left_canny_e = cv2.Canny(roi_eye_left_canny, 70, 150)
                roi_eye_left_canny_ret, roi_eye_left_canny_e = cv2.threshold(roi_eye_left_canny_e, 50,255, cv2.THRESH_BINARY) 
                eye_det_l = 1
                if (str(type(roi_eye_left_canny_b)) != "<type 'NoneType'>"):
                    cv2.imshow('roi_eye_left_canny', roi_eye_left_canny_e)
            else:
                eye_det_l = 0
                eyeDet_nLcnt+=1
            if (eye_right != ()) :
                roi_eye_right_canny = roi_eye_right.copy()
                roi_eye_right_canny_ret, roi_eye_right_canny_b = cv2.threshold(roi_eye_right_canny, 50,250, cv2.THRESH_BINARY) 
                roi_eye_right_canny_e = cv2.Canny(roi_eye_right_canny, 70, 150)
                roi_eye_right_canny_ret, roi_eye_right_canny_e = cv2.threshold(roi_eye_right_canny_e, 50,255, cv2.THRESH_BINARY) 
                eye_det_r = 1
                if (str(type(roi_eye_right_canny_e)) != "<type 'NoneType'>"):
                    cv2.imshow('roi_eye_right_canny', roi_eye_right_canny_e)
            else :
                eye_det_r = 0
                eyeDet_nRcnt+=1

        #sleep detection
        if eye_det_l == 1 :
            sum_l = 0
            if (str(type(roi_eye_left_canny_e)) != "<type 'NoneType'>"):
                height, width = roi_eye_left_canny_e.shape
            for i in range(0,height) :
                for j in range(0,width) :
                    if (str(type(roi_eye_left_canny_e)) != "<type 'NoneType'>"):
                        sum_l += roi_eye_left_canny_e[i][j]/255
        else :
            sum_l = 0
        if eye_det_r == 1 :
            sum_r = 0
            if (str(type(roi_eye_right_canny_e)) != "<type 'NoneType'>"):
                height, width = roi_eye_right_canny_e.shape
            for i in range(0,height) :
                for j in range(0,width) :
                    if (str(type(roi_eye_right_canny_e)) != "<type 'NoneType'>"):
                        sum_r += roi_eye_right_canny_e[i][j]/255
        else :
            sum_r = 0



        if FACE_DETECT_FLAG :
            if (frame_num<9):
                sum_r_rev += sum_r
                sum_l_rev += sum_l
                frame_num+=1
            else :
                sum_r_rev += sum_r
                sum_l_rev += sum_l 
                frame_num = 0
                if(eyeDet_nLcnt<10 and eyeDet_nRcnt<10) :
                    sum_r_rev/=(10-eyeDet_nRcnt)
                    sum_l_rev/=(10-eyeDet_nLcnt)
                else :
                    sum_l_rev = 0
                    sum_r_rev = 0
                if ((sum_r_rev<sleep_value) and (sum_l_rev<sleep_value)) :
                    print('sleep')
                    if EYE_NOT_DETECT_NUM>600 :
                        sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('sleep', NOW())"
                        cursor.execute(sql)
                        conn.commit()
                else :
                    print('dont sleep')
                print('sum_l_rev = {0:>d}, sum_r_rev = {1:>4d}'.format(sum_l_rev, sum_r_rev))
                eyeDet_nLcnt = 0
                eyeDet_nRcnt = 0
            print('sum_l = {0:>4d}, sum_r = {1:>4d}'.format(sum_l, sum_r))
        else :
            sum_l_rev = 0
            sum_r_rev = 0
            eyeDet_nLcnt = 0
            eyeDet_nRcnt = 0
                




    #initial value
    eye_det_l = 0
    eye_det_r = 0
    roi_eye_left_canny_b = 0
    roi_eye_left_canny_e = 0
    roi_eye_left_canny_ret = 0
    roi_eye_right_canny_b = 0
    roi_eye_right_canny_e = 0
    roi_eye_right_canny_ret = 0
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
sql = "INSERT INTO collect_data(TextData, LastUpdate) VALUES ('studyfinish', NOW())"
cursor.execute(sql)
conn.commit()
cv2.destroyAllWindows()