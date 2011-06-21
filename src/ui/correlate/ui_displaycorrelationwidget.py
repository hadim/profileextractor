# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './correlate/displaycorrelationwidget.ui'
#
# Created: Tue Jun 21 10:58:16 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DisplayCorrelationWidget(object):
    def setupUi(self, DisplayCorrelationWidget):
        DisplayCorrelationWidget.setObjectName("DisplayCorrelationWidget")
        DisplayCorrelationWidget.resize(814, 540)
        self.verticalLayout = QtGui.QVBoxLayout(DisplayCorrelationWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container = QtGui.QLabel(DisplayCorrelationWidget)
        self.container.setText("")
        self.container.setObjectName("container")
        self.verticalLayout.addWidget(self.container)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.statusBar = QtGui.QLabel(DisplayCorrelationWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setText("")
        self.statusBar.setObjectName("statusBar")
        self.horizontalLayout.addWidget(self.statusBar)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveButton = QtGui.QPushButton(DisplayCorrelationWidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.closeButton = QtGui.QPushButton(DisplayCorrelationWidget)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DisplayCorrelationWidget)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), DisplayCorrelationWidget.close)
        QtCore.QMetaObject.connectSlotsByName(DisplayCorrelationWidget)

    def retranslateUi(self, DisplayCorrelationWidget):
        DisplayCorrelationWidget.setWindowTitle(QtGui.QApplication.translate("DisplayCorrelationWidget", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("DisplayCorrelationWidget", "Save as .png", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("DisplayCorrelationWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

