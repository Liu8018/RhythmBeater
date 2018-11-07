# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(745, 573)
        Dialog.setMinimumSize(QtCore.QSize(745, 573))
        Dialog.setMaximumSize(QtCore.QSize(745, 573))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 721, 511))
        self.label.setStyleSheet("background-color: rgb(93, 93, 93);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.open_pushButton = QtWidgets.QPushButton(Dialog)
        self.open_pushButton.setGeometry(QtCore.QRect(20, 530, 88, 34))
        self.open_pushButton.setObjectName("open_pushButton")
        self.exit_pushButton = QtWidgets.QPushButton(Dialog)
        self.exit_pushButton.setGeometry(QtCore.QRect(630, 530, 88, 34))
        self.exit_pushButton.setObjectName("exit_pushButton")
        self.start_pushButton = QtWidgets.QPushButton(Dialog)
        self.start_pushButton.setGeometry(QtCore.QRect(280, 530, 88, 34))
        self.start_pushButton.setObjectName("start_pushButton")
        self.pause_pushButton = QtWidgets.QPushButton(Dialog)
        self.pause_pushButton.setGeometry(QtCore.QRect(370, 530, 88, 34))
        self.pause_pushButton.setObjectName("pause_pushButton")
        self.text_label = QtWidgets.QLabel(Dialog)
        self.text_label.setGeometry(QtCore.QRect(10, 10, 721, 31))
        self.text_label.setText("")
        self.text_label.setObjectName("text_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RhythmBeater"))
        self.open_pushButton.setText(_translate("Dialog", "open"))
        self.exit_pushButton.setText(_translate("Dialog", "exit"))
        self.start_pushButton.setText(_translate("Dialog", "start"))
        self.pause_pushButton.setText(_translate("Dialog", "pause"))

