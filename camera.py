
import numpy as np
import os
from imutils.video import VideoStream, FPS
import cv2


class SmartCamera():

    def __init__(self):
        resolution = (320, 240)

        self.classes: list = self.readClasses()
        self.categories: list = self.ClassToCategory(self.classes)

        self.vs = VideoStream(src=0, framerate=10,
                              resolution=resolution).start()

        self.net = cv2.dnn.readNetFromCaffe('./Models/MobileNetSSD.txt',
                                            './Models/MobileNetSSD.caffemodel')
        
        print('camera is ready')


    def MobileNetStart(self):

        img = self.vs.read()

        h, w = img.shape[0], img.shape[1]

        sizeImg = (300, 300)

        img_reseze = cv2.resize(img, sizeImg)
        blob = cv2.dnn.blobFromImage(img_reseze, 0.007843, sizeImg, 127.5)
        self.net.setInput(blob)

        detections = self.net.forward()


        colors = np.random.uniform(255, 0, size=(len(self.categories), 3))

        for i in np.arange(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:

                idx = int(detections[0, 0, i, 1])

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                (startX, startY, endX, endY) = box.astype('int')

                label = f"{self.classes[idx]} {int(confidence * 100)}%"

                if 'person' in self.classes[idx] or 'cat' in self.classes[idx] or 'dog' in self.classes[idx] or 'car' in self.classes[idx]:

                    cv2.rectangle(img, (startX, startY),
                                (endX, endY), colors[idx], 4)

                    y = startY - 15 if startY - 15>15 else startY + 15  
                    cv2.putText(img, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
                    
                    return img

    def readClasses(self):
        return open('./Files/classItems.txt', 'r').readlines()

    def ClassToCategory(self, classes: list):

        category = []

        for i, _class in enumerate(classes):    

            _class = _class.replace("\n",'')
            category.append({i:_class})

        return category
