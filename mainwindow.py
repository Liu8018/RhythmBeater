import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from ui_mainwindow import Ui_Dialog
from PyQt5.QtCore import QTimer, pyqtSlot, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import numpy as np
import cv2
import random
from HandDetector import HandDetector

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 载入ui文件
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 打开摄像头
        try:
            self.capture = cv2.VideoCapture(0)
        except:
            self.capture = cv2.VideoCapture('/dev/video0')
        _, self.frame = self.capture.read()
        self.height, self.width, self.bytesPerComponent = self.frame.shape
        self.frame_to_show = np.zeros(shape=(self.height,self.width,3),dtype=np.uint8)
        self.cover = np.zeros(shape=(self.height,self.width,3),dtype=np.uint8)

        # hand_detector初始化
        self.hand_detector1 = HandDetector()
        self.hand_detector2 = HandDetector()
        self.hand_pos = [[],[]]

        # 创建计时器
        self.timer = QTimer(self)
        self.timer.setInterval(1000 / self.capture.get(cv2.CAP_PROP_FPS))
        self.timer.start()
        self.timer.timeout.connect(self.get_frame)

        self.music_file_path = " "
        self.player = QMediaPlayer()
        self.music_inputed = False
        self.player_started = False

        self.beat_times = []
        self.start_time = 0.0
        self.played_time = 0.0

        self.blocks = [[], [], [], []]

        pass

    def reset(self):
        self.player_started = False

        self.beat_times = []
        self.start_time = 0.0
        self.played_time = 0.0

        self.blocks = [[], [], [], []]

    @pyqtSlot()
    def on_open_pushButton_clicked(self):
        self.reset()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.music_file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "",
                                                  "music file (*.mp3)", options=options)
        if self.music_file_path:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file_path)))
            self.ui.text_label.setText(self.music_file_path)

            # 生成节拍序列，存储在csv文件里
            #os.system("python3 beat_tracker.py " + self.music_file_path + " beat_times.csv")
            self.load_csv()

            self.music_inputed = True

    @pyqtSlot()
    def on_exit_pushButton_clicked(self):
        #os.system("rm beat_times.csv")
        exit(0)

    def start_play(self):
        if self.music_inputed and (not self.player_started):
            self.player.play()
            self.player_started = True

            self.start_time = cv2.getTickCount()
            self.played_time = 0.0

        pass

    @pyqtSlot()
    def get_frame(self):
        # 读取一帧并左右翻转
        _,self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)

        # cover初始化
        self.cover = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

        # 检测手
        rects = self.hand_detector1.detect(self.frame, "opened")
        self.draw_rects(self.cover, rects, (0, 255, 0))

        # 如果检测到两只张开的手掌，则开始播放
        if len(rects) >= 2:
            self.start_play()

            self.hand_pos[0] = rects[0]
            self.hand_pos[1] = rects[1]

            self.hand_detector1.track_init(self.frame, self.hand_pos[0])
            self.hand_detector2.track_init(self.frame, self.hand_pos[1])

        self.hand_pos[0] = self.hand_detector1.track(self.frame, self.hand_pos[0])
        self.hand_pos[1] = self.hand_detector2.track(self.frame, self.hand_pos[1])
        if len(self.hand_pos[0]):
            #print(self.hand_pos[0])
            cv2.ellipse(self.cover, tuple(self.hand_pos[0]), (0, 0, 255), 2)
        if len(self.hand_pos[1]):
            #print(self.hand_pos[1])
            cv2.ellipse(self.cover, tuple(self.hand_pos[1]), (0, 0, 255), 2)

        # 更新played_time
        if self.music_inputed and self.player_started:
            self.played_time = (cv2.getTickCount() - self.start_time) / cv2.getTickFrequency()

            # 若到达节拍点则生成一个block
            if self.played_time >= self.beat_times[0]:
                self.generate_block()
                self.beat_times.pop(0)

            # 移动block
            self.move_blocks()

        # 显示图片到label上
        self.show_frame()

    def show_frame(self):
        # 画线
        cv2.line(self.cover, (int(self.width / 2), 0), (int(self.width / 2), self.height), (255, 0, 0), 2)
        cv2.line(self.cover, (int(self.width / 4), 0), (int(self.width / 4), self.height), (255, 0, 0), 2)
        cv2.line(self.cover, (int(self.width*3/4), 0), (int(self.width*3/4), self.height), (255, 0, 0), 2)

        # 画blocks
        for i, _ in enumerate(self.blocks):
            for block in self.blocks[i]:
                cv2.line(self.cover, (int(self.width/4*i)+5, self.height - block),
                                     (int(self.width/4*(i+1))-5, self.height - block),
                                     (0,255,0),8)

        # 叠加显示frame与cover
        self.frame_to_show = cv2.add(self.frame, self.cover)

        # 调整大小
        self.frame_to_show = cv2.resize(self.frame_to_show, (self.ui.label.width(), self.ui.label.height()))

        self.frame_to_show = cv2.cvtColor(self.frame_to_show, cv2.COLOR_BGR2RGB)
        height, width, bytesPerComponent = self.frame_to_show.shape
        bytesPerLine = 3 * width
        qimg = QImage(self.frame_to_show.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.label.setPixmap(pixmap)

    def load_csv(self):
        with open("beat_times.csv") as file:
            for line in file:
                self.beat_times.append(float(line))

    def generate_block(self):
        n = random.randint(0,3)
        self.blocks[n].append(0)
        pass

    def move_blocks(self):
        for i, _ in enumerate(self.blocks):
            for j, _ in enumerate(self.blocks[i]):
                self.blocks[i][j] += 5

            while self.blocks[i] and (self.blocks[i][0] > self.height):
                self.blocks[i].pop(0)
        pass

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        pass