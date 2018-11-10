import cv2
import numpy as np

class HandDetector():
    def __init__(self):
        self.closed_palm_classifier = cv2.CascadeClassifier("xmls/closed_palm.xml")
        self.opened_palm_classifier = cv2.CascadeClassifier("xmls/opened_palm.xml")
        self.face_classifier = cv2.CascadeClassifier("xmls/lbpcascade_frontalface_improved.xml")

        self.track_inited = False
        self.track_window = ()
        self.hsv_img = []
        self.hsv_roi = []
        self.hsv_l = np.array((0., 30., 60.))
        self.hsv_h = np.array((20., 150., 255.))
        self.roi_hist = []
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        pass

    def detect(self, img, mode):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        """face_rects = self.__detectMS(gray, self.face_classifier)
        for x1, y1, x2, y2 in face_rects:
            w = x2 - x1
            h = y2 - y1
            w_ratio = 0.1
            h_ratio = 0.4
            cv2.rectangle(gray, (x1-int(w*w_ratio), y1-int(h*h_ratio)),
                                (x2+int(w*w_ratio), y2+int(h*h_ratio)),
                                (0,0,0), -1)

        #cv2.imshow("gray",gray)"""


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

    def track_init(self, img, box):
        self.track_inited = True

        self.track_window = tuple(box)
        self.hsv_roi = img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        self.hsv_roi = cv2.cvtColor(self.hsv_roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(self.hsv_roi, self.hsv_l, self.hsv_h)
        self.roi_hist = cv2.calcHist([self.hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)

        pass

    def track(self, img, box):
        if not self.track_inited:
            return []

        self.hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([self.hsv_img], [0], self.roi_hist, [0, 180], 1)

        track_box, self.track_window = cv2.CamShift(dst, self.track_window, self.term_crit)

        return list(track_box)

        pass