# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './about.ui'
#
# Created: Tue Jun 21 13:26:36 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AboutWidget(object):
    def setupUi(self, AboutWidget):
        AboutWidget.setObjectName("AboutWidget")
        AboutWidget.resize(603, 372)
        self.gridLayout_3 = QtGui.QGridLayout(AboutWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtGui.QTabWidget(AboutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtGui.QLabel(self.tab)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtGui.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.licenseText = QtGui.QTextEdit(self.tab_2)
        self.licenseText.setReadOnly(True)
        self.licenseText.setAcceptRichText(False)
        self.licenseText.setObjectName("licenseText")
        self.gridLayout.addWidget(self.licenseText, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.authorsText = QtGui.QTextEdit(self.tab_3)
        self.authorsText.setReadOnly(True)
        self.authorsText.setAcceptRichText(False)
        self.authorsText.setObjectName("authorsText")
        self.gridLayout_2.addWidget(self.authorsText, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtGui.QPushButton(AboutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(AboutWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), AboutWidget.close)
        QtCore.QMetaObject.connectSlotsByName(AboutWidget)

    def retranslateUi(self, AboutWidget):
        AboutWidget.setWindowTitle(QtGui.QApplication.translate("AboutWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.titleLabel.setText(QtGui.QApplication.translate("AboutWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">ProfileExtractor - VERSION_HERE</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AboutWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ProfileExtractor is a software designed in the aim to extract informations from image segmentation results performed by CellProfiler.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AboutWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ProfileExtractor is under BSD license</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("AboutWidget", "About ProfileExtractor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("AboutWidget", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("AboutWidget", "Authors", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("AboutWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))

