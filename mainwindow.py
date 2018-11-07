from PyQt5.QtWidgets import QDialog, QFileDialog
from ui_mainwindow import Ui_Dialog
from PyQt5.QtCore import QTimer, pyqtSlot, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import cv2

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 载入ui文件
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 打开摄像头
        self.capture = cv2.VideoCapture('/dev/video0')
        _, self.frame = self.capture.read()
        self.frame_to_show = self.frame

        # 创建计时器
        self.timer = QTimer(self)
        self.timer.setInterval(1000 / self.capture.get(cv2.CAP_PROP_FPS))
        self.timer.start()
        self.timer.timeout.connect(self.getFrame)

        self.music_file_path = " "
        self.player = QMediaPlayer()

    @pyqtSlot()
    def on_open_pushButton_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.music_file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file_path)))
        self.player.play()

    @pyqtSlot()
    def on_start_pushButton_clicked(self):
        pass

    @pyqtSlot()
    def on_exit_pushButton_clicked(self):
        exit(0)

    @pyqtSlot()
    def getFrame(self):
        # 读取一帧并左右翻转
        _,self.frame = self.capture.read()
        self.frame = cv2.flip(self.frame, 1)

        # 调整大小
        self.frame = cv2.resize(self.frame, (self.ui.label.width(), self.ui.label.height()))

        # 显示到label上
        self.show_frame()

    def show_frame(self):
        height, width, bytesPerComponent = self.frame.shape
        bytesPerLine = 3 * width
        self.frame_to_show = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        qimg = QImage(self.frame_to_show.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.ui.label.setPixmap(pixmap)