# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mainwindow.ui'
#
# Created: Tue Jun 21 10:58:16 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1509, 659)
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(MainWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.aboutButton = QtGui.QPushButton(MainWindow)
        self.aboutButton.setObjectName("aboutButton")
        self.horizontalLayout.addWidget(self.aboutButton)
        self.quitButton = QtGui.QPushButton(MainWindow)
        self.quitButton.setObjectName("quitButton")
        self.horizontalLayout.addWidget(self.quitButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL("clicked()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Profile Extractor", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

