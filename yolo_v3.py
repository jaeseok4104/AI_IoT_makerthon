import sys
import numpy as np
import cv2


model_yolo = './data/yolov3-tiny.weights'
config_yolo = './data/yolov3-tiny.cfg'
class_labels = './data/coco.names'
confThreshold = 0.352
nmsThreshold = 0.4

cap = cv2.VideoCapture(0)

if not cap.isOpened():
   print('Camera open failed!')
   sys.exit()

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

while True:
    ret, frame = cap.read()

    if not ret:
        break

    blob_yolo = cv2.dnn.blobFromImage(frame, 1/255., (320, 320), swapRB=True)
    net_yolo.setInput(blob_yolo)
    outs_yolo = net_yolo.forward(output_layers)
    h, w = frame.shape[:2]

    class_ids = []
    confidences = []
    boxes = []

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
    for i in indices:
            i = i[0]
            sx, sy, bw, bh = boxes[i]
            label = '{}: {}'.format(classes[class_ids[i]],{confidences[i]:.2})
            if (classes[class_ids[i]] == "cell phone") :
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (sx, sy, bw, bh), color, 2)
                cv2.putText(frame, label, (sx, sy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

    t, _ = net_yolo.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
