import cv2
import numpy as np

class HandDetector():
    def __init__(self):
        self.closed_palm_classifier = cv2.CascadeClassifier("xmls/closed_palm.xml")
        self.opened_palm_classifier = cv2.CascadeClassifier("xmls/opened_palm.xml")

        pass

    def detect(self, img, mode):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        if mode == "closed":
            rects = self.__detectMS(gray, self.closed_palm_classifier)
        else:
            rects = self.__detectMS(gray, self.opened_palm_classifier)

        return rects

    def __detectMS(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        return rects