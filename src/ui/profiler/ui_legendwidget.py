# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './profiler/legendwidget.ui'
#
# Created: Tue Jun 21 10:58:17 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LegendWidget(object):
    def setupUi(self, LegendWidget):
        LegendWidget.setObjectName("LegendWidget")
        LegendWidget.resize(755, 170)
        self.verticalLayout_2 = QtGui.QVBoxLayout(LegendWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtGui.QScrollArea(LegendWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setGeometry(QtCore.QRect(0, 0, 735, 114))
        self.scrollWidget.setObjectName("scrollWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollWidget)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtGui.QPushButton(LegendWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(LegendWidget)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), LegendWidget.close)
        QtCore.QMetaObject.connectSlotsByName(LegendWidget)

    def retranslateUi(self, LegendWidget):
        LegendWidget.setWindowTitle(QtGui.QApplication.translate("LegendWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("LegendWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

