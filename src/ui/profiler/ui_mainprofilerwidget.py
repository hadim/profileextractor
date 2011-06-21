# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './profiler/mainprofilerwidget.ui'
#
# Created: Tue Jun 21 13:26:36 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainProfilerWidget(object):
    def setupUi(self, MainProfilerWidget):
        MainProfilerWidget.setObjectName("MainProfilerWidget")
        MainProfilerWidget.resize(1190, 571)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainProfilerWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(MainProfilerWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayout_2.addWidget(self.splitter)
        self.scrollArea = QtGui.QScrollArea(MainProfilerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 21, 1170, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.statusBar = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.statusBar.setText("")
        self.statusBar.setObjectName("statusBar")
        self.horizontalLayout.addWidget(self.statusBar)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loadButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout.addWidget(self.loadButton)
        self.saveCsvButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.saveCsvButton.setEnabled(False)
        self.saveCsvButton.setObjectName("saveCsvButton")
        self.horizontalLayout.addWidget(self.saveCsvButton)
        self.saveButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.saveButton.setEnabled(False)
        self.saveButton.setDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.legendButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.legendButton.setEnabled(False)
        self.legendButton.setObjectName("legendButton")
        self.horizontalLayout.addWidget(self.legendButton)
        self.mergeButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.mergeButton.setObjectName("mergeButton")
        self.horizontalLayout.addWidget(self.mergeButton)
        self.helpButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.helpButton.setEnabled(False)
        self.helpButton.setObjectName("helpButton")
        self.horizontalLayout.addWidget(self.helpButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(MainProfilerWidget)
        QtCore.QMetaObject.connectSlotsByName(MainProfilerWidget)

    def retranslateUi(self, MainProfilerWidget):
        MainProfilerWidget.setWindowTitle(QtGui.QApplication.translate("MainProfilerWidget", "Profile Visualizer", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Load .csv file", None, QtGui.QApplication.UnicodeUTF8))
        self.saveCsvButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Save current as .csv", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Save current profile as an image", None, QtGui.QApplication.UnicodeUTF8))
        self.legendButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Display legend", None, QtGui.QApplication.UnicodeUTF8))
        self.mergeButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Merge controls", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("MainProfilerWidget", "Help", None, QtGui.QApplication.UnicodeUTF8))

