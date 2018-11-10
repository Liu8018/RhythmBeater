import cv2
import numpy as np

class HandDetector():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.skin_img = np.zeros(shape=(self.height, self.width), dtype=np.uint8)

        pass

    def detect(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_img = cv2.medianBlur(hsv_img,5)
        self.skin_img = cv2.inRange(hsv_img, np.array((0., 30., 60.)), np.array((20., 150., 255.)))

        # 预处理
        self.skin_img = cv2.medianBlur(self.skin_img, 5)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        self.skin_img = cv2.dilate(self.skin_img, kernel)

        # 检测轮廓
        _, contours, _ = cv2.findContours(self.skin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # 找到面积最大的轮廓
            maxArea = 0.0
            maxCnt = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > maxArea:
                    maxArea = area
                    maxCnt = cnt

            # 检测手指
            hull = cv2.convexHull(maxCnt, returnPoints=False)
            defects = cv2.convexityDefects(maxCnt, hull)

            # 匹配
            template = cv2.imread("palm1.png",0)
            ret, template = cv2.threshold(template, 127, 255, 0)
            _, cnts, _ = cv2.findContours(template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            match_rate = cv2.matchShapes(cnts[0], maxCnt, 1, 0.0)
            print(match_rate)

            # test
            canvas = np.zeros((self.width, self.height, 3), dtype=np.uint8)
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(maxCnt[s][0])
                end = tuple(maxCnt[e][0])
                far = tuple(maxCnt[f][0])
                cv2.line(canvas, start, end, [0, 255, 0], 2)
                cv2.line(canvas, far, start, [0, 255, 0], 2)
                cv2.line(canvas, far, end, [0, 255, 0], 2)
                cv2.circle(canvas, far, 5, [0, 0, 255], -1)
            cv2.imshow("skin",canvas)
            cv2.waitKey()

        pass

    def __detect_palm(self):
        pass