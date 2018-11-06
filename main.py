import sys
from PyQt5.QtWidgets import QApplication, QDialog
from mainwindow import MainWindow

app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(mainwindow.exec())